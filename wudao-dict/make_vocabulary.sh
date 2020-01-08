#!/bin/bash

count=`ps -ef | grep "python3 WudaoServer.py" | grep -v "grep" | wc -l`

if [ $count == 0 ]; then
    nohup python3 WudaoServer.py > ./usr/server.log 2>&1 &
fi

for enfile in $1/*;
do
    python3 vocabulary.py $enfile ../vocabulary/learned_words.txt $1;
done
