from PandaCore.Tools.Misc import *
from re import sub

eleTrigger='(trigger&2)!=0'
muTrigger='(trigger&8)!=0'

presel = 'nTau==0 && Sum$(jetPt>25)>0' #Need to check

cuts = {
    'nLep1' : tAND(presel,'nTightLep==1 && (nTightElectron + nTightMuon)==1 && mT>=160'),
    'nLep_e': tAND(presel,'nTightLep==1 && nTightElectron==1 && mT>=160'),
    'nLep_m': tAND(presel,'nTightLep==1 && nTightMuon==1 && mT>=160'),
    'nLep2' : tAND(presel,'nLooseLep==2 && mT>=160'),
    }

cuts['signal']   = tAND(nLep1,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==1')
cuts['wen']      = tAND(nLep_e,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==0')
cuts['wmn']      = tAND(nLep_m,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==0')
cuts['ttbar1e']  = tAND(nLep_e,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')
cuts['ttbar1m']  = tAND(nLep_m,'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')
cuts['ttbar2le'] = tAND(nLep2,'nTightMuon==1 && Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')
cuts['ttbar2lm'] = tAND(nLep2,'nTightElectron==1 && Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')

weights = {
    'signal'  : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag1',
    'wen'     : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag0',
    'wmn'     : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag0',
    'ttbar1e' : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag2',
    'ttbar1m' : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag2',
    'ttbar2le': '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag2',
    'ttbar2lm': '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_qcdTT*sf_btag2',
}

for x in ['signal','wmn','wen','ttbar1e','ttbar1m','ttbar2le','ttbar2lm']:
 for shift in ['BUp','BDown','MUp','MDown']:
  for cent in ['sf_btag']:
   weights[r+'_'+cent+shift] = sub(cent+'0',cent+'0'+shift,sub(cent+'1',cent+'1'+shift,sub(cent+'2',cent+'2'+shift,weights[r])))
