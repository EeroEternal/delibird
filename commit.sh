#!/bin/bash
commit_msg=$1

git pull
git add .

if [ -z "$commit_msg" ]
then
    commit_message="update"
else
    commit_message=$commit_msg
fi

git commit -m "$commit_message"

git push
