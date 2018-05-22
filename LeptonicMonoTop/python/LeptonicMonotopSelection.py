from PandaCore.Tools.Misc import *
from re import sub

eleTrigger='(trigger&2)!=0'
muTrigger='(trigger&8)!=0'

presel = 'nTau==0 && Sum$(jetPt>25)>0' #Need to check

cuts = {
    'nLep1': tAND(presel,'nTightLep==1 && (nTightElectron + nTightMuon)==1 && mT>=160'),
    'nLep2' : tAND(presel,'nTightLep==2 && mT>=160'),
    }

cuts['wjets'] = tAND(nLep1,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==0')
cuts['signal'] = tAND(nLep1,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==1')
cuts['ttbar1l'] = tAND(nLep1,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')
cuts['ttbar2l'] = tAND(nLep2,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')

weights = {
    'signal': '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag1',
    'wjets' : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag0',
    'ttbar1l' : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag2',
    'ttbar2l': '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag2',
}




