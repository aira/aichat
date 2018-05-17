#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Usage: tagRelease.sh <version_number> <summary_message>"
    exit 1
fi
git tag -a $1 -m "$2";
git push --tag;
