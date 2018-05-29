#!/usr/bin/env python

# imports and load libraries
from array import array
import glob
import fnmatch
from re import sub
import os
import sys
import subprocess
from argparse import ArgumentParser

import ROOT as root
from PandaCore.Tools.Misc import *
from PandaCore.Tools.Load import Load

parser = ArgumentParser(description='Parsing dataset folder')
parser.add_argument('--folder',type=str,default=None)
parser.add_argument('--panda',type=str,default="80X-v1")
parser.add_argument('--mit',type=bool,default=None)
parser.add_argument('--test',type=bool,default=None)
args = parser.parse_args()

outpath = "/uscms_data/d3/lpcmetx/"+args.panda+"/"
if args.test:
    outpath = "/uscms_data/d3/lpcmetx/test/"

xrd = "root://cmseos.fnal.gov/" 
inbase="/eos/uscms/store/group/lpcmetx/pandaprod/"+args.panda
if args.mit:
    xrd = "root://xrootd.cmsaf.mit.edu/"
    inbase="/store/user/paus/pandaf/009/"

xrdls = "xrdfs "+xrd+" ls "
folders = subprocess.check_output(xrdls+inbase,shell=True).split()

def scan(starting_path):
    if '.root' in starting_path:
        return [starting_path]
    elif '.' not in starting_path:
        for x in subprocess.check_output(xrdls+starting_path,shell=True).split():
            if '.root' in x:
                try:
                    rootfiles.append(x)
                except:
                    rootfiles = [x]
            elif '.' not in x:
                rootfiles = scan(x)
    try: 
        return rootfiles
    except:
        return

def runAll():
    for f in folders:
        split = f.split('/')
        folder =  split[-1]
        runOneFolder(folder)

def runOneFolder(folder):
    f=inbase+'/'+folder
    if f in folders:
        subprocess.Popen(['mkdir', '-p', outpath + folder])
        subfolders = subprocess.check_output(xrdls+f,shell=True).split()
        with open(outpath + folder +"/RawFiles.00","w") as f:
            for s in subfolders:
                for r in scan(s): 
                    print r
                    rootfile = root.TFile.Open(xrd+r)
                    tree = rootfile.Get("events")
                    nevents = tree.GetEntriesFast()
                    rootfile.Close()
                    print xrd + r + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1"
                    f.write(xrd + r + " " + str(nevents) + " " + str(nevents) + " 1 1 1 1" + '\n')
            f.close()


if not args.folder:
    print 'folder not specify, running over %s' %inbase
    runAll()
else:
    print 'folder is specified: %s' %args.folder
    runOneFolder(args.folder)
