#!/bin/bash                                                                                                                                                                                                 
ANALYSIS=$1
REGION1=$2
REGION2=$3
FROMLIMIT=$4

source ../lpc_setup.sh $ANALYSIS $REGION1
python analysis.py --region $REGION2 --analysis $ANALYSIS $FROMLIMIT

