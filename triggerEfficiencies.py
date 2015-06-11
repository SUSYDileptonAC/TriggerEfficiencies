### Calculates efficiencies of DiLepton Triggers in HT of alphaT triggered events

import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import os
import pickle

from messageLogger import messageLogger as log

import math

from array import array

import argparse	


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1


from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts

from setTDRStyle import setTDRStyle
from helpers import readTrees, createHistoFromTree, TheStack, totalNumberOfGeneratedEvents, Process
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, baselineTrigger, systematics
from locations import locations

tableTemplate = r"""
\begin{tabular}{l|c|c|c|c}
Run Period & Trigger & $N_{nominator}$ & $N_{denominator}$ & efficiency\\
\hline
%s
\end{tabular}
"""

def getEfficiency(nominatorHisto, denominatorHisto,cutString):
	eff = TGraphAsymmErrors(nominatorHisto,denominatorHisto,"cp")
	effValue = ROOT.Double(0.)
	blubb = ROOT.Double(0.)
	intttt = eff.GetPoint(0,blubb,effValue) 
	   
	n= {
		"Nominator": nominatorHisto.Integral(),
		"Denominator": denominatorHisto.Integral(),
		"Efficiency": nominatorHisto.Integral()/denominatorHisto.Integral(),
		"UncertaintyUp": eff.GetErrorYhigh(0),
		"UncertaintyDown": eff.GetErrorYlow(0), 
		}
	#	print cut, n
	n["cut"] = cutString
	return n


def efficiencyRatio(eff1,eff2):
	newEff = TGraphAsymmErrors(eff1.GetN())
	for i in range(0,eff1.GetN()):
		pointX1 = ROOT.Double(0.)
		pointX2 = ROOT.Double(0.)
		pointY1 = ROOT.Double(0.)
		pointY2 = ROOT.Double(0.)
		
		isSuccesful1 = eff1.GetPoint(i,pointX1,pointY1)
		isSuccesful2 = eff2.GetPoint(i,pointX2,pointY2)
		errY1Up = eff1.GetErrorYhigh(i)
		errY1Low = eff1.GetErrorYlow(i)
		errY2Up = eff2.GetErrorYhigh(i)
		errY2Low = eff2.GetErrorYlow(i)
		
		errX = eff1.GetErrorX(i)
		if pointY2!=0:
			yValue = pointY1/pointY2
			xValue = pointX1
			xError = errX
			yErrorUp = math.sqrt(((1/pointY2)*errY1Up)**2+((pointY1/pointY2**2)*errY2Up)**2)
			yErrorDown = math.sqrt(((1/pointY2)*errY1Low)**2+((pointY1/pointY2**2)*errY2Low)**2)				
		else:
			yValue = 0
			xValue = pointX1
			xError = errX
			yErrorUp =0
			yErrorDown = 0
			
		#~ print i
		newEff.SetPoint(i,xValue,yValue)
		newEff.SetPointError(i,xError,xError,yErrorDown,yErrorUp)
		
	return newEff
	
def efficiencyRatioGeometricMean(eff1,eff2,eff3):
	newEff = TGraphAsymmErrors(eff1.GetN())
	for i in range(0,eff1.GetN()):
		pointX1 = ROOT.Double(0.)
		pointX2 = ROOT.Double(0.)
		pointX3 = ROOT.Double(0.)
		pointY1 = ROOT.Double(0.)
		pointY2 = ROOT.Double(0.)
		pointY3 = ROOT.Double(0.)
		
		isSuccesful1 = eff1.GetPoint(i,pointX1,pointY1)
		isSuccesful2 = eff2.GetPoint(i,pointX2,pointY2)
		isSuccesful3 = eff3.GetPoint(i,pointX3,pointY3)
		errY1Up = eff1.GetErrorYhigh(i)
		errY1Down = eff1.GetErrorYlow(i)
		errY2Up = eff2.GetErrorYhigh(i)
		errY2Down = eff2.GetErrorYlow(i)
		errY3Up = eff3.GetErrorYhigh(i)
		errY3Down = eff3.GetErrorYlow(i)
		
		errX = eff1.GetErrorX(i)
		#~ print pointY1
		#~ print pointY2


		if pointY3!=0 and pointY2!=0 and pointY3!=0:
			yValue = (pointY1*pointY2)**0.5/pointY3
			xValue = pointX1
			xError = errX			
			yErrorUp = math.sqrt( ( ( 0.5*(pointY1*pointY2)**(-0.5)*pointY2 / pointY3 ) * errY1Up )**2 + ( ( 0.5*(pointY1*pointY2)**(-0.5)*pointY1 / pointY3 ) * errY2Up )**2 + ( ( (pointY1*pointY2)**0.5/pointY3**2 ) * errY3Down )**2)				
			yErrorDown = math.sqrt( ( ( 0.5*(pointY1*pointY2)**(-0.5)*pointY2 / pointY3 ) * errY1Down )**2 + ( ( 0.5*(pointY1*pointY2)**(-0.5)*pointY1 / pointY3 ) * errY2Down )**2 + ( ( (pointY1*pointY2)**0.5/pointY3**2 ) * errY3Up )**2)				
		else:
			yValue = 0
			xValue = pointX1
			xError = errX
			yErrorUp =0
			yErrorDown = 0
			
		#~ print i
		newEff.SetPoint(i,xValue,yValue)
		newEff.SetPointError(i,xError,xError,yErrorDown,yErrorUp)
		
	return newEff


def getHistograms(path,source,modifier,plot,runRange,isMC,backgrounds,tight,source2,path2):
	


	
	if not isMC:
		additionalString = ""
		if source == "PFHT":
			additionalString = "PF"
		
		if "Single" in source:


		
			treesDenominatorEE = readTrees(path,"EE",source = source, modifier = "%s"%(source+"Trigger",))
			treesDenominatorMuMu = readTrees(path,"MuMu",source = source, modifier = "%s"%(source+"Trigger",))
			treesDenominatorEMu = readTrees(path,"EMu",source = source, modifier = "%s"%(source+"Trigger",))

			treesNominatorEE = readTrees(path,"EE",source = source,modifier="%sHLTDiEle"%(source+"Trigger"))
			treesNominatorMuMu = readTrees(path,"MuMu",source = source,modifier="%sHLTDiMu"%(source+"Trigger"))
			treesNominatorMuMuNoTrack = readTrees(path,"MuMu",source = source,modifier="%sHLTDiMuNoTrackerMuon"%(source+"Trigger"))
			treesNominatorEMu = readTrees(path,"EMu",source = source,modifier="%sHLTEleMu"%(source+"Trigger"))
			treesNominatorMuE = readTrees(path,"EMu",source = source,modifier="%sHLTMuEle"%(source+"Trigger"))
			treesNominatorMuEG = readTrees(path,"EMu",source = source,modifier="%sHLTMuEG"%(source+"Trigger"))
			
			cutStringEE = plot.cuts.replace("weight*(","weight*(matchesSingleElectron2 == 1 &&")				
			cutStringMuMu = plot.cuts.replace("weight*","weight*(matchesSingleMuon2 == 1)*")			
			cutStringEMu = plot.cuts.replace("weight*","weight*(pt1 > 20 && matchesSingleElectron1 == 1)*")	
			cutStringMuE = plot.cuts.replace("weight*","weight*(pt2 > 20 && matchesSingleMuon2 == 1 )*")	
			
			denominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEE.iteritems():
				denominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,cutStringEE,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())		
			denominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,cutStringEMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,cutStringMuE,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())


			nominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEE.iteritems():
				nominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,cutStringEE,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMu.iteritems():
				nominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMuNoTrack.iteritems():
				nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuE.iteritems():
				nominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,cutStringMuE,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEMu.iteritems():
				nominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,cutStringEMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuEG.iteritems():
				nominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			
		else:	
			treesDenominatorEE = readTrees(path,"EE",source = source, modifier = "%s"%("Trigger"+source,))
			treesDenominatorMuMu = readTrees(path,"MuMu",source = source, modifier = "%s"%("Trigger"+source,))
			treesDenominatorEMu = readTrees(path,"EMu",source = source, modifier = "%s"%("Trigger"+source,))
			treesNominatorEE = readTrees(path,"EE",source = source,modifier="%sHLT%sDiEle"%("Trigger"+source,additionalString))
			treesNominatorMuMu = readTrees(path,"MuMu",source = source,modifier="%sHLT%sDiMu"%("Trigger"+source,additionalString))
			treesNominatorMuMuNoTrack = readTrees(path,"MuMu",source = source,modifier="%sHLT%sDiMuNoTrackerMuon"%("Trigger"+source,additionalString))
			treesNominatorEMu = readTrees(path,"EMu",source = source,modifier="%sHLT%sEleMu"%("Trigger"+source,additionalString))
			treesNominatorMuE = readTrees(path,"EMu",source = source,modifier="%sHLT%sMuEle"%("Trigger"+source,additionalString))
			treesNominatorMuEG = readTrees(path,"EMu",source = source,modifier="%sHLT%sMuEG"%("Trigger"+source,additionalString))
				
			denominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEE.iteritems():
				denominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())		
			denominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			denominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())




			nominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEE.iteritems():
				nominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMu.iteritems():
				nominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMuNoTrack.iteritems():
				nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuE.iteritems():
				nominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEMu.iteritems():
				nominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
			nominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuEG.iteritems():
				nominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
				
		return {"EE":denominatorHistoEE,"MuMu":denominatorHistoMuMu,"MuMuNoTrack":denominatorHistoMuMuNoTrack,"EMu":denominatorHistoEMu,"MuE":denominatorHistoMuE,"MuEG":denominatorHistoMuEG} , {"EE":nominatorHistoEE,"MuMu":nominatorHistoMuMu,"MuMuNoTrack":nominatorHistoMuMuNoTrack,"EMu":nominatorHistoEMu,"MuE":nominatorHistoMuE,"MuEG":nominatorHistoMuEG}
	else:
		
		if "DiLeptonTrigger" in source:
			if "baseTrees" in source:	
				treesDenominatorEE = readTrees(path,"EE",source = "baseTrees", modifier = "baseTrees")
				treesDenominatorMuMu = readTrees(path2,"MuMu")
				treesDenominatorEMu = readTrees(path,"EMu",source = "baseTrees", modifier = "baseTrees")
				
				treesNominatorEE = readTrees(path,"EE",source = source,modifier= source)
				treesNominatorMuMu = readTrees(path2,"MuMu",source = source2,modifier= source2)
				treesNominatorEMu = readTrees(path,"EMu",source = source,modifier= source)
				
				eventCounts = totalNumberOfGeneratedEvents(path,source)
			else:
				treesDenominatorEE = readTrees(path,"EE",source = source.replace(modifier,""))
				treesDenominatorMuMu = readTrees(path,"MuMu",source = source.replace(modifier,""))
				treesDenominatorEMu = readTrees(path,"EMu",source = source.replace(modifier,""))
				
				treesNominatorEE = readTrees(path,"EE",source = source,modifier= modifier)
				treesNominatorMuMu = readTrees(path,"MuMu",source = source,modifier= modifier)
				treesNominatorEMu = readTrees(path,"EMu",source = source,modifier= modifier)
				
				eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)
			
				
			processes = []
			
			for background in backgrounds:
				processes.append(Process(getattr(Backgrounds,background),eventCounts))
			
			if tight:
				
				baseCuts = plot.cuts
				print baseCuts
				#~ prompt_cuts = "(%s) && (abs(motherPdgId1) == 15 || motherPdgId1 == 23 || abs(motherPdgId1) == 24) && (abs(motherPdgId2) == 15 || motherPdgId2 == 23 || abs(motherPdgId2) == 24)"%plot.cuts
				prompt_cuts = plot.cuts
				EECuts = "(%s) && iso1 <0.15 && iso2 < 0.15 && d01 < 0.02 && d02 < 0.02 && dZ1 < 0.1 && dZ2 < 0.1 && abs(deltaEtaSuperClusterTrackAtVtx1) < 0.007 && abs(deltaEtaSuperClusterTrackAtVtx2) < 0.007 && abs(deltaPhiSuperClusterTrackAtVtx1) < 0.015 && abs(deltaPhiSuperClusterTrackAtVtx2) < 0.015 && sigmaIetaIeta1 < 0.01 && sigmaIetaIeta2 < 0.01 && hadronicOverEm1 < 0.12 && hadronicOverEm2 < 0.12 && eOverP1 < 0.05 && eOverP2 < 0.05 && missingHits1 < 2 && missingHits2 < 2"%prompt_cuts
				EMuCuts = "(%s) && iso1 <0.15 && iso2 < 0.15 && d01 < 0.02 && d02 < 0.02 && dZ1 < 0.1 && dZ2 < 0.1 && abs(deltaEtaSuperClusterTrackAtVtx1) < 0.007 && abs(deltaPhiSuperClusterTrackAtVtx1) < 0.015 && sigmaIetaIeta1 < 0.01 && hadronicOverEm1 < 0.12 && eOverP1 < 0.05 && missingHits1 < 2 && globalMuon2 == 1 && trackerMuon2 == 1 && pfMuon2 == 1 && trackChi22 < 10 && numberOfValidMuonHits2 > 0 && numberOfMatchedStations2 > 1 && numberOfValidPixelHits2 > 0 && trackerLayersWithMeasurement2 > 5"%prompt_cuts
				
				
				plot.cuts = EECuts	
				nominatorStackEE = TheStack(processes,runRange.lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)
				denominatorStackEE = TheStack(processes,runRange.lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)
				
				plot.cuts = EMuCuts
				nominatorStackEMu = TheStack(processes,runRange.lumi,plot,treesNominatorEMu,"None",1.0,1.0,1.0)
				denominatorStackEMu = TheStack(processes,runRange.lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)			
				
				
				#~ plot.cuts = MuMuCuts
				#~ print MuMuCuts			
				plot.cuts = baseCuts			
				nominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)				
				denominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)
				
				plot.cuts = baseCuts

			else:
				denominatorStackEE = TheStack(processes,runRange.lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
				denominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
				denominatorStackEMu = TheStack(processes,runRange.lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
				
				nominatorStackEE = TheStack(processes,runRange.lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
				nominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)			
				nominatorStackEMu = TheStack(processes,runRange.lumi,plot,treesNominatorEMu,"None",1.0,1.0,1.0)
			
			denominatorHistoEE = denominatorStackEE.theHistogram
			denominatorHistoMuMu = denominatorStackMuMu.theHistogram
			denominatorHistoEMu = denominatorStackEMu.theHistogram
			
			nominatorHistoEE = nominatorStackEE.theHistogram
			nominatorHistoMuMu = nominatorStackMuMu.theHistogram
			nominatorHistoEMu = nominatorStackEMu.theHistogram
			
			
			return {"EE":denominatorHistoEE,"MuMu":denominatorHistoMuMu,"EMu":denominatorHistoEMu} , {"EE":nominatorHistoEE,"MuMu":nominatorHistoMuMu,"EMu":nominatorHistoEMu}
				
			

		else:
			if source == "PFHT":
				source = "HT"
			
			treesDenominatorEE = readTrees(path,"EE",source = "Summer12", modifier = "%s"%("TriggerEfficiency"+source,))
			treesDenominatorMuMu = readTrees(path,"MuMu",source = "Summer12", modifier = "%s"%("TriggerEfficiency"+source,))
			treesDenominatorEMu = readTrees(path,"EMu",source = "Summer12", modifier = "%s"%("TriggerEfficiency"+source,))
			
			
			treesNominatorEE = readTrees(path,"EE",source = "Summer12",modifier="%sHLTDiEle%s"%("TriggerEfficiency",source))
			treesNominatorMuMu = readTrees(path,"MuMu",source = "Summer12",modifier="%sHLTDiMu%s"%("TriggerEfficiency",source))
			treesNominatorMuMuNoTrack = readTrees(path,"MuMu",source = "Summer12",modifier="%sHLTDiMuNoTrackerMuon%s"%("TriggerEfficiency",source))
			treesNominatorEMu = readTrees(path,"EMu",source = "Summer12",modifier="%sHLTEleMu%s"%("TriggerEfficiency",source))
			treesNominatorMuE = readTrees(path,"EMu",source = "Summer12",modifier="%sHLTMuEle%s"%("TriggerEfficiency",source))
			treesNominatorMuEG = readTrees(path,"EMu",source = "Summer12",modifier="%sHLTMuEG%s"%("TriggerEfficiency",source))
			
			eventCounts = totalNumberOfGeneratedEvents(path,"TTJets")	
			processes = []
			for background in backgrounds:
				processes.append(Process(getattr(Backgrounds,background),eventCounts))
			
			denominatorStackEE = TheStack(processes,runRange.lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
			denominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
			denominatorStackEMu = TheStack(processes,runRange.lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
			denominatorStackMuE = TheStack(processes,runRange.lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
			denominatorStackMuEG = TheStack(processes,runRange.lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
				
			nominatorStackEE = TheStack(processes,runRange.lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
			nominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)		
			nominatorStackMuMuNoTrack = TheStack(processes,runRange.lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
			nominatorStackEMu = TheStack(processes,runRange.lumi,plot,treesNominatorEMu,"None",1.0,1.0,1.0)		
			nominatorStackMuE = TheStack(processes,runRange.lumi,plot,treesNominatorMuE,"None",1.0,1.0,1.0)		
			nominatorStackMuEG = TheStack(processes,runRange.lumi,plot,treesNominatorMuEG,"None",1.0,1.0,1.0)		
	
			denominatorHistoEE = denominatorStackEE.theHistogram
			denominatorHistoMuMu = denominatorStackMuMu.theHistogram
			denominatorHistoMuMuNoTrack = denominatorStackMuMu.theHistogram
			denominatorHistoEMu = denominatorStackEMu.theHistogram
			denominatorHistoMuE = denominatorStackMuE.theHistogram
			denominatorHistoMuEG = denominatorStackMuEG.theHistogram
			
			nominatorHistoEE = nominatorStackEE.theHistogram
			nominatorHistoMuMu = nominatorStackMuMu.theHistogram
			nominatorHistoMuMuNoTrack = nominatorStackMuMuNoTrack.theHistogram
			nominatorHistoEMu = nominatorStackEMu.theHistogram
			nominatorHistoMuE = nominatorStackMuE.theHistogram
			nominatorHistoMuEG = nominatorStackMuEG.theHistogram		

			return {"EE":denominatorHistoEE,"MuMu":denominatorHistoMuMu,"MuMuNoTrack":denominatorHistoMuMuNoTrack,"EMu":denominatorHistoEMu,"MuE":denominatorHistoMuE,"MuEG":denominatorHistoMuEG} , {"EE":nominatorHistoEE,"MuMu":nominatorHistoMuMu,"MuMuNoTrack":nominatorHistoMuMuNoTrack,"EMu":nominatorHistoEMu,"MuE":nominatorHistoMuE,"MuEG":nominatorHistoMuEG}

def centralValues(source,modifier,path,selection,runRange,isMC,backgrounds,ptCut,tight,source2,path2):
	
	
	if "Central" in selection.name:
		err = systematics.trigger.central.val
	elif "Forward" in selection.name:
		err = systematics.trigger.forward.val
	else:
		print "have no uncertainty for this selection, using 5%"
		err = 0.05
	
	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	if ptCut != "pt2020":
		pt_Cut = getattr(theCuts.ptCuts,ptCut)
		plot.cuts = plot.cuts.replace("pt1 > 20 && pt2 > 20",pt_Cut.cut)
		pt_label = pt_Cut.label
	else:
		pt_label = "p_{T} > 20 GeV"	
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		
	plot.firstBin = 20
	plot.lastBin = 10000
	plot.nBins = 1
	
	counts = {runRange.label:{}}	
								
	denominators, nominators = getHistograms(path,source,modifier,plot,runRange,isMC,backgrounds,tight,source2,path2)
	
	counts[runRange.label]["EE"] = getEfficiency(nominators["EE"], denominators["EE"],plot.cuts)
	counts[runRange.label]["MuMu"] = getEfficiency(nominators["MuMu"], denominators["MuMu"],plot.cuts)
	counts[runRange.label]["EMu"] = getEfficiency(nominators["EMu"], denominators["EMu"],plot.cuts)
	counts[runRange.label]["RT"] = (counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**0.5 / counts[runRange.label]["EMu"]["Efficiency"]
	counts[runRange.label]["RTErrSyst"] =  counts[runRange.label]["RT"]*(err**2/(2*counts[runRange.label]["EE"]["Efficiency"])**2+ err**2/(2*counts[runRange.label]["MuMu"]["Efficiency"])**2 + err**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5
	counts[runRange.label]["RTErrStat"] =  counts[runRange.label]["RT"]*(max(counts[runRange.label]["EE"]["UncertaintyUp"],counts[runRange.label]["EE"]["UncertaintyDown"])**2/(2*counts[runRange.label]["EE"]["Efficiency"])**2+ max(counts[runRange.label]["MuMu"]["UncertaintyUp"],counts[runRange.label]["MuMu"]["UncertaintyDown"])**2/(2*counts[runRange.label]["MuMu"]["Efficiency"])**2 + max(counts[runRange.label]["EMu"]["UncertaintyUp"],counts[runRange.label]["EMu"]["UncertaintyDown"])**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5
	
	#~ counts[runRange.label]["EE"] = getEfficiency(nominators["EE"], denominators["EE"],plot.cuts)
	#~ counts[runRange.label]["MuMu"] = getEfficiency(nominators["MuMu"], denominators["MuMu"],plot.cuts)
	#~ counts[runRange.label]["MuMuNoTrack"] = getEfficiency(nominators["MuMuNoTrack"], denominators["MuMuNoTrack"],plot.cuts)
	#~ counts[runRange.label]["EMu"] = getEfficiency(nominators["MuEG"], denominators["MuEG"],plot.cuts)
	#~ counts[runRange.label]["RT"] = (counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**0.5 / counts[runRange.label]["EMu"]["Efficiency"]
	#~ counts[runRange.label]["RTErrSyst"] =  (err**2/(2*counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**2+ err**2/(2*counts[runRange.label]["MuMu"]["Efficiency"]*counts[runRange.label]["EE"]["Efficiency"])**2 + err**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5
	#~ counts[runRange.label]["RTErrStat"] =  (max(counts[runRange.label]["EE"]["UncertaintyUp"],counts[runRange.label]["EE"]["UncertaintyDown"])**2/(2*counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**2+ max(counts[runRange.label]["MuMu"]["UncertaintyUp"],counts[runRange.label]["MuMu"]["UncertaintyDown"])**2/(2*counts[runRange.label]["MuMu"]["Efficiency"]*counts[runRange.label]["EE"]["Efficiency"])**2 + max(counts[runRange.label]["EMu"]["UncertaintyUp"],counts[runRange.label]["EMu"]["UncertaintyDown"])**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5

	return counts



def dependencies(source,modifier,path,selection,plots,runRange,isMC,backgrounds,cmsExtra,ptCut,tight,source2,path2):

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	

	legend = TLegend(0.55, 0.16, 0.9, 0.35)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	
	legendHist1 = TH1F()
	legendHist2 = TH1F()
	legendHist3 = TH1F()
	legendHist4 = TH1F()
	legendHist5 = TH1F()
	
	legendHist1.SetMarkerColor(ROOT.kBlack)
	legendHist2.SetMarkerColor(ROOT.kRed)
	#~ legendHist3.SetMarkerColor(ROOT.kRed+2)
	legendHist3.SetMarkerColor(ROOT.kBlue)
	legendHist4.SetMarkerColor(ROOT.kBlue+2)
	
	legend.AddEntry(legendHist1,"Ele_17_X_Ele8_X","p")
	#~ legend.AddEntry(legendHist2,"Mu17_Mu8 or Mu17_TkMu8","p")
	legend.AddEntry(legendHist2,"Mu17_TrkIsoVVL_Mu8_TrkIsoVVL","p")
	legend.AddEntry(legendHist3,"Mu17_Ele8_X","p")
	legend.AddEntry(legendHist4,"Ele17_X_Mu8","p")
	
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(11)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexLumi = ROOT.TLatex()
	latexLumi.SetTextFont(42)
	latexLumi.SetTextAlign(31)
	latexLumi.SetTextSize(0.04)
	latexLumi.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	#latexCMS.SetTextAlign(31)
	latexCMS.SetTextSize(0.06)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	#latexCMSExtra.SetTextAlign(31)
	latexCMSExtra.SetTextSize(0.045)
	latexCMSExtra.SetNDC(True)		
	


	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)		
	#~ if isMC:
		#~ if os.path.isfile("shelves/triggerEff_%s_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label,ptCut)):
			#~ centralVals = pickle.load(open("shelves/triggerEff_%s_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label,ptCut),"rb"))
		#~ else:
			#~ centralVals = centralValues(source,path,selection,runRange,isMC,backgrounds,ptCut)
	#~ else:
		#~ if os.path.isfile("shelves/triggerEff_%s_%s_%s_%s.pkl"%(selection.name,source,runRange.label,ptCut)):
			#~ centralVals = pickle.load(open("shelves/triggerEff_%s_%s_%s_%s.pkl"%(selection.name,source,runRange.label,ptCut),"rb"))
		#~ else:
	centralVals = centralValues(source,modifier,path,selection,runRange,isMC,backgrounds,ptCut,tight,source2,path2)
	
				
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		if ptCut != "pt2020":
			pt_Cut = getattr(theCuts.ptCuts,ptCut)
			plot.cuts = plot.cuts.replace("pt1 > 20 && pt2 > 20",pt_Cut.cut)
			pt_label = pt_Cut.label
		else:
			pt_label = "p_{T} > 20 GeV"	
		#~ plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut	

		if  "Forward" in selection.name:
			plot.nBins = int(plot.nBins/2)
		denominators, nominators = getHistograms(path,source,modifier,plot,runRange,isMC,backgrounds,tight,source2,path2)	
		
		if "MiniIsoEffAreaIso" in source:
			iso_label = "mini iso cone, eff. area corrected"
		elif "MiniIsoDeltaBetaIso" in source:
			iso_label = "mini iso cone, #Delta#beta corrected"
		elif "MiniIsoPFWeights" in source:
			iso_label = "mini iso cone, PF weights"
		elif "EffAreaIso" in source:
			iso_label = "R=0.3 cone, eff. area corrected"
		elif "DeltaBetaIso" in source:
			iso_label = "R=0.3 cone, #Delta#beta corrected"


		if "DiLeptonTrigger" in source:
			effEE = TGraphAsymmErrors(nominators["EE"],denominators["EE"],"cp")
			effEMu = TGraphAsymmErrors(nominators["EMu"],denominators["EMu"],"cp")
			effMuMu = TGraphAsymmErrors(nominators["MuMu"],denominators["MuMu"],"cp")
			
	
			effEE.SetMarkerColor(ROOT.kBlack)
			effMuMu.SetMarkerColor(ROOT.kRed)
			effEMu.SetMarkerColor(ROOT.kBlue+2)
			effEE.SetLineColor(ROOT.kBlack)
			effMuMu.SetLineColor(ROOT.kRed)			
			effEMu.SetLineColor(ROOT.kBlue+2)
			effEE.SetMarkerStyle(20)
			effMuMu.SetMarkerStyle(21)
			effEMu.SetMarkerStyle(33)				
			plotPad.DrawFrame(plot.firstBin,0.6,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
			
	
			
			leg = TLegend(0.525, 0.16, 0.95, 0.4)
			leg.SetFillStyle(0)
			leg.SetBorderSize(0)
			leg.AddEntry(effEE,"Ele23_X_Ele12_X ","p")
			#~ leg.AddEntry(effMuMu,"Mu17_Mu8 || Mu17_TkMu8","p")
			leg.AddEntry(effMuMu,"Mu17_TrkIsoVVL_Mu8_TrkIsoVVL","p")
			leg.AddEntry(effEMu,"Ele23_X_Mu8 || Mu23_Ele12_X","p")
	
			
			effEE.Draw("samep")
			effMuMu.Draw("samep")
			effEMu.Draw("samep")
	
			#~ latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
			latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
			if tight:
				latex.DrawLatex(0.25, 0.4, "tight Supercluster #Delta#phi cut")
			latex.DrawLatex(0.25, 0.2, pt_label)
			latex.DrawLatex(0.25, 0.25, selection.latex)
			latex.DrawLatex(0.35, 0.75, iso_label)
			
	
			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	
	
			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
			leg.Draw("same")
			if isMC:
				if tight:
					hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s_%s_MC_tight.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
				else:
					hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
			else:	
				hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
			
			denominatorHistoSF = denominators["EE"].Clone()
			denominatorHistoOF = denominators["EMu"].Clone()
			denominatorHistoSF.Add(denominators["MuMu"].Clone())
			
			nominatorHistoSF = nominators["EE"].Clone()
			
			nominatorHistoSF.Add(nominators["MuMu"].Clone())
			
			nominatorHistoOF = nominators["EMu"].Clone()
			
			effSF = TGraphAsymmErrors(nominatorHistoSF,denominatorHistoSF,"cp")
			effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cp")
	
	
	
			effSF.SetMarkerColor(ROOT.kBlack)
			effOF.SetMarkerColor(ROOT.kBlue)
			effSF.SetLineColor(ROOT.kBlack)
			effOF.SetLineColor(ROOT.kBlue)
			effSF.SetMarkerStyle(20)
			effOF.SetMarkerStyle(22)			
		
			plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
				
			legend.Clear()
			#~ legend.AddEntry(effSF,"Ele23_X_Ele12_X || Mu17_Mu8 || Mu17_TkMu8 ","p")
			legend.AddEntry(effSF,"Ele23_X_Ele12_X || Mu17_Mu8","p")
			legend.AddEntry(effOF,"Mu23_Ele12_X || Ele23_X_Mu8" ,"p")
	
			effSF.Draw("samep")
			effOF.Draw("samep")
		
			#~ latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
			latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
			if tight:
				latex.DrawLatex(0.25, 0.4, "tight Supercluster #Delta#phi cut")
			latex.DrawLatex(0.25, 0.2, pt_label)
			latex.DrawLatex(0.25, 0.25, selection.latex)
			latex.DrawLatex(0.35, 0.75, iso_label)
				
			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	
	
			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
			legend.Draw("same")
			if isMC:
				if tight:
					hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s_%s_MC_tight.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
				else:
					hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
			else:	
				hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
	
	
			plotPad.DrawFrame(plot.firstBin,.6,plot.lastBin,1.4,"; %s ; R_{T}" %(plot.xaxis))
			#~ plotPad.DrawFrame(plot.firstBin,0.,plot.lastBin,2.,"; %s ; R_{T}" %(plot.xaxis))
	
			
			effSFvsOF = efficiencyRatioGeometricMean(effEE,effMuMu,effOF)
	
			x= array("f",[plot.firstBin, plot.lastBin]) 
		
			y= array("f", [float(centralVals[runRange.label]["RT"]), float(centralVals[runRange.label]["RT"])]) 
			ey= array("f", [float(centralVals[runRange.label]["RTErrSyst"]), float(centralVals[runRange.label]["RTErrSyst"])])					
			sfLine= ROOT.TF1("sfLine",str(centralVals[runRange.label]["RT"]),plot.firstBin, plot.lastBin)
			ex= array("f", [0.,0.])
			
			ge= ROOT.TGraphErrors(2, x, y, ex, ey)
			ge.SetFillColor(ROOT.kOrange-9)
			ge.SetFillStyle(1001)
			ge.SetLineColor(ROOT.kWhite)
			ge.Draw("SAME 3")
			
			effSFvsOF.Draw("samep")
			
			
			sfLine.SetLineColor(ROOT.kBlack)
			sfLine.SetLineWidth(3)
			sfLine.SetLineStyle(2)
			sfLine.Draw("SAME")				
			
			#~ latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
			latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
			if tight:
				latex.DrawLatex(0.25, 0.4, "tight Supercluster #Delta#phi cut")
			latex.DrawLatex(0.25, 0.2, pt_label)
			latex.DrawLatex(0.25, 0.25, selection.latex)
			latex.DrawLatex(0.35, 0.75, iso_label)
	
			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	
	
			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	
	
			
			legend.Clear()
			legend.AddEntry(effSFvsOF,"R_{T}","p")
			legend.AddEntry(sfLine,"Mean R_{T}: %.3f"%(centralVals[runRange.label]["RT"]),"l") 
			legend.AddEntry(ge,"syst. uncert.","f") 
			legend.Draw("same")
			ROOT.gPad.RedrawAxis()
			if isMC:
				if tight:
					hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s_%s_MC_tight.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
				else:		
					hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))		
			else:
				hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))
		
		else:	
			effEE = TGraphAsymmErrors(nominators["EE"],denominators["EE"],"cp")
			effEMu = TGraphAsymmErrors(nominators["EMu"],denominators["EMu"],"cp")
			effMuE = TGraphAsymmErrors(nominators["MuE"],denominators["MuE"],"cp")
			effMuMu = TGraphAsymmErrors(nominators["MuMu"],denominators["MuMu"],"cp")
			effMuMuNoTrack = TGraphAsymmErrors(nominators["MuMuNoTrack"],denominators["MuMuNoTrack"],"cp")
	
			effEE.SetMarkerColor(ROOT.kBlack)
			effMuMu.SetMarkerColor(ROOT.kRed)
			effMuMuNoTrack.SetMarkerColor(ROOT.kRed+2)
			effMuE.SetMarkerColor(ROOT.kBlue)
			effEMu.SetMarkerColor(ROOT.kBlue+2)
			effEE.SetLineColor(ROOT.kBlack)
			effMuMu.SetLineColor(ROOT.kRed)
			effMuMuNoTrack.SetLineColor(ROOT.kRed+2)
			effMuE.SetLineColor(ROOT.kBlue)
			effEMu.SetLineColor(ROOT.kBlue+2)
			effEE.SetMarkerStyle(20)
			effMuMu.SetMarkerStyle(21)
			effMuMuNoTrack.SetMarkerStyle(22)
			effMuE.SetMarkerStyle(23)
			effEMu.SetMarkerStyle(33)				
			plotPad.DrawFrame(plot.firstBin,0.6,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
			
	
			
			legend.Clear()
			legend.AddEntry(effEE,"Ele_17_X_Ele8_X ","p")
			#~ legend.AddEntry(effMuMu,"Mu17_Mu8 || Mu17_TkMu8","p")
			legend.AddEntry(effMuMu,"Mu17_TrkIsoVVL_Mu8_TrkIsoVVL","p")
			legend.AddEntry(effMuE,"Mu17_Ele8_X","p")
			legend.AddEntry(effEMu,"Ele17_X_Mu8","p")
	
			
			effEE.Draw("samep")
			effMuMu.Draw("samep")
			#~ effMuMuNoTrack.Draw("samep")
			effMuE.Draw("samep")
			effEMu.Draw("samep")
	
			latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
			
	
			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	
	
			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
			legend.Draw("same")
			if isMC:
				hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
			else:	
				hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
			
			denominatorHistoSF = denominators["EE"].Clone()
			denominatorHistoOF = denominators["MuEG"].Clone()
			denominatorHistoSF.Add(denominators["MuMu"].Clone())
			
			nominatorHistoSF = nominators["EE"].Clone()
			nominatorHistoSFNoTrack = nominators["EE"].Clone()
			
			nominatorHistoSF.Add(nominators["MuMu"].Clone())
			nominatorHistoSFNoTrack.Add(nominators["MuMuNoTrack"].Clone())
			
			nominatorHistoOF = nominators["MuEG"].Clone()
			
			effSF = TGraphAsymmErrors(nominatorHistoSF,denominatorHistoSF,"cp")
			effSFNoTrack = TGraphAsymmErrors(nominatorHistoSFNoTrack,denominatorHistoSF,"cp")
			effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cp")
	
	
	
			effSF.SetMarkerColor(ROOT.kBlack)
			effSFNoTrack.SetMarkerColor(ROOT.kRed)
			effOF.SetMarkerColor(ROOT.kBlue)
			effSF.SetLineColor(ROOT.kBlack)
			effSFNoTrack.SetLineColor(ROOT.kRed)
			effOF.SetLineColor(ROOT.kBlue)
			effSF.SetMarkerStyle(20)
			effSFNoTrack.SetMarkerStyle(21)
			effOF.SetMarkerStyle(22)
			
			effSFNoFit = effSF.Clone()
			effSFNoTrackNoFit = effSF.Clone()
			effOFNoFit = effSF.Clone()
			
		
			plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
			
	
			legend.Clear()
			#~ legend.AddEntry(effSF,"Ele_17_X_Ele8_X || Mu17_Mu8 || Mu17_TkMu8 ","p")
			legend.AddEntry(effSF,"Ele_17_X_Ele8_X || Mu17_Mu8","p")
			legend.AddEntry(effOF,"Mu17_Ele8_X || Ele17_X_Mu8" ,"p")
	
			effSF.Draw("samep")
			effOF.Draw("samep")
	
	
			latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
			
	
			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	
	
			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
			legend.Draw("same")
			if isMC:
				hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
			else:	
				hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
	
	
			plotPad.DrawFrame(plot.firstBin,.6,plot.lastBin,1.4,"; %s ; R_{T}" %(plot.xaxis))
	
			
			effSFvsOF = efficiencyRatioGeometricMean(effEE,effMuMu,effOF)
	
			x= array("f",[plot.firstBin, plot.lastBin]) 
		
			y= array("f", [float(centralVals[runRange.label]["RT"]), float(centralVals[runRange.label]["RT"])]) 
			ey= array("f", [float(centralVals[runRange.label]["RTErrSyst"]), float(centralVals[runRange.label]["RTErrSyst"])])					
			sfLine= ROOT.TF1("sfLine",str(centralVals[runRange.label]["RT"]),plot.firstBin, plot.lastBin)
			ex= array("f", [0.,0.])
			
			ge= ROOT.TGraphErrors(2, x, y, ex, ey)
			ge.SetFillColor(ROOT.kOrange-9)
			ge.SetFillStyle(1001)
			ge.SetLineColor(ROOT.kWhite)
			ge.Draw("SAME 3")
			
			effSFvsOF.Draw("samep")
			
			
			sfLine.SetLineColor(ROOT.kBlack)
			sfLine.SetLineWidth(3)
			sfLine.SetLineStyle(2)
			sfLine.Draw("SAME")				
			
			latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
			
	
			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	
	
			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	
	
			
			legend.Clear()
			legend.AddEntry(effSFvsOF,"R_{T}","p")
			legend.AddEntry(sfLine,"Mean R_{T}: %.3f"%(centralVals[runRange.label]["RT"]),"l") 
			legend.AddEntry(ge,"syst. uncert.","f") 
			legend.Draw("same")
			ROOT.gPad.RedrawAxis()
			if isMC:
				hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))		
			else:
				hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
			
			
def studyTriggerBias(path,source,plots,selection,runRange,backgrounds,cmsExtra):			
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cuts = plot.cuts % runRange.runCut	

		denominators, nominators = getHistograms(path,source,plot,runRange,True,backgrounds)
		denominatorsNoTrig, nominatorsNoTrig = getHistograms(path,"",plot,runRange,True,backgrounds)


		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()

		plotPad.Draw()	
		plotPad.cd()	
		
		legend = TLegend(0.5, 0.13, 0.95, 0.3)
		legend.SetFillStyle(0)
		legend.SetBorderSize(1)
		
		legendHist1 = TH1F()
		legendHist2 = TH1F()
		legendHist3 = TH1F()
		legendHist4 = TH1F()
		legendHist5 = TH1F()
		
		legendHist1.SetMarkerColor(ROOT.kBlack)
		legendHist2.SetMarkerColor(ROOT.kRed)
		#~ legendHist3.SetMarkerColor(ROOT.kRed+2)
		legendHist3.SetMarkerColor(ROOT.kBlue)
		legendHist4.SetMarkerColor(ROOT.kBlue+2)
		
		legend.AddEntry(legendHist1,"Ele_17_X_Ele8_X","p")
		#~ legend.AddEntry(legendHist2,"Mu17_Mu8 || Mu17_TkMu8","p")
		legend.AddEntry(legendHist2,"Mu17_TrkIsoVVL_Mu8_TrkIsoVVL","p")
		legend.AddEntry(legendHist3,"Mu17_Ele8_X","p")
		legend.AddEntry(legendHist4,"Ele17_X_Mu8","p")
		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)		

		intlumi = ROOT.TLatex()
		intlumi.SetTextAlign(12)
		intlumi.SetTextSize(0.03)
		intlumi.SetNDC(True)					
		
		
		denominatorHistoSF = denominators["EE"].Clone()
		denominatorHistoSF.Add(denominators["MuMu"].Clone())
		denominatorHistoOF = denominators["MuEG"].Clone()
		
		nominatorHistoSF = nominators["EE"].Clone()
		nominatorHistoSF.Add(nominators["MuMu"].Clone())
		
		nominatorHistoOF = nominators["MuEG"].Clone()
		
		denominatorHistoSFNoTrig = denominatorsNoTrig["EE"].Clone()
		denominatorHistoSFNoTrig.Add(denominatorsNoTrig["MuMu"].Clone())
		denominatorHistoOFNoTrig = denominatorsNoTrig["MuEG"].Clone()
		
		nominatorHistoSFNoTrig = nominatorsNoTrig["EE"].Clone()
		nominatorHistoSFNoTrig.Add(nominatorsNoTrig["MuMu"].Clone())
		
		nominatorHistoOFNoTrig = nominatorsNoTrig["MuEG"].Clone()

		effSF = TGraphAsymmErrors(nominatorHistoSF,denominatorHistoSF,"cl=0.683 b(1,1) mode")
		effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cl=0.683 b(1,1) mode")
		
		effSFNoTrig = TGraphAsymmErrors(nominatorHistoSFNoTrig,denominatorHistoSFNoTrig,"cl=0.683 b(1,1) mode")
		effOFNoTrig = TGraphAsymmErrors(nominatorHistoOFNoTrig,denominatorHistoOFNoTrig,"cl=0.683 b(1,1) mode")




		effRatioSF = efficiencyRatio(effSF,effSFNoTrig)
		effRatioOF = efficiencyRatio(effOF,effOFNoTrig)
		
		effRatioSF.SetMarkerStyle(21)
		effRatioOF.SetMarkerStyle(22)
		effRatioOF.SetMarkerColor(ROOT.kBlue)
		effRatioOF.SetLineColor(ROOT.kBlue)
		
		hCanvas.DrawFrame(plot.firstBin,0.95,plot.lastBin,1.05,"; %s ; Measured Efficiency / True Efficiency" %(plot.xaxis))


		x= array("f",[plot.firstBin, plot.lastBin]) 
		y= array("f", [1.0, 1.0]) # 1.237
		ex= array("f", [0.,0.])
		ey= array("f", [0.01, 0.01])
		ge= ROOT.TGraphErrors(2, x, y, ex, ey)
		ge.SetFillColor(ROOT.kOrange-9)
		ge.SetFillStyle(1001)
		ge.SetLineColor(ROOT.kWhite)

		sfLine= ROOT.TF1("sfLine","1.0",plot.firstBin, plot.lastBin)
		sfLine.SetLineColor(ROOT.kBlack)
		sfLine.SetLineWidth(3)
		sfLine.SetLineStyle(2)
		sfLine.Draw("SAME")					

		effRatioOF.Draw("samep")
		effRatioSF.Draw("samep")



		legend.Clear()
		legend.AddEntry(effRatioSF,"Same Flavour","p")
		legend.AddEntry(effRatioOF,"Opposite Flavour","p")
		legend.AddEntry(sfLine,"1.0","l")




		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		
		legend.Draw("same")
		if source == "HT" or source == "AlphaT":
			hCanvas.Print("fig/Triggereff_AlphaTSyst_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/Triggereff_AlphaTSyst_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))								
				


def singleLepton(path,selection,runRange,backgrounds,cmsExtra):
	
	
	plot = getPlot("trailigPtPlotTriggerLeading30Single")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut	
	
	
	denominatorsElectron, nominatorsElectron = getHistograms(path,"SingleElectron",plot,runRange,False,backgrounds)
	denominatorsMuon, nominatorsMuon = getHistograms(path,"SingleMuon",plot,runRange,False,backgrounds)

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	
	legend = TLegend(0.3, 0.15, 0.95, 0.5)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)

	
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	#latexCMS.SetTextAlign(31)
	latexCMS.SetTextSize(0.06)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	#latexCMSExtra.SetTextAlign(31)
	latexCMSExtra.SetTextSize(0.045)
	latexCMSExtra.SetNDC(True)		
	


	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)				



	effEE = TGraphAsymmErrors(nominatorsElectron["EE"],denominatorsElectron["EE"],"cp")
	effEMu = TGraphAsymmErrors(nominatorsElectron["EMu"],denominatorsElectron["EMu"],"cp")
	effMuE = TGraphAsymmErrors(nominatorsMuon["MuE"],denominatorsMuon["MuE"],"cp")
	effMuMu = TGraphAsymmErrors(nominatorsMuon["MuMu"],denominatorsMuon["MuMu"],"cp")
	effMuMuNoTrack = TGraphAsymmErrors(nominatorsMuon["MuMuNoTrack"],denominatorsMuon["MuMuNoTrack"],"cp")

	effEE.SetMarkerColor(ROOT.kBlack)
	effMuMu.SetMarkerColor(ROOT.kRed)
	effMuMuNoTrack.SetMarkerColor(ROOT.kRed+2)
	effMuE.SetMarkerColor(ROOT.kBlue)
	effEMu.SetMarkerColor(ROOT.kBlue+2)
	effEE.SetLineColor(ROOT.kBlack)
	effMuMu.SetLineColor(ROOT.kRed)
	effMuMuNoTrack.SetLineColor(ROOT.kRed+2)
	effMuE.SetLineColor(ROOT.kBlue)
	effEMu.SetLineColor(ROOT.kBlue+2)
	effEE.SetMarkerStyle(20)
	effMuMu.SetMarkerStyle(21)
	effMuMuNoTrack.SetMarkerStyle(22)
	effMuE.SetMarkerStyle(23)
	effEMu.SetMarkerStyle(33)				
	plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
	
		
	
	
	fitEE = TF1("fitEE","[0]",0,100)
	fitMuMu = TF1("fitMuMu","[0]",0,100)
	fitMuMuNoTrack = TF1("fitMuMuNoTrack","[0]",0,100)
	fitEMu = TF1("fitEMu","[0]",0,100)
	fitMuE = TF1("fitMuE","[0]",0,100)
	#~ fitEE = TF1("fitEE","0.5*[2]*(1. + TMath::Erf((x-[0])/(TMath::Sqrt(2)*[1])))",0,100)
	#~ fitEE.SetParameter(2,0.95)
	#~ fitEE.SetParameter(0,10)
	#~ fitEE.SetParLimits(0,100)
	#~ fitEE.SetParameter(1,1)

	fitEE.SetLineColor(ROOT.kBlack)
	fitMuMu.SetLineColor(ROOT.kRed)
	fitMuMuNoTrack.SetLineColor(ROOT.kRed+2)
	fitEMu.SetLineColor(ROOT.kBlue+2)
	fitMuE.SetLineColor(ROOT.kBlue)
	effEE.Fit("fitEE","BRQE","",40,100)
	effMuMu.Fit("fitMuMu","BRQE","",40,100)
	effMuMuNoTrack.Fit("fitMuMuNoTrack","BRQE","",40,100)
	effEMu.Fit("fitEMu","BRQE","",40,100)
	effMuE.Fit("fitMuE","BRQE","",40,100)
	
	legend.Clear()

	legend.SetHeader("Efficiencies of trailing lepton leg")
	legend.AddEntry(effEE,"Dielectron %.3f #pm %.3f"%(fitEE.GetParameter(0),fitEE.GetParError(0)),"p")
	legend.AddEntry(effMuMu,"Dimuon incl. tracker muon %.3f #pm %.3f"%(fitMuMu.GetParameter(0),fitMuMu.GetParError(0)),"p")
	legend.AddEntry(effMuMuNoTrack,"Dimuon %.3f #pm %.3f"%(fitMuMuNoTrack.GetParameter(0),fitMuMuNoTrack.GetParError(0)),"p")
	legend.AddEntry(effMuE,"OF muon leading %.3f #pm %.3f"%(fitMuE.GetParameter(0),fitMuE.GetParError(0)),"p")
	legend.AddEntry(effEMu,"OF electron leading %.3f #pm %.3f"%(fitEMu.GetParameter(0),fitEMu.GetParError(0)),"p")

	
	effEE.Draw("samep")
	effMuMu.Draw("samep")
	effMuMuNoTrack.Draw("samep")
	effMuE.Draw("samep")
	effEMu.Draw("samep")


	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.89,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.82	
	else:
		yLabelPos = 0.85	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	#~ intlumi.DrawLatex(0.2,0.9,"#splitline{"+logEtaCut+", "+cut.label1+"}{"+variable.additionalCutsLabel+"}")	
	legend.Draw("same")
	
	
	line1 = ROOT.TLine(20,0,20,1.05)
	line1.SetLineColor(ROOT.kBlue+3)

	line1.SetLineWidth(2)
	line1.SetLineStyle(2)

	line1.Draw("same")				
				
	hCanvas.Print("fig/Triggereff_SingleLepton_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	

			
				
def main():


	parser = argparse.ArgumentParser(description='Trigger efficiency measurements.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="use MC, default is to use data.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", action ="append", default=[],
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-C", "--ptCut",action="store", dest="ptCut", default="pt2020",
						  help="modify the pt cuts")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")
	parser.add_argument("-T", "--tight",action="store_true", dest="tight", default=False,
						  help="use tight electron id like for emu trigger")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-a", "--alphaT", action="store_true", dest="alphaT", default=False,
						  help="use alphaT triggers as baseline.")	
	parser.add_argument("-l", "--dilepton", action="store_true", dest="dilepton", default=False,
						  help="use dilepton triggers as baseline.")	
	parser.add_argument("-e", "--effectiveArea", action="store_true", dest="effectiveArea", default=False,
						  help="use effective area PU corrections.")	
	parser.add_argument("-D", "--deltaBeta", action="store_true", dest="deltaBeta", default=False,
						  help="use delta beta PU corrections.")	
	parser.add_argument("-R", "--constantConeSize", action="store_true", dest="constantConeSize", default=False,
						  help="use constant cone of R=0.3 for iso.")	
	parser.add_argument("-z", "--bias", action="store_true", dest="bias", default=False,
						  help="produce trigger bias studies.")	
	parser.add_argument("-t", "--trailing", action="store_true", dest="trailing", default=False,
						  help="trailing lepton pt dependence using single lepton trigger.")						
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
					
	args = parser.parse_args()





	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.trigger
	if len(args.plots) == 0:
		args.plots = plotLists.trigger
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.triggerEfficiencies.central.name)	
		args.selection.append(regionsToUse.triggerEfficiencies.forward.name)	
		args.selection.append(regionsToUse.triggerEfficiencies.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	

	if args.bias:
		args.mc = True
				
	path = locations.triggerDataSetPath	
	if args.mc:
		path = locations.triggerDataSetPathMC
	if args.trailing:
		path = locations.triggerDataSetPathSingleLepton
	if args.alphaT:
		source = "AlphaT"
	elif args.dilepton:
		source = "DiLeptonTrigger"
		modifier = "DiLeptonTrigger"
	else:
		source = baselineTrigger.name
	log.logHighlighted("Calculating trigger efficiencies on %s triggered dataset"%source)
	log.logHighlighted("Using trees from %s "%path)
	
	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
		if args.mc:
			cmsExtra = "#splitline{Private Work}{Simulation}"
	elif args.mc:
		cmsExtra = "Simulation"	
	else:
		cmsExtra = "Preliminary"	
	
	if args.tight:
		path = locations.baseTreesDataSetPath
		source = "baseTreesDiLeptonTrigger"
		source2 = "DiLeptonTrigger"
		path2 = locations.triggerDataSetPathMC
	else:
		source2 = ""
		path2 = ""
		
	if args.constantConeSize:
		if args.effectiveArea:
			source = "EffAreaIso%s"%source
		elif args.deltaBeta:
			source = "DeltaBetaIso%s"%source
		else:
			print "Constant cone size (option -R) can only be used in combination with effective area (-e) or delta beta (-D) pileup corrections."
			print "Using default miniIso cone with PF weights instead"
	else:
		if args.effectiveArea:
			source = "MiniIsoEffAreaIso%s"%source
		elif args.deltaBeta:
			source = "MiniIsoDeltaBetaIso%s"%source
		else:
			source = "MiniIsoPFWeights%s"%source

	
	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)
			

			
			if args.central:
				centralVal = centralValues(source,modifier,path,selection,runRange,args.mc,args.backgrounds,args.ptCut,args.tight,source2,path2)
				if args.mc:
					if args.tight:
						outFilePkl = open("shelves/triggerEff_%s_%s_%s_%s_MC_tight.pkl"%(selection.name,source,runRange.label,args.ptCut),"w")
					else:
						outFilePkl = open("shelves/triggerEff_%s_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label,args.ptCut),"w")
				else:
					outFilePkl = open("shelves/triggerEff_%s_%s_%s_%s.pkl"%(selection.name,source,runRange.label,args.ptCut),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(source,modifier,path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.ptCut,args.tight,source2,path2)	
			
			if args.bias:
				studyTriggerBias(path,source,args.plots,selection,runRange,args.backgrounds,cmsExtra)
			if args.trailing:
				singleLepton(path,selection,runRange,args.backgrounds,cmsExtra)		
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/triggerEff_%s_%s_%s_MC.pkl %s/shelves"%(selection.name,source,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves/triggerEff_%s_%s_%s.pkl %s/shelves"%(selection.name,source,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())								
				
main()
