# Python Selenium
Currently learning Selenium for the purpose of backend api.

[credential]
helper=!aws codecommit --profile AdminContributor credential-helper $@
usehttppath=true
[alias]
mfa=!~/populateSessionTokenProfile.sh AdminAssumer FetchMfaCredentials
[remote "origin"]
url=https://git-codecommit.ap-southeast-1.amazonaws.com/v1/repos/ship-migrate
fetch=+refs/heads/*:refs/remotes/origin/*
[branch "master"]
remote=origin
merge=refs/heads/master