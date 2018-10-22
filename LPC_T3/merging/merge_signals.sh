#!/bin/bash                                                                                                                                                                                               

ANALYSIS=$1
#REGION=$2

source ../lpc_setup.sh $ANALYSIS monotop

echo $ANALYSIS 


while read p; do
    echo $p  | xargs -n 1 -P 10 python merge.py
done <monotop_sig.txt
