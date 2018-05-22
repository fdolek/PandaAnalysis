#!/usr/bin/env python
from re import sub
from math import *
from array import array
from sys import argv,exit
from os import path,getenv
import os
import ROOT as r
from glob import glob
import argparse
parser = argparse.ArgumentParser(description='make forest')
parser.add_argument('--region',metavar='region',type=str,default=None)
parser.add_argument('--input',metavar='input',type=str,default=getenv('PANDA_FLATDIR'))

args = parser.parse_args()
nddt = args.ddt
region = args.region  
#out_region = args.region
#region = out_region.split('_')[0]
if region=='test':
    is_test = True 
    region = 'signal'
else:
    is_test = False

argv=[]
import PandaAnalysis.Flat.fitting_forest as forest 
from PandaCore.Tools.Misc import *
import PandaCore.Tools.Functions # kinematics
#import PandaAnalysis.MonoX.MonoXSelection as sel
import PandaAnalysis.LeptonicMonoTop.LeptonicMonotopSelection as sel

basedir = args.input
lumi = 35900

def f(x):
    return basedir + x + '.root'

def shift_btags(additional=None):
    shifted_weights = {}
    #if not any([x in region for x in ['signal','top','w']]):
    #    return shifted_weights 
    for shift in ['BUp','BDown','MUp','MDown']:
        for cent in ['sf_btag']:
            shiftedlabel = ''
            if 'sj' in cent:
                shiftedlabel += 'sj'
            if 'B' in shift:
                shiftedlabel += 'btag'
            else:
                shiftedlabel += 'mistag'
            if 'Up' in shift:
                shiftedlabel += 'Up'
            else:
                shiftedlabel += 'Down'
            weight = sel.weights[region+'_'+cent+shift]%lumi
            if additional:
                weight = tTIMES(weight,additional)
            shifted_weights[shiftedlabel] = weight
    return shifted_weights

#vmap definition
vmap = {}
#mc_vmap = {‘genBosonPt’:‘genBosonPt’}
vmap[‘mt’] = ‘mT’

#weights
weights = {'nominal' : sel.weights[region]%lumi}
weights.update(shift_btags())

factory = forest.RegionFactory(name = region if not(is_test) else 'test',
                               cut = sel.cuts[region],
                               variables = vmap, 
                               mc_variables = mc_vmap, 
                               mc_weights = weights)

#Process and creation of new ntuples process


elif 'signal' not in region:
    factory.add_process(f('ZJets'),'Zll')
    factory.add_process(f('WJets'),'Wlv')
    factory.add_process(f('SingleTop'),'ST')
    factory.add_process(f('Diboson'),'Diboson')
    factory.add_process(f('QCD'),'QCD')
    factory.add_process(f('TTbar'),'ttbar')

    if 'zee' in region or 'te' in region or 'wen' in region:
        factory.add_process(f('SingleElectron'),'Data',is_data=True,extra_cut=sel.eleTrigger)

    if 'zmm' in region or 'tm' in region or 'wmn' in region:
        factory.add_process(f('MET'),'Data',is_data=True,extra_cut=sel.metTrigger)
	

forestDir = basedir + '/limits/'
os.system('mkdir -p %s'%(forestDir))
factory.run(forestDir+'/fittingForest_%s.root'%region)

