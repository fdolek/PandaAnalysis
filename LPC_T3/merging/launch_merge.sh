#!/bin/bash                                                                                                                                                                                                 
ANALYSIS=$1

for REGION in met pho singleele singlemu diele dimu
do 
    source merge.sh $ANALYSIS $REGION
done

if [ $ANALYSIS = 'monojet' ]
then 
    source merge.sh monojet elemu
    source merge.sh monojet muele
fi