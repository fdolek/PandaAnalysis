#!/usr/bin/env python

# imports and load libraries
from array import array
from glob import glob
from re import sub
from sys import argv,exit
import os
import sys
import subprocess
from os import environ,system,path,remove
from argparse import ArgumentParser

import ROOT as root
from PandaCore.Tools.Misc import *
from PandaCore.Tools.Load import Load

parser = ArgumentParser(description='Parsing dataset folder')
parser.add_argument('--folder',type=str,default=None)
args = parser.parse_args()

#inbase="/store/user/paus/pandaf/009/"
#inbase="/store/group/lpcmetx/pandaprod/80X-v1/Vector_MonoTop_Leptonic_NLO_Mphi_2500_Mchi_500_gSM_0p25_gDM_1p0_13TeV_madgraph/"
inbase="/store/group/lpcmetx/pandaprod/80X-v1/Vector_MonoTop_Leptonic_NLO_Mphi_2500_Mchi_500_gSM_0p25_gDM_1p0_13TeV_madgraph/Vector_MonoTop_Leptonic_NLO_Mphi_2500_Mchi_500_gSM_0p25_gDM_1p0_13TeV_madgraph/180521_171141/0000"
#inpath = 'xrdfs root://xrootd.cmsaf.mit.edu ls ' + inbase
inpath = 'xrdfs root://cmseos.fnal.gov ls ' + inbase
files = subprocess.check_output(inpath,shell=True)
file = files.split()

def runAll():
    for f in file:
        split = f.split('/')
        direc =  split[-1]
        print direc
        #path = "/uscms_data/d3/lpcmetx/catalog/80x-v1/"
        path = "/uscms_data/d3/lpcmetx/test-Diana/"
        os.makedirs(path + direc)

        #subfiles=subprocess.check_output("xrdfs root://xrootd.cmsaf.mit.edu ls "+f,shell=True)
        subfiles=subprocess.check_output("xrdfs root://cmseos.fnal.gov ls "+f,shell=True)
        subfile = subfiles.split()
        with open(path + direc +"/RawFiles.00","w") as f:
            for s in subfile:
                #rootfile = root.TFile.Open("root://xrootd.cmsaf.mit.edu/" + s)
                rootfile = root.TFile.Open("root://root://cmseos.fnal.gov" + s)
                tree = rootfile.Get("events")
                nevents = tree.GetEntriesFast()
                rootfile.Close()
                #print "root://xrootd.cmsaf.mit.edu/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1"
                print "root://cmseos.fnal.gov/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1"
                #f.write("root://xrootd.cmsaf.mit.edu/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1" + '\n')
                f.write("root://cmseos.fnal.gov/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1" + '\n')
            f.close()

def runOneFolder(folderName):
    f=inbase+'/'+folderName
    if f in file:
        split = f.split('/')
        direc =  split[-1]
        print direc
        path = "/uscms_data/d3/lpcmetx/test-Diana/"
        #path = "/uscms_data/d3/lpcmetx/catalog/80x-v1/"
        os.makedirs(path + direc)
        #subfiles=subprocess.check_output("xrdfs root://xrootd.cmsaf.mit.edu ls "+f,shell=True)
        subfiles=subprocess.check_output("xrdfs root://cmseos.fnal.gov ls "+f,shell=True)
        subfile = subfiles.split()
        with open(path + direc +"/RawFiles.00","w") as f:
            for s in subfile:
                #rootfile = root.TFile.Open("root://xrootd.cmsaf.mit.edu/" + s)
                rootfile = root.TFile.Open("root://cmseos.fnal.gov/" + s)
                tree = rootfile.Get("events")
                nevents = tree.GetEntriesFast()
                rootfile.Close()
                #print "root://xrootd.cmsaf.mit.edu/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1"
                print "root://cmseos.fnal.gov/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1"
                #f.write("root://xrootd.cmsaf.mit.edu/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1" + '\n')
                f.write("root://cmseos.fnal.gov/" + s + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1" + '\n')
            f.close()


if not args.folder:
    print 'folder not specify, running over %s' %inbase
    runAll()
else:
    print 'folder is specified: %s' %args.folder
    runOneFolder(args.folder)
