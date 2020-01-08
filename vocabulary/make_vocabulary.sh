#!/bin/bash

for enfile in *;
do
    python3 /opt/WuYoudao-dict/vocabulary.py $enfile;
done
