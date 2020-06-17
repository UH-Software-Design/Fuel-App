# 
Quick basics on how to use github

-To download the repo to your local machine: git clone url

-Following sequence of commands to save changes to github:

->git status

->git add . 

->git commit -m "a comment describing the changes you made"

->git push

-#Git status can be skipped. You can simply use git add filename if you only want to save changes made   to   those files. 


-Create a branch: 

->git branch nameofnewbranch

->git checkout -b nameofnewbranch 

-#The first command will just create the branch. The second will create it and switch you to it.


-Working with branches:

-Can switch between branches using: git checkout branchname

-Save work with a modified push command: git push origin branchname

-Delete a brach using the folling commands:

->git branch -d branchname

->git push origin --delete branchname

-Merge branches with master: git merge branchname


Will reformat and add more as we learn.

