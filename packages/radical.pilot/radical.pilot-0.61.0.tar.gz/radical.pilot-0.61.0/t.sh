#!/usr/bin/env python


branches=$(git for-each-ref --format="%(refname)" refs/heads)

# iterate through the commits, most recent first
for COMMIT in $(git log --pretty='tformat:%H'); do
    echo
    echo $COMMIT
    for BRANCH in $branches
    do
        printf '.'
        if (git log --pretty="format:%H" $BRANCH | fgrep -q COMMIT); then
            echo $BRANCH
            FOUND=true
        fi
    done
    if ! test -z "$FOUND"
    then
        break
    fi
done

