#!/usr/bin/env python

from os import system,getenv
from sys import argv
import argparse,sys

parser = argparse.ArgumentParser(description='plot stuff')

parser.add_argument('--bdtcut',type=float,default=None)
parser.add_argument('--masscut1',type=float,default=None)
parser.add_argument('--masscut2',type=float,default=None)
parser.add_argument('--tt',metavar='tt',type=str,default='')
parser.add_argument('--cut',metavar='cut',type=str,default='1==1')
parser.add_argument('--outdir',metavar='outdir',type=str,default='.')
parser.add_argument('--region',metavar='region',type=str,default=None)
parser.add_argument('--analysis',metavar='analysis',type=str,default=None)
parser.add_argument('--fromlimit',action='store_true',help='enable direct plotting from fitting ntuple')

args  = parser.parse_args()
region= args.region

sname = argv[0]
argv=[]

lumi    =   35800.
blind   =   False
SIGNAL  =   False

import ROOT as root
root.gROOT.SetBatch()
from PandaCore.Tools.Misc import *
import PandaCore.Tools.Functions
from PandaCore.Drawers.plot_utility import *
import PandaAnalysis.LeptonicMonoTop.LeptonicMonotopSelection as sel

### SET GLOBAL VARIABLES ###
if not args.fromlimit:
    baseDir = '/uscms_data/d3/fdolek/panda/80X-v1.6/lep_monotop/flat/'
    dataDir = baseDir
    ### DEFINE REGIONS ###
    cut = tAND(sel.cuts[args.region],args.cut)
else:
    baseDir = '/uscms_data/d3/fdolek/panda/80X-v1.6/lep_monotop/flat/'
    dataDir = baseDir
    cut = '1==1'

print "PLOTTER: input directory is:", baseDir

if args.bdtcut:
    cut = tAND(cut,'top_ecf_bdt>%f'%args.bdtcut)
if args.masscut1 and args.masscut2:
    cut = tAND(cut,'fj1MSD>%f'%args.masscut1)
    cut = tAND(cut,'fj1MSD<%f'%args.masscut2)
if args.masscut1:
    cut = tAND(cut,'fj1MSD>%f'%args.masscut1)

### LOAD PLOTTING UTILITY ###
plot = PlotUtility()
plot.Stack(True)
plot.Ratio(True)
plot.FixRatio(0.4)
if 'qcd' in region:
    plot.FixRatio(1)
plot.SetTDRStyle()
plot.InitLegend()
plot.cut = cut
plot.DrawMCErrors(True)
plot.AddCMSLabel()
plot.SetEvtNum("eventNumber")
plot.SetLumi(lumi/1000)
plot.AddLumiLabel(True)
plot.do_overflow = True
plot.do_underflow = True

if args.bdtcut:
    plot.AddPlotLabel('BDT > %.2f'%args.bdtcut,.18,.7,False,42,.04)

if args.masscut1 and args.masscut2:
    plot.AddPlotLabel('%i GeV < m_{SD} < %i GeV'%(int(args.masscut1),int(args.masscut2)),.18,.7,False,42,.04)

def f(x):
    return dataDir + 'fittingForest_' + x + '.root'

def normalPlotting(region):

    print 'Plotting from PandaAnalyzed  ntuple: ',region, ' region'
    region=region
    weight = sel.weights[region]%lumi
    plot.mc_weight = weight

    PInfo('cut',plot.cut)
    PInfo('weight',plot.mc_weight)

    #plot.add_systematic('QCD scale','scaleUp','scaleDown',root.kRed+2)
    #plot.add_systematic('PDF','pdfUp','pdfDown',root.kBlue+2)

    ### DEFINE PROCESSES ###
    zjets         = Process('Z+jets',root.kZjets,None,root.kCyan-9)
    wjets         = Process('W+jets',root.kWjets,None,root.kGreen-10)
    ttbar1l       = Process('t#bar{t} 1l',root.kTTbar1l,None,root.kOrange-3)
    ttbar2l       = Process('t#bar{t} 2l',root.kTTbar2l,None,root.kOrange-5)
    singletop     = Process('Single t',root.kST,None,root.kRed-9)
    qcd           = Process("QCD",root.kQCD,None,root.kMagenta-10)
    diboson       = Process('Diboson',root.kDiboson,None,root.kYellow-9)
    data          = Process("Data",root.kData)
    signal        = Process('m_{#phi}=1750.0 TeV, m_{#chi}=400 GeV',root.kSignal)

    processes = []

    if 'signale' in region:
       # processes = [wjets,zjets,ttbar1l,ttbar2l,singletop,qcd,diboson]       
        processes = [qcd,diboson,singletop,ttbar2l,ttbar1l,zjets,wjets]
        wjets.add_file          (baseDir+'WJets.root')
        zjets.add_file          (baseDir+'ZJets.root')
        ttbar1l.add_file        (baseDir+'TTbar_L.root')
        ttbar2l.add_file        (baseDir+'TTbar_2L.root')
        singletop.add_file      (baseDir+'SingleTop.root')
        qcd.add_file            (baseDir+'QCD.root')
        diboson.add_file        (baseDir+'Diboson.root')

    if 'signalm' in region:
        processes = [qcd,diboson,singletop,ttbar2l,ttbar1l,zjets,wjets]
        wjets.add_file          (baseDir+'WJets.root')
        zjets.add_file          (baseDir+'ZJets.root')
        ttbar1l.add_file        (baseDir+'TTbar_L.root')
        ttbar2l.add_file        (baseDir+'TTbar_2L.root')
        singletop.add_file      (baseDir+'SingleTop.root')
        qcd.add_file            (baseDir+'QCD.root')
        diboson.add_file        (baseDir+'Diboson.root')        
       
    if 'tee' in region or 'tmm' in region:    
        processes = [qcd,diboson,singletop,wjets,ttbar2l,ttbar1l,zjets]
        zjets.add_file          (baseDir+'ZJets.root')
	ttbar1l.add_file        (baseDir+'TTbar_L.root')
	ttbar2l.add_file        (baseDir+'TTbar_2L.root')
	wjets.add_file          (baseDir+'WJets.root')
        singletop.add_file      (baseDir+'SingleTop.root')
        diboson.add_file        (baseDir+'Diboson.root')
        qcd.add_file            (baseDir+'QCD.root')        
       
    if 'ten' in region or 'tmn' in region:    
        processes = [qcd,diboson,singletop,zjets,wjets,ttbar2l,ttbar1l]
        wjets.add_file          (baseDir+'WJets.root')
        zjets.add_file          (baseDir+'ZJets.root')
        ttbar1l.add_file        (baseDir+'TTbar_L.root')
        ttbar2l.add_file        (baseDir+'TTbar_2L.root')
        singletop.add_file      (baseDir+'SingleTop.root')
        qcd.add_file            (baseDir+'QCD.root')
        diboson.add_file        (baseDir+'Diboson.root') 

    if 'wen' in region or 'wmn' in region:	
	processes = [qcd,diboson,singletop,zjets,ttbar2l,ttbar1l,wjets]
	wjets.add_file          (baseDir+'WJets.root')
	zjets.add_file          (baseDir+'ZJets.root')
	ttbar1l.add_file        (baseDir+'TTbar_L.root')
	ttbar2l.add_file        (baseDir+'TTbar_2L.root')
	singletop.add_file      (baseDir+'SingleTop.root')
	qcd.add_file            (baseDir+'QCD.root')
	diboson.add_file        (baseDir+'Diboson.root') 


        #qcd.add_file(baseDir+'SingleTop.root')
        #qcd.additional_cut = sel.muTrigger
        #qcd.use_common_weight = False
        #qcd.additional_weight = 'sf_phoPurity'
    
    if any([x in region for x in ['signalm','wmn','tmm','tmn']]):
	if not blind:
	   data.additional_cut = sel.muTrigger
        data.add_file(dataDir+'SingleMuon.root')
        #data.additional_cut = sel.metTrigger
        lep='#mu'
    elif any([x in region for x in ['signale','wen','tee','ten']]):
	if not blind:
	   data.additional_cut = sel.eleTrigger
        data.add_file(dataDir+'SingleElectron.root')
        lep='e'   
 
    if not blind:	
        processes.append(data)
    if 'signale' in region  or 'signalm' in region:
 	SIGNAL=True
        signal.add_file(baseDir+'Vector_MonoTop_Leptonic_Mphi_1750_Mchi_1.root')
        processes.append(signal)
    #    #processes.append(signal1)

    for p in processes:
       #print "processess considered -> ", p
        plot.add_process(p)

    recoilBins = [100,200,300,400,500,600,700,1000]
    nRecoilBins = len(recoilBins)-1

    ### CHOOSE DISTRIBUTIONS, LABELS ###
    if 'signale' in region or 'signalm' in region or 'tee' in region or 'tmm' in region or 'ten' in region or 'tmn' in region or 'wen' in region or 'wmn' in region: 
        recoil=VDistribution("pfmet",recoilBins,"PF MET [GeV]","Events/GeV")
        #plot.add_distribution(FDistribution('dphipfmet',0,3.14,10,'min#Delta#phi(AK4 jet,E_{T}^{miss})','Events'))
    #elif any([x in region for x in ['wen','wmn','ten','tmn']]):
    #    recoil=VDistribution("pfUWmag",recoilBins,"PF U(%s) [GeV]"%(lep),"Events/GeV")
        plot.add_distribution(FDistribution('mT',0,500,25,'Transverse Mass of W [GeV]','Events'))
        if not lep=="e":
            plot.add_distribution(FDistribution('muonPt[0]',-10,800,30,'Leading %s p_{T} [GeV]'%lep,'Events/25 GeV'))
            plot.add_distribution(FDistribution('muonEta[0]',-2.7,2.7,15,'%s #eta'%lep,'Events'))
        else:
            plot.add_distribution(FDistribution('electronPt[0]',-10,800,30,'Leading %s p_{T} [GeV]'%lep,'Events/25 GeV'))
            plot.add_distribution(FDistribution('electronEta[0]',-2.7,2.7,15,'%s #eta'%lep,'Events'))
        #plot.add_distribution(FDistribution('dphipfUW',0,3.14,10,'min#Delta#phi(AK4 jet,E_{T}^{miss})','Events'))
        #plot.add_distribution(FDistribution('jetNMBtags',0,5,5,'nmbtag jets','Events'))
        #plot.add_distribution(FDistribution('jetNBtags',0,5,5,'nbtag jets','Events'))
        
    #recoil.calc_chi2 = True
    plot.add_distribution(recoil)


    plot.add_distribution(FDistribution("1",0,2,1,"dummy","dummy"))
    system('mkdir -p %s/%s/%s' %(args.outdir,args.analysis,region))
    plot.draw_all(args.outdir+'/'+args.region+'/')

def fromLimit(region):
    region=region
    print 'Plotting from fitting ntuple: ',region, ' region'
    #znunu = Process('Z(#nu#nu)+jets',root.kZjets,'Zvv_'+region,root.kCyan-9)
    zjets         = Process('Z+jets',root.kZjets,'Zll_'+region,root.kCyan-9)
    wjets         = Process('W+jets',root.kWjets,'Wlv_'+region,root.kGreen-10)
    ttbar1l       = Process('t#bar{t} 1l',root.kTTbar1l,None,root.kOrange-3)
    ttbar2l       = Process('t#bar{t} 2l',root.kTTbar2l,None,root.kOrange-5)
    singletop     = Process('Single t',root.kST,'ST_'+region,root.kRed-9)
    qcd           = Process('QCD',root.kQCD,'QCD_'+region,root.kMagenta-10)
    diboson       = Process('Diboson',root.kDiboson,'Diboson_'+region,root.kYellow-9)
    data          = Process("Data",root.kData,'Data_'+region)
    signal        = Process('m_{Zp}=1.0 TeV,m_{h}=90 GeV, m_{#chi}=400 GeV',root.kSignal)
    
    processes = [wjets,zjets,ttbar1l,ttbar2l,singletop,qcd,diboson]
    if 'signale' in region:
        processes = [wjets,zjets,ttbar1l,ttbar2l,singletop,qcd,diboson]       
    if 'signalm' in region:
        processes = [wjets,zjets,ttbar1l,ttbar2l,singletop,qcd,diboson]
    if 'tee' in region or 'tmm' in region:    
        processes = [zjets,ttbar2l,singletop,diboson]
    if 'ten' in region or 'tmn' in region or 'wen' in region or 'wmn' in region:    
        processes = [wjets,zjets,ttbar1l,singletop,qcd,diboson]

    for p in processes:
        p.add_file(f(region))
        p.additional_weight='weight'
        plot.add_process(p)

    #Inclusion of data
    data.add_file(f(region))
    data.additional_weight='weight'
    processes.append(data)
    plot.add_process(data)
    recoilBins = [100,200,300,400,500,600,700,1000]
    nRecoilBins = len(recoilBins)-1

    plot.add_distribution(FDistribution('mT',0,500,25,'Transverse Mass of W [GeV]','Events'))
    plot.add_distribution(recoil)

    system('mkdir -p %s/%s/' %(args.outdir,region))
    plot.draw_all(args.outdir+'/'+region+'/')

if not args.fromlimit:
    normalPlotting(region)
else:
    fromLimit(region)


