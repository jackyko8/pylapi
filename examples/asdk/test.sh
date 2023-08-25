#!/bin/bash

script_path=$(dirname $0)

# if [ -z "$ASDK_AUTH" ]; then
#     echo ASDK_AUTH is not defined.
#     exit 1
# fi

num=0
for ii in \
    get-user-task-list \
    list-projects-tasks-user \
    list-projects \
    list-sections-for-project \
    list-tags \
    list-teams \
    list-users \
    load-project \
    load-task \
    load-user-task-list \
    ; do
    num=$[num+1]
    echo "$num. $ii BEGINS --------------------"
    python $script_path/$ii.py
    RET=$?
    if [ "$RET" -ne 0 ]; then
        echo ERROR in $ii.py
        exit $RET
    fi
    echo "$num. $ii ENDS   --------------------"
done
echo "============================================================"
echo $num tests completed
