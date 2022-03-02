import os
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # inclusive BDT Training 0j merged
configurations = os.path.dirname(configurations) # Merged Training 
configurations = os.path.dirname(configurations) # FullRunII
configurations = os.path.dirname(configurations) # WW
configurations = os.path.dirname(configurations) # Configurations


from LatinoAnalysis.Tools.commonTools import getSampleFiles, getBaseWnAOD, getBaseW, addSampleWeight
def nanoGetSampleFiles(inputDir, sample):
    try:
        if _samples_noload:
            return []
    except NameError:
        pass

    return getSampleFiles(inputDir, sample, True, 'nanoLatino_')
	
# samples

try:
    len(samples)
except NameError:
    import collections
    samples = collections.OrderedDict()


################################################
################# SKIMS ########################
################################################

mcProduction_2016 = 'Summer16_102X_nAODv7_Full2016v7'
mcSteps_2016 = 'MCl1loose2016v7__MCCorr2016v7__l2loose__l2tightOR2016v7{var}'

mcProduction_2017 = 'Fall2017_102X_nAODv7_Full2017v7'
mcSteps_2017 = 'MCl1loose2017v7__MCCorr2017v7__l2loose__l2tightOR2017v7{var}'

mcProduction_2018 = 'Autumn18_102X_nAODv7_Full2018v7'
mcSteps_2018 = 'MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7{var}'

##############################################
###### Tree base directory for the site ######
##############################################

SITE=os.uname()[1]
if    'iihe' in SITE:
  treeBaseDir = '/pnfs/iihe/cms/store/user/xjanssen/HWW2015'
elif  'cern' in SITE:
  treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'

def makeMCDirectory_2016(var=''):
    if var:
        return os.path.join(treeBaseDir, mcProduction_2016, mcSteps_2016.format(var='__' + var))
    else:
        return os.path.join(treeBaseDir, mcProduction_2016, mcSteps_2016.format(var=''))
		
def makeMCDirectory_2017(var=''):
    if var:
        return os.path.join(treeBaseDir, mcProduction_2017, mcSteps_2017.format(var='__' + var))
    else:
        return os.path.join(treeBaseDir, mcProduction_2017, mcSteps_2017.format(var=''))
		
def makeMCDirectory_2018(var=''):
    if var:
        return os.path.join(treeBaseDir, mcProduction_2018, mcSteps_2018.format(var='__' + var))
    else:
        return os.path.join(treeBaseDir, mcProduction_2018, mcSteps_2018.format(var=''))

mcDirectory_2016 = makeMCDirectory_2016()
mcDirectory_2017 = makeMCDirectory_2017()
mcDirectory_2018 = makeMCDirectory_2018()

################################################
############### Lepton WP ######################
################################################

eleWP_2016 = 'mva_90p_Iso2016_tthmva_70'
muWP_2016 = 'cut_Tight80x_tthmva_80'

eleWP_2017 = 'mvaFall17V1Iso_WP90_tthmva_70'	
muWP_2017 = 'cut_Tight_HWWW_tthmva_80'

eleWP_2018 = 'mvaFall17V1Iso_WP90_tthmva_70'
muWP_2018 = 'cut_Tight_HWWW_tthmva_80'

LepWPCut_2016 = 'LepCut2l__ele_' + eleWP_2016 + '__mu_' + muWP_2016
LepWPCut_2017 = 'LepCut2l__ele_' + eleWP_2017 + '__mu_' + muWP_2017
LepWPCut_2018 = 'LepCut2l__ele_' + eleWP_2018 + '__mu_' + muWP_2018

################################################
############### b-tag WP ######################
################################################

btagWP = '0.4941' # Medium WP for 2017 DeepCSV

bVeto = 'Sum$(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Jet_btagDeepB[CleanJet_jetIdx] > '+btagWP+') == 0'
bVetoSF = 'TMath::Exp(Sum$(TMath::Log((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Jet_btagSF_deepcsv_shape[CleanJet_jetIdx]+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'
bReq = 'Sum$(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Jet_btagDeepB[CleanJet_jetIdx] > '+btagWP+') >= 1'
bReqSF = 'mtw2>30 && mll>50 && ((Sum$(CleanJet_pt > 30.) == 0 && !bVeto) || bReq)'
topcr = 'mtw2>30 && mll>50 && ((Sum$(CleanJet_pt > 30.) == 0 && !bVeto) || bReq)'
btagSF = '(bVeto || (topcr && Sum$(CleanJet_pt > 30.) == 0))*bVetoSF + (topcr && Sum$(CleanJet_pt > 30.) > 0)*bReqSF'

################################################
############ BASIC MC WEIGHTS ##################
################################################

Jet_PUIDSF = 'TMath::Exp(Sum$((Jet_jetId>=2)*TMath::Log(Jet_PUIDSF_loose)))'

SFweight_2016 = ' * '.join(['SFweight2l', LepWPCut_2016, 'LepSF2l__ele_' + eleWP_2016 + '__mu_' + muWP_2016, btagSF , 'PrefireWeight', Jet_PUIDSF]) 
SFweight_2017 = ' * '.join(['SFweight2l', LepWPCut_2017, 'LepSF2l__ele_' + eleWP_2017 + '__mu_' + muWP_2017, btagSF , 'PrefireWeight', Jet_PUIDSF])
SFweight_2018 = ' * '.join(['SFweight2l', LepWPCut_2018, 'LepSF2l__ele_' + eleWP_2018 + '__mu_' + muWP_2018, btagSF , Jet_PUIDSF])

PromptGenLepMatch2l = 'Alt$(Lepton_promptgenmatched[0]*Lepton_promptgenmatched[1], 0)'

mcCommonWeight_2016 = 'XSWeight*' + SFweight_2016 + '*' + PromptGenLepMatch2l + '*METFilter_MC'
mcCommonWeight_2017 = 'XSWeight*' + SFweight_2017 + '*' + PromptGenLepMatch2l + '*METFilter_MC'
mcCommonWeight_2018 = 'XSWeight*' + SFweight_2018 + '*' + PromptGenLepMatch2l + '*METFilter_MC'

###########################################
#############  BACKGROUNDS  ###############
###########################################

###### Top #######

#xxxxxxx 2016 xxxxxxx
files = nanoGetSampleFiles(mcDirectory_2016, 'TTJets_DiLept') + \
    nanoGetSampleFiles(mcDirectory_2016, 'TTJets_DiLept_ext1') + \
    nanoGetSampleFiles(mcDirectory_2016, 'ST_s-channel') + \
    nanoGetSampleFiles(mcDirectory_2016, 'ST_t-channel_antitop') + \
    nanoGetSampleFiles(mcDirectory_2016, 'ST_t-channel_top') + \
    nanoGetSampleFiles(mcDirectory_2016, 'ST_tW_antitop') + \
    nanoGetSampleFiles(mcDirectory_2016, 'ST_tW_top')

samples['top_2016'] = {
    'name': files,
    'weight': mcCommonWeight_2016,
    'FilesPerJob': 4,
}

Top_pTrw_2016 = '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) * (TMath::Sqrt(TMath::Exp(1.61468e-03 + 3.46659e-06*topGenPt - 8.90557e-08*topGenPt*topGenPt) * TMath::Exp(1.61468e-03 + 3.46659e-06*antitopGenPt - 8.90557e-08*antitopGenPt*antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)'

addSampleWeight(samples,'top_2016','TTJets_DiLept',Top_pTrw_2016)

#xxxxxxx 2017 xxxxxxx
files = nanoGetSampleFiles(mcDirectory_2017, 'TTTo2L2Nu') + \
    nanoGetSampleFiles(mcDirectory_2017, 'ST_s-channel') + \
    nanoGetSampleFiles(mcDirectory_2017, 'ST_t-channel_antitop') + \
    nanoGetSampleFiles(mcDirectory_2017, 'ST_t-channel_top') + \
    nanoGetSampleFiles(mcDirectory_2017, 'ST_tW_antitop') + \
    nanoGetSampleFiles(mcDirectory_2017, 'ST_tW_top')

samples['top_2017'] = {
    'name': files,
    'weight': mcCommonWeight_2017,
    'FilesPerJob': 1,
}

Top_pTrw_2017 = '((topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.))'

addSampleWeight(samples,'top_2017','TTTo2L2Nu',Top_pTrw_2017)

#xxxxxxx 2018 xxxxxxx
files = nanoGetSampleFiles(mcDirectory_2018, 'TT_DiLept') + \
    nanoGetSampleFiles(mcDirectory_2018, 'ST_s-channel_ext1') + \
    nanoGetSampleFiles(mcDirectory_2018, 'ST_t-channel_antitop') + \
    nanoGetSampleFiles(mcDirectory_2018, 'ST_t-channel_top') + \
    nanoGetSampleFiles(mcDirectory_2018, 'ST_tW_antitop_ext1') + \
    nanoGetSampleFiles(mcDirectory_2018, 'ST_tW_top_ext1')

samples['top_2018'] = {
    'name': files,
    'weight': mcCommonWeight_2018,
    'FilesPerJob': 2,
}

Top_pTrw_2018 = '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)'

addSampleWeight(samples,'top_2018','TT_DiLept',Top_pTrw_2018)

###########################################
#############   SIGNALS  ##################
###########################################

###### WW ########

#xxxxxxx 2016 xxxxxxx
samples['WW_2016'] = {
    'name': nanoGetSampleFiles(mcDirectory_2016, 'WW-LO'),
    'weight': mcCommonWeight_2016+ '*nllW',
    'FilesPerJob': 4
}

#xxxxxxx 2017 xxxxxxx
samples['WW_2017'] = {
    'name': nanoGetSampleFiles(mcDirectory_2017, 'WW-LO'),
    'weight': mcCommonWeight_2017 + '*nllW',
    'FilesPerJob': 1
}

#xxxxxxx 2018 xxxxxxx
samples['WW_2018'] = {
    'name': nanoGetSampleFiles(mcDirectory_2018, 'WW-LO'),
    'weight': mcCommonWeight_2018+'*nllW',
    'FilesPerJob': 2
}

###### ggWW ########

#xxxxxxx 2016 xxxxxxx
samples['ggWW_2016'] = {
    'name': nanoGetSampleFiles(mcDirectory_2016, 'GluGluWWTo2L2Nu_MCFM'),
    'weight': mcCommonWeight_2016+'*1.53/1.4', # updating k-factor
    'FilesPerJob': 4
}

#xxxxxxx 2017 xxxxxxx
files = nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToENEN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToENMN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToENTN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToMNEN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToMNMN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToMNTN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToTNEN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToTNMN') + \
    nanoGetSampleFiles(mcDirectory_2017, 'GluGluToWWToTNTN')

samples['ggWW_2017'] = {
    'name': files,
    'weight': mcCommonWeight_2017 + '*1.53/1.4', # updating k-factor
    'FilesPerJob': 10
}

#xxxxxxx 2018 xxxxxxx
samples['ggWW_2018'] = {
    'name': nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToENEN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToENMN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToENTN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToMNEN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToMNMN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToMNTN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToTNEN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToTNMN') + \
            nanoGetSampleFiles(mcDirectory_2018, 'GluGluToWWToTNTN'),
    'weight': mcCommonWeight_2018+'*1.53/1.4',
    'FilesPerJob': 2
}
