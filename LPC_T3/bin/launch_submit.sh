#!/bin/bash                                                                                                                                                                                                                                                                                                                                                                                                          
ANALYSIS=$1

for REGION in met pho singleele singlemu diele dimu
do
    source submit.sh $ANALYSIS $REGION
done

if [ $ANALYSIS = 'monojet' ]
then
    source submit.sh monojet elemu
    source submit.sh monojet muele
fi