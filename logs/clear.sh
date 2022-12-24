#!/bin/sh

for i in *.log ; do
    if [ -f $i ]
    then
        rm -f $i
    fi
done

exit 0