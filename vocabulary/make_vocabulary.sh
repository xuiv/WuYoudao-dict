#!/bin/bash

for enfile in 20*.txt;
do
    timeout 180 python3 /opt/WuYoudao-dict/vocabulary.py $enfile;
done
