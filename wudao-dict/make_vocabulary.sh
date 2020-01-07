#!/bin/bash
count=`ps -ef | grep "python3 WudaoServer.py" | grep -v "grep" | wc -l`

save_path=$PWD
 
if [ $count == 0 ]; then
    cd /opt/WuYoudao-dict/wudao-dict
    nohup python3 WudaoServer.py > ./usr/server.log 2>&1 &
    cd $save_path
fi

for enfile in 20*.txt;
do
    python3 /opt/WuYoudao-dict/wudao-dict/vocabulary.py $enfile /opt/WuYoudao-dict/vocabulary/learned_words.txt;
done
