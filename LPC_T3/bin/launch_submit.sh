#!/bin/bash                                                                                                                                                                                                                                                                                                                                                                                                          
ANALYSIS=$1

for REGION in pho singleele singlemu diele dimu
# elemu muele
#for REGION in elemu muele
do
    source submit.sh $ANALYSIS $REGION
done