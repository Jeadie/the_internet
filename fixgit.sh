#!/bin/bash
#
# An easy fix for all the times I accidentally commit with my work, and not my Github, git details.

git filter-branch -f --env-filter '
OLD_EMAIL="jeadi@amazon.com"
NEW_NAME="Jeadie"
NEW_EMAIL="jackeadie@duck.com"
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
  export GIT_COMMITTER_NAME="$NEW_NAME"
  export GIT_COMMITTER_EMAIL="$NEW_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
  export GIT_AUTHOR_NAME="$NEW_NAME"
  export GIT_AUTHOR_EMAIL="$NEW_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
