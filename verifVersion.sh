#!/bin/sh
path=`dirname $0`
GITCMD="git --git-dir=$path/.git --work-tree=$path"
`$GITCMD fetch origin`
UPSTREAM=${1:-'@{u}'}
LOCAL=$($GITCMD rev-parse @)
REMOTE=$($GITCMD rev-parse "$UPSTREAM")
BASE=$($GITCMD merge-base @ "$UPSTREAM")
echo PATH=$path
echo STATUS=`$GITCMD status`
echo LOCAL=$LOCAL
echo REMOTE=$REMOTE
echo BASE=$BASE
if [ $LOCAL = $REMOTE ]; then
    if [ -z "$LOCAL" ]; then
        echo "Problem with Git"
        ret="1"
    else
        echo "Up-to-date"
        ret="0"
    fi
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    ret="0"
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
    ret="0"
else
    echo "Diverged"
    ret="1"
fi
return "$ret"
