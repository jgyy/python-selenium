"""
File I/O
'w' -> Write-Only Mode, 'r' -> Read-Only Mode
'r+' -> Read And Write Mode, 'a' -> Append Mode
Reading a file -> .read()
Reading line by line -> .readline()
With / As Keywords
"""

MY_LIST = ["first line", "second line", "third line"]
with open("first_file.txt", "r+") as MY_FILE:
    print(str(MY_FILE.read()))
    for item in MY_LIST:
        MY_FILE.write(str(item) + "\n")

with open("first_file.txt", "r+") as MY_FILE:
    print("Line by line ========>>")
    print(str(MY_FILE.readline()))
    print("Line by line ========>>")
    print(str(MY_FILE.readline()))
    print("Line by line ========>>")
    print(str(MY_FILE.readline()))
