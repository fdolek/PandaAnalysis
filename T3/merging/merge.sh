#!/bin/bash 

#echo Diboson MET QCD SingleElectron SingleTop TTbar WJets ZJets ZtoNuNu | xargs -n 1 -P 10 python merge.py

#echo TTTo2L2Nu | xargs -n 1 -P 10 python merge.py

while read p; do
    echo $p  | xargs -n 1 -P 10 python merge.py
done <darkhiggs.txt

