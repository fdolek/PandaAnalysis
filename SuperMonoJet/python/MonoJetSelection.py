from PandaCore.Tools.Misc import *
from re import sub

metTrigger='(trigger&1)!=0'
eleTrigger='(trigger&2)!=0'
phoTrigger='(trigger&4)!=0'

metFilter='metFilter==1'# && egmFilter==1'
presel = '!(nFatjet==1 && fj1Pt>200) && nJet>0 && jet1Pt>100 && abs(jet1Eta)<2.5 && nTau==0'

cuts = {
    'signal' : tAND(metFilter,tAND(presel,'nLooseLep==0 && nLooseElectron==0 && nLoosePhoton==0 && pfUmag>250 && dphipfmet>0.5')),
    'wmn'    : tAND(metFilter,tAND(presel,'nLoosePhoton==0 && nLooseLep==1 && nTightLep==1  && pfUWmag>250 && dphipfUW>0.5')),
    'wen'    : tAND(metFilter,tAND(presel,'nLoosePhoton==0 && nLooseLep==1 && nTightLep==1  && pfmet>50 && pfUWmag>250 && dphipfUW>0.5')),
    'zmm'    : tAND(metFilter,tAND(presel,'pfUZmag>250 && dphipfUZ>0.5 && nLooseElectron==0 && nLoosePhoton==0 && nLooseMuon==2 && nTightLep>0 && 60<diLepMass && diLepMass<120')),
    'zee'    : tAND(metFilter,tAND(presel,'pfUZmag>250 && dphipfUZ>0.5 && nLoosePhoton==0 && nLooseMuon==0 && nLooseElectron==2 && nTightLep>0 && 60<diLepMass && diLepMass<120')),
    'tme'    : tAND(metFilter,tAND(presel,'pfUWWmag>250 && dphipfUWW>0.5 && nLoosePhoton==0 && nLooseLep==2 && nTightLep==1 ')),
    'tem'    : tAND(metFilter,tAND(presel,'pfUWWmag>250 && dphipfUWW>0.5 && nLoosePhoton==0 && nLooseLep==2 && nTightLep==1 ')),
    'pho'    : tAND(metFilter,tAND(presel,'pfUAmag>250 && dphipfUA>0.5 && nLooseLep==0 && nLoosePhoton==1 && loosePho1IsTight==1 && fabs(loosePho1Eta)<1.4442')),
    }

for r in ['signal','zmm','zee','wmn','wen','tem','tme','pho']:
    cuts['monojet_'+r+'_0tag'] = tAND(cuts[r],'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==0')
    cuts['monojet_'+r+'_1tag'] = tAND(cuts[r],'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==1')
    cuts['monojet_'+r+'_2tag'] = tAND(cuts[r],'Sum$(jetCSV>0.8 && abs(jetEta)<2.5)==2')

weights = {
  'signal'         : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV*sf_metTrig',
  'control'        : '%f*sf_pu*sf_tt*normalizedWeight*sf_lepID*sf_lepIso*sf_lepTrack*sf_ewkV*sf_qcdV',
  'pho'            : '%f*sf_pu*normalizedWeight*sf_ewkV*sf_qcdV*sf_pho*sf_phoTrig *sf_qcdV2j', # add the additional 2-jet kfactor
}

for x in ['tme','tem','wmn','wen','zee','zmm','pho']:
	if 'en' in x or 'ee' in x:
	  weights[x] = tTIMES(weights['control'],'sf_eleTrig')
	elif 'em' in x or 'me' in x:
	  weights[x] = tTIMES(weights['control'],'sf_eleTrig*sf_metTrig')
	elif 'mn' in x or 'mm' in x:
	  weights[x] = tTIMES(weights['control'],'sf_metTrig')
	else:
	  weights[x] = tTIMES(weights['pho'],'sf_phoTrig')

for x in ['signal','tme','tem','wmn','wen','zee','zmm','pho']:
    weights['monojet_'+x+'_0tag'] = tTIMES(weights[x],'sf_btag0')
    weights['monojet_'+x+'_1tag'] = tTIMES(weights[x],'sf_btag1')
    weights['monojet_'+x+'_2tag'] = tTIMES(weights[x],'sf_btag2')

for x in ['signal','tme','tem','wmn','wen','zee','zmm','pho']:
    for y in ['0tag','1tag','2tag']:
        r = 'monojet_'+x+'_'+y
        for shift in ['BUp','BDown','MUp','MDown']:
            for cent in ['sf_btag']:
               weights[r+'_'+cent+shift] = sub(cent+'0',cent+'0'+shift,sub(cent+'1',cent+'1'+shift,sub(cent+'2',cent+'2'+shift,weights[r])))
