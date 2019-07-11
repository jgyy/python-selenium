"""
When migrating to AWS CodeCommit, consider pushing your repository in increments or chunks to
reduce the chances an intermittent network issue or degraded network performance causes the
entire push to fail. By using incremental pushes with this script, you can restart the migration
and push only those commits that did not succeed on the earlier attempt.
"""
# !/usr/bin/env python3
import os
import sys
import argparse
from git import Repo, TagReference, RemoteProgress, GitCommandError


class PushProgressPrinter(RemoteProgress):
    """
    push progress printer class
    """
    def update(self, op_code, cur_count, max_count=None, message=''):
        """
        :param op_code: operational code
        :param cur_count: current count
        :param max_count: maximum count
        :param message: git message
        """
        op_id = op_code & self.OP_MASK
        stage_id = op_code & self.STAGE_MASK
        if op_id == self.WRITING and stage_id == self.BEGIN:
            print("\tObjects: %d" % max_count)


class RepoInit:
    """
    repository migration super class
    """
    MAX_COMMITS_TOLERANCE_PERCENT = 0.05
    PUSH_RETRY_LIMIT = 3
    MIGRATION_TAG_PREFIX = "codecommit_migration_"

    def __init__(self, repo_dir, remote_name, commit_batch_size, clean):
        self.local_repo = Repo(repo_dir)
        self.remote_name = remote_name
        self.remote_migration_tags = dict({})

        # max commits per push
        self.mcpp = commit_batch_size
        self.max_commits_tolerance = self.mcpp * self.MAX_COMMITS_TOLERANCE_PERCENT
        self.clean = clean

    def get_remote_migration_tags(self):
        """
        check if this tags is alright
        """
        remote_tags_output = self.local_repo.git.ls_remote(
            self.remote_name, tags=True).split('\n')
        self.remote_migration_tags = dict(
            (
                tag.split()[1].replace("refs/tags/", ""), tag.split()[0]
            ) for tag in remote_tags_output if self.MIGRATION_TAG_PREFIX in tag
        )

    def clean_up(self, clean_up_remote=False):
        """
        :param clean_up_remote: clean up remote status
        """
        tags = [
            tag for tag in self.local_repo.tags if tag.name.startswith(self.MIGRATION_TAG_PREFIX)
        ]

        # delete the local tags
        TagReference.delete(self.local_repo, *tags)

        # delete the remote tags
        if clean_up_remote:
            tags_to_delete = [":" + tag_name for tag_name in self.remote_migration_tags]
            self.local_repo.remote(self.remote_name).push(refspec=tags_to_delete)


class RepositoryMigration(RepoInit):
    """
    repository migration class
    """

    def __init__(self, repo_dir, remote_name, commit_batch_size, clean):
        # noinspection PyCompatibility
        super().__init__(repo_dir, remote_name, commit_batch_size, clean)
        self.w_c = set()
        self.migration_tags = []
        self.next_tag_number = 0

    def migrate_repository_in_parts(self):
        """
        :return: ends the function if clean
        """
        try:
            self.local_repo.remote(self.remote_name)
            self.get_remote_migration_tags()
        except (ValueError, GitCommandError):
            print(
                "Could not contact the remote repository. The most common reasons for this error "
                "are that the name of the remote repository is incorrect, or that you do not "
                "have permissions to interact with that remote repository."
            )
            sys.exit(1)

        if self.clean:
            self.clean_up(clean_up_remote=True)
            return

        self.clean_up()

        print("Analyzing repository")
        head_commit = self.local_repo.head.commit
        sys.setrecursionlimit(max(sys.getrecursionlimit(), head_commit.count()))

        # tag commits on default branch
        leftover_commits = self.migrate_commit(head_commit)
        self.tag_commits([commit for (commit, commit_count) in leftover_commits])

        # tag commits on each branch
        for branch in self.local_repo.heads:
            leftover_commits = self.migrate_commit(branch.commit)
            self.tag_commits([commit for (commit, commit_count) in leftover_commits])

        # push the tags
        self.push_migration_tags()

        # push all branch references
        for branch in self.local_repo.heads:
            print("Pushing branch %s" % branch.name)
            self.do_push_with_retries(ref=branch.name)

        # push all tags
        print("Pushing tags")
        self.do_push_with_retries(push_tags=True)

        self.get_remote_migration_tags()
        self.clean_up(clean_up_remote=True)

        print("Migration to CodeCommit was successful")

    def migrate_commit(self, commit):
        """
        :param commit: git commit
        :return: empty list if there are commit
        """
        if commit in self.w_c:
            return []

        pending_ancestor_pushes = []
        commit_count = 1

        if len(commit.parents) > 1:
            # This is a merge commit
            # Ensure that all parents are pushed first
            for parent_commit in commit.parents:
                pending_ancestor_pushes.extend(self.migrate_commit(parent_commit))
        elif len(commit.parents) == 1:
            # Split linear history into individual pushes
            next_ancestor, c_to_next_ancestor = self.find_next_ancestor_for_push(commit.parents[0])
            commit_count += c_to_next_ancestor
            pending_ancestor_pushes.extend(self.migrate_commit(next_ancestor))

        self.w_c.add(commit)

        return self.stage_push(commit, commit_count, pending_ancestor_pushes)

    def find_next_ancestor_for_push(self, commit):
        """
        Traverse linear history until we reach our commit limit, a merge commit, or an initial
        commit
        :param commit: git commit
        :return: commit and commit count
        """
        commit_count = 0

        while len(commit.parents) == 1 and commit_count < self.mcpp and commit not in self.w_c:
            commit_count += 1
            self.w_c.add(commit)
            commit = commit.parents[0]

        return commit, commit_count

    def stage_push(self, commit, commit_count, pending_ancestor_pushes):
        """
        Determine whether we can roll up pending ancestor pushes into this push
        :param commit: git commit
        :param commit_count: git commit count
        :param pending_ancestor_pushes: pending git ancestor push
        :return: returns list
        """
        combined_commit_count = commit_count + sum(
            ancestor_commit_count for (ancestor, ancestor_commit_count) in pending_ancestor_pushes
        )

        if combined_commit_count < self.mcpp:
            # don't push anything, roll up all pending ancestor pushes into this pending push
            return [(commit, combined_commit_count)]

        if combined_commit_count <= (self.mcpp + self.max_commits_tolerance):
            # roll up everything into this commit and push
            self.tag_commits([commit])
            return []

        if commit_count >= self.mcpp:
            # need to push each pending ancestor and this commit
            self.tag_commits(
                [ancestor for (ancestor, ancestor_commit_count) in pending_ancestor_pushes]
            )
            self.tag_commits([commit])
            return []

        # push each pending ancestor, but roll up this commit
        self.tag_commits(
            [ancestor for (ancestor, ancestor_commit_count) in pending_ancestor_pushes]
        )
        return [(commit, commit_count)]

    def tag_commits(self, commits):
        """
        :param commits: git commits
        """
        for commit in commits:
            self.next_tag_number += 1
            tag_name = self.MIGRATION_TAG_PREFIX + str(self.next_tag_number)

            if tag_name not in self.remote_migration_tags:
                tag = self.local_repo.create_tag(tag_name, ref=commit)
                self.migration_tags.append(tag)
            elif self.remote_migration_tags[tag_name] != str(commit):
                print(
                    "Migration tags on the remote do not match the local tags. Most likely your "
                    "batch size has changed since the last time you ran this script. Please run "
                    "this script with the --clean option, and try again."
                )
                sys.exit(1)

    def push_migration_tags(self):
        """
        push migration tags function
        """
        print("Will attempt to push %d tags" % len(self.migration_tags))
        self.migration_tags.sort(
            key=lambda tag: int(tag.name.replace(self.MIGRATION_TAG_PREFIX, ""))
        )
        for tags in self.migration_tags:
            print("Pushing tag %s (out of %d tags), commit %s" % (tags.name, self.next_tag_number,
                                                                  str(tags.commit)))
            self.do_push_with_retries(ref=tags.name)

    def do_push_with_retries(self, ref=None, push_tags=False):
        """
        :param ref: git reference
        :param push_tags: git push tags
        :return: ends function if successful
        """
        for i in range(0, self.PUSH_RETRY_LIMIT):
            if i == 0:
                progress_printer = PushProgressPrinter()
            else:
                progress_printer = None

            try:
                success = self.information(push_tags, progress_printer, ref)

                if success:
                    return
            except GitCommandError as err:
                print(err)

        if push_tags:
            print("Pushing all tags failed after %d attempts" % self.PUSH_RETRY_LIMIT)
        elif ref is not None:
            print("Pushing %s failed after %d attempts" % (ref, self.PUSH_RETRY_LIMIT))
            print(
                "For more information about the cause of this error, run the following command "
                "from the local repo: 'git push %s %s'" % (self.remote_name, ref)
            )
        else:
            print("Pushing all branches failed after %d attempts" % self.PUSH_RETRY_LIMIT)
        sys.exit(1)

    def information(self, push_tags, progress_printer, ref):
        """
        :param push_tags: git push tags
        :param progress_printer: push process printer
        :param ref: git reference
        :return: success status
        """
        if push_tags:
            infos = self.local_repo.remote(
                self.remote_name).push(tags=True, progress=progress_printer)
        elif ref is not None:
            infos = self.local_repo.remote(
                self.remote_name).push(refspec=ref, progress=progress_printer)
        else:
            infos = self.local_repo.remote(
                self.remote_name).push(progress=progress_printer)

        success = True
        if not infos:
            success = False
        else:
            for i in infos:
                if i.flags & i.UP_TO_DATE or i.flags & i.NEW_TAG or i.flags & i.NEW_HEAD:
                    continue
                success = False
                print(i.summary)
        return success


PARSER = argparse.ArgumentParser(description='Process the AWS CodeCommit')
PARSER.add_argument(
    "-l", "--local", action="store", dest="localrepo", default=os.getcwd(),
    help="The path to the local repo. If this option is not specified, the script will attempt "
         "to use current directory by default. If it is not a local git repo, the script will "
         "fail."
)
PARSER.add_argument(
    "-r", "--remote", action="store", dest="remoterepo", default="codecommit",
    help="The name of the remote repository to be used as the push or migration destination. The "
         "remote must already be set in the local repo ('git remote add ...'). If this option is "
         "not specified, the script will use 'codecommit' by default."
)
PARSER.add_argument(
    "-b", "--batch", action="store", dest="batchsize", default="100",
    help="Specifies the commit batch size for pushes. If not explicitly set, the default is 1,"
         "000 commits."
)
PARSER.add_argument(
    "-c", "--clean", action="store_true", dest="clean", default=False,
    help="Remove the temporary tags created by migration from both the local repo and the remote "
         "repository. This option will not do any migration work, just cleanup. Cleanup is done "
         "automatically at the end of a successful migration, but not after a failure so that "
         "when you re-run the script, the tags from the prior run can be used to identify commit "
         "batches that were not pushed successfully."
)

ARGS = PARSER.parse_args()

MIGRATION = RepositoryMigration(
    ARGS.localrepo,
    ARGS.remoterepo,
    int(ARGS.batchsize),
    ARGS.clean
)
MIGRATION.migrate_repository_in_parts()
