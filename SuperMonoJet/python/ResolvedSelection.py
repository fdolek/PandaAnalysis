from PandaCore.Tools.Misc import *
from re import sub


metTrigger='(trigger&1)!=0'
eleTrigger='(trigger&2)!=0'
phoTrigger='(trigger&4)!=0'


cuts = {}
weights = {}
triggers = {}

baseline = 'metFilter==1 && nTau==0 && bosonpt>150 && Sum$(jetPt>30)>1 && Sum$(jetPt>30)<4 && !(nFatjet==1 && fj1Pt>200 && puppimet>200)' 

#cuts for specific regions
cuts['signal'] = tAND(baseline,'nLooseLep==0 && nLooseElectron==0 && nLoosePhoton==0 && puppimet>170 && dphipuppimet>0.4 && Sum$(jetCSV>0.8484 && jetEta<2.5)==2 && min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])>0.8484')
cuts['tm'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==1 && nTightMuon==1 && puppiUWmag>170 && dphipuppiUW>0.4 && Sum$(jetCSV>0.8484 && jetEta<2.5)==2 && min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])>0.8484')
cuts['te'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==1 && nTightElectron==1 && puppiUWmag>170 && dphipuppiUW>0.4 && Sum$(jetCSV>0.8484 && jetEta<2.5)==2 && min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])>0.8484 && puppimet>50')
cuts['wmn'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==1 && nTightMuon==1 && puppiUWmag>170 && dphipuppiUW>0.4 && Sum$(jetCSV>0.5426 && jetEta<2.5)==2 && max(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])<0.8484 && min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])>0.5426')
cuts['wen'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==1 && nTightElectron==1 && puppiUWmag>170 && dphipuppiUW>0.4 && Sum$(jetCSV>0.5426 && jetEta<2.5)==2 && max(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])<0.8484 && min(jetCSV[bosonjtidx[0]],jetCSV[bosonjtidx[1]])>0.5426 && puppimet>50')
cuts['zmm'] = tAND(baseline,'(nLooseElectron+nLoosePhoton+nTau)==0 && nLooseMuon==2 && nTightMuon==1 && puppiUZmag>170 && dphipuppiUZ>0.4 && diLepMass>80 && diLepMass<100')
cuts['zee'] = tAND(baseline,'(nLooseMuon+nLoosePhoton+nTau)==0 && nLooseElectron==2 && nTightElectron==1 && puppiUZmag>170 && dphipuppiUZ>0.4 && diLepMass>80 && diLepMass<100')
cuts['pho'] = tAND(baseline,'(nLooseMuon+nLooseElectron+nTau)==0 && nLoosePhoton==1 && loosePho1IsTight==1 && puppiUAmag>170 && dphipuppiUA>0.4')

#weights for specific regions
weights['base'] = 'normalizedWeight*sf_pu*sf_ewkV*sf_qcdV'
weights['signal'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_tt')
weights['tm'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')
weights['te'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepTrack*sf_tt')
weights['wmn'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')
weights['wen'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')
weights['zmm'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')
weights['zee'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt')
weights['pho'] = tTIMES(weights['base'],'%f*sf_phoTrig*1.0')

'''
for r in ['signal','wmn','wen','tm','te','zmm','zee','pho']:
    print r
    for shift in ['BUp','BDown','MUp','MDown']:
        for cent in ['sf_btag']:
            if 'btag0' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'0',cent+'0'+shift,weights[r])
#                print weights[r+'_'+cent+shift]
            if 'btag1' in weights[r]:
                weights[r+'_'+cent+shift] = sub(cent+'1',cent+'1'+shift,weights[r])
#                print weights[r+'_'+cent+shift]
'''
for r in ['signal','wmn','wen','tm','te','zmm','zee','pho']:
    for shift in ['ScaleUp','ScaleDown','PDFUp','PDFDown']:
        if shift == 'ScaleUp':
            weights[r+'_'+shift] = weights[r] + "*(scale[3]+1)"
        if shift == 'ScaleDown':
            weights[r+'_'+shift] = weights[r] + "*(scale[5]+1)"
        if shift == 'PDFUp':
            weights[r+'_'+shift] = weights[r] + "*pdfUp"
        if shift == 'PDFDown':
            weights[r+'_'+shift] = weights[r] + "*pdfDown"
     
'''            
weights['zmm_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfUp')
weights['zmm_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfDown')
weights['zmm_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[3]+1)')
weights['zmm_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[5]+1)')
weights['zee_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfUp')
weights['zee_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfDown')
weights['zee_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[3]+1)')
weights['zee_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[5]+1)')
weights['wmn_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfUp')
weights['wmn_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfDown')
weights['wmn_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[3]+1)')
weights['wmn_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[5]+1)')
weights['wen_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfUp')
weights['wen_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*pdfDown')
weights['wen_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[3]+1)')
weights['wen_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag0*(scale[5]+1)')

weights['pho_fail_PDFUp'] = tTIMES(weights['base'],'%f*sf_phoTrig*sf_btag0*1.0*pdfUp')
weights['pho_fail_PDFDown'] = tTIMES(weights['base'],'%f*sf_phoTrig*sf_btag0*1.0*pdfDown')
weights['pho_fail_ScaleUp'] = tTIMES(weights['base'],'%f*sf_phoTrig*sf_btag0*1.0*(scale[3]+1)')
weights['pho_fail_ScaleDown'] = tTIMES(weights['base'],'%f*sf_phoTrig*sf_btag0*1.0*(scale[5]+1)')

weights['tm_fail_PDFUp']     =  tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag1*pdfUp')
weights['tm_fail_PDFDown']   =  tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag1*pdfDown')
weights['tm_fail_ScaleUp']   =  tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag1*(scale[3]+1)')
weights['tm_fail_ScaleDown'] =  tTIMES(weights['base'],'%f*sf_metTrig*sf_lepID*sf_lepIso*sf_lepTrack*sf_tt*sf_btag1*(scale[5]+1)')

weights['te_fail_PDFUp']     =  tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepTrack*sf_tt*sf_btag1*pdfUp')
weights['te_fail_PDFDown']   =  tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepTrack*sf_tt*sf_btag1*pdfDown')
weights['te_fail_ScaleUp']   =  tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepTrack*sf_tt*sf_btag1*(scale[3]+1)')
weights['te_fail_ScaleDown'] =  tTIMES(weights['base'],'%f*sf_eleTrig*sf_lepID*sf_lepTrack*sf_tt*sf_btag1*(scale[5]+1)')

'''
