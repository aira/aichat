#!/bin/bash
if [ $# -eq 0 ]; then
    echo "No branch name provided. Provide a branch name to delete it"
    exit 1
fi
read -p "Are you sure you want to delete branch $1? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    git push -d origin $1;
    git branch -d $1;
fi
