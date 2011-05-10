#!/bin/bash
for file in $(ls *.po); do
    fileLen=${#file}
    fileLang=${file:0:fileLen-3}
    dir="../../mj_res/locale/$fileLang/LC_MESSAGES"
    mkdir -p $dir
    msgfmt $file -o $dir/OGSMahjong.mo
done

