#!/bin/bash

if [ -e darkhiggs.txt ];then
    rm darkhiggs.txt
fi

for l in `ls /eos/uscms/store/user/lpcmetx/pandaprod/80X_monoz`
do
    file=`(echo $l | awk -F "_gSM" '{print $1}' | awk -F "_LO_" '{print $1"_"$2}')`
    ((var+=1))
    echo $var
    if [ $var -eq 1 ];then
	echo $file > darkhiggs.txt
    else
	echo $file >> darkhiggs.txt
    fi
done