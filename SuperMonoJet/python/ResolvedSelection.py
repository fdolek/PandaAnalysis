from PandaCore.Tools.Misc import *
from re import sub


metTrigger='(trigger&1)!=0'
eleTrigger='(trigger&2)!=0'
phoTrigger='(trigger&4)!=0'


cuts = {}
weights = {}
triggers = {}

baseline = 'metFilter==1 && nTau==0 && bosonpt>150 && Sum$(jetPt>30)>1 && Sum$(jetPt>30)<4 && !(nFatjet==1 && fj1Pt>200)' 

#cuts for specific regions
cuts['signal'] = tAND(baseline,'nLooseLep==0 && nLooseElectron==0 && nLoosePhoton==0 && pfmet>250 && dphipfmet>0.4')
cuts['tm'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==1 && nTightMuon==1 && pfUWmag>250 && dphipfUW>0.4')
cuts['te'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==1 && nTightElectron==1 && pfUWmag>250 && dphipfUW>0.4 && pfmet>50')
cuts['wmn'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==1 && nTightMuon==1 && pfUWmag>250 && dphipfUW>0.4')
cuts['wen'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==1 && nTightElectron==1 && pfUWmag>250 && dphipfUW>0.4 && pfmet>50')
cuts['zmm'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==2 && nTightMuon==1 && pfUZmag>250 && dphipfUZ>0.4 && diLepMass>80 && diLepMass<100')
cuts['zee'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==2 && nTightElectron==1 && pfUZmag>250 && dphipfUZ>0.4 && diLepMass>80 && diLepMass<100')
cuts['pho'] = tAND(baseline,'(nLooseMuon+nLooseElectron+nTau)==0 && nLoosePhoton==1 && loosePho1IsTight==1 && pfUAmag>250 && dphipfUA>0.4')


for r in ['signal','zmm','zee','wen','wmn','pho']:
        cuts[r] = tAND(cuts[r],'Sum$(jetCSV>0.8484 && jetEta<2.5)==2')
        cuts[r+'_fail'] = tAND(cuts[r],'Sum$(jetCSV>0.8484 && jetEta<2.5)==0')

for r in ['tm','te']:
        cuts[r] = tAND(cuts[r],'Sum$(jetCSV>0.8484 && jetEta<2.5)==3')
        cuts[r+'_fail'] = tAND(cuts[r],'Sum$(jetCSV>0.8484 && jetEta<2.5)==1')

for r in ['signal','tm','te','zmm','zee','wen','wmn','pho']:
        cuts[r] = tAND(cuts[r],'min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])>0.8484')
        cuts[r+'_fail'] = tAND(cuts[r],'min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])<=0.8484')


#weights for specific regions
weights = {
   'base'  : '%f*normalizedWeight*sf_pu*sf_ewkV*sf_qcdV',
}

for x in ['signal','signal_fail']:
	  weights[x] = tTIMES(weights['base'],'%f*sf_metTrig*sf_tt')
        
for x in ['tm','te','wmn','wen','zmm','zee','tm_fail','te_fail','wmn_fail','wen_fail','zmm_fail','zee_fail']:
	if 'e' in x:
	  weights[x] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')
	else:
	  weights[x] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')

for x in ['pho','pho_fail']:
	  weights[x] = tTIMES(weights['base'],'%f*sf_phoTrig*1.0')

for x in ['wmn','wen','zmm','zee','wmn_fail','wen_fail','zmm_fail','zee_fail']:
	if 'fail' in x:
	  weights[x] = tTIMES(weights[x],'sf_btag0')
        else:
	  weights[x] = tTIMES(weights[x],'sf_btag2')
   
for x in ['tm','te','tm_fail','te_fail']:
	if 'fail' in x:
	  weights[x] = tTIMES(weights[x],'sf_btag1')
        else:
	  weights[x] = tTIMES(weights[x],'sf_btag3')


for r in ['signal','tm','te','wmn','wen','zmm','zee','signal_fail','tm_fail','te_fail','wmn_fail','wen_fail','zmm_fail','zee_fail']:
    for shift in ['BUp','BDown','MUp','MDown']:
        for cent in ['sf_btag']:
            if 'btag0' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'0',cent+'0'+shift,weights[r])
            if 'btag1' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'1',cent+'1'+shift,weights[r])
            if 'btag2' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'2',cent+'2'+shift,weights[r])
            if 'btag3' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'3',cent+'3'+shift,weights[r])
