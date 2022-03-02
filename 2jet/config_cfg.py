#!/usr/bin/env python

from __future__ import print_function
import os
from ROOT import gROOT, TFile, TChain, TCut

# import models
#import preselections

isDEV=False

# Load configuration
with open("configuration.py") as handle:
    exec handle

samples={}
structure={}
cuts={}

for f in [samplesFile, structureFile, cutsFile]:
    with open(f) as handle:
        exec handle


# Reduce sample files for fast dev
for sampleName, sample in samples.items():
    if sampleName not in ['ggWW_2016','ggWW_2017','ggWW_2018','WW_2016','WW_2017','WW_2018','top_2016','top_2017','top_2018']:
        samples.pop(sampleName)
        continue

    if isDEV:
        if len(sample['name']) > 2:
            sample['name'] = sample['name'][0:1]
    else :
        sample['name'] = sample['name']

# Define data to be loaded
#with open("./preselections.py") as handle:
#    exec handle

#cut="(({0}) && ({1}))".format(supercut,preselections['ALL'])
#cut="(({0}))".format(preselections['ALL'])
cut="(({0}))".format(supercut)
mvaVariables = [
   'pt1',
   'mll',
   'drll',
   'dphillmet',
   'mtw1',
   'mtw2',
   'pTWW',
   'pTHjj',
   'mjj',
   'detajj',
   'dphijj',
   'dphijet2met',
   'dphijjmet',
   'dphilep1jet1',
   'dphilep1jet2',
   'mindetajl',
   'Alt$(CleanJet_pt[0], 0)',
   'Alt$(CleanJet_pt[1], 0)',
   'Alt$(CleanJet_eta[0], 0)',
   'Alt$(CleanJet_eta[1], 0)',
   'Alt$(Jet_btagDeepB[CleanJet_jetIdx[0]],-2)',
   'Alt$(Jet_btagDeepB[CleanJet_jetIdx[1]],-2)'
]


