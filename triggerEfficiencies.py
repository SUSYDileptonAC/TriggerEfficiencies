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
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, createHistoFromTree, TheStack, totalNumberOfGeneratedEvents, Process


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


def getHistograms(path,source,plot,runRange,isMC,backgrounds):
	


	
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
				denominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,cutStringEE,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin).Clone())		
			denominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,cutStringEMu,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,cutStringMuE,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())


			nominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEE.iteritems():
				nominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,cutStringEE,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMu.iteritems():
				nominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMuNoTrack.iteritems():
				nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,cutStringMuMu,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuE.iteritems():
				nominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,cutStringMuE,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEMu.iteritems():
				nominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,cutStringEMu,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuEG.iteritems():
				nominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			
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
				denominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())		
			denominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorMuMu.iteritems():
				denominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			denominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesDenominatorEMu.iteritems():
				denominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())




			nominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEE.iteritems():
				nominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMu.iteritems():
				nominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuMuNoTrack = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuMuNoTrack.iteritems():
				nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuE.iteritems():
				nominatorHistoMuE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoEMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorEMu.iteritems():
				nominatorHistoEMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
			nominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
			for name, tree in treesNominatorMuEG.iteritems():
				nominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
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

def centralValues(source,path,selection,runRange,isMC,backgrounds):
	
	
	err = 0.05
	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		
	plot.firstBin = 20
	plot.lastBin = 10000
	plot.nBins = 1
	
	counts = {runRange.label:{}}	
								
	denominators, nominators = getHistograms(path,source,plot,runRange,isMC,backgrounds)
	
	counts[runRange.label]["EE"] = getEfficiency(nominators["EE"], denominators["EE"],plot.cuts)
	counts[runRange.label]["MuMu"] = getEfficiency(nominators["MuMu"], denominators["MuMu"],plot.cuts)
	counts[runRange.label]["MuMuNoTrack"] = getEfficiency(nominators["MuMuNoTrack"], denominators["MuMuNoTrack"],plot.cuts)
	counts[runRange.label]["EMu"] = getEfficiency(nominators["MuEG"], denominators["MuEG"],plot.cuts)
	print counts[runRange.label]["EE"]
	counts[runRange.label]["RT"] = (counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**0.5 / counts[runRange.label]["EMu"]["Efficiency"]
	counts[runRange.label]["RTErrSyst"] =  (err**2/(2*counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**2+ err**2/(2*counts[runRange.label]["MuMu"]["Efficiency"]*counts[runRange.label]["EE"]["Efficiency"])**2 + err**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5
	counts[runRange.label]["RTErrStat"] =  (max(counts[runRange.label]["EE"]["UncertaintyUp"],counts[runRange.label]["EE"]["UncertaintyDown"])**2/(2*counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**2+ max(counts[runRange.label]["MuMu"]["UncertaintyUp"],counts[runRange.label]["MuMu"]["UncertaintyDown"])**2/(2*counts[runRange.label]["MuMu"]["Efficiency"]*counts[runRange.label]["EE"]["Efficiency"])**2 + max(counts[runRange.label]["EMu"]["UncertaintyUp"],counts[runRange.label]["EMu"]["UncertaintyDown"])**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5

	return counts



def dependencies(source,path,selection,plots,runRange,isMC,backgrounds):

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
	legendHist3.SetMarkerColor(ROOT.kRed+2)
	legendHist4.SetMarkerColor(ROOT.kBlue)
	legendHist5.SetMarkerColor(ROOT.kBlue+2)
	
	legend.AddEntry(legendHist1,"Ele_17_X_Ele8_X","p")
	legend.AddEntry(legendHist2,"Mu17_Mu8 or Mu17_TkMu8","p")
	legend.AddEntry(legendHist3,"Mu17_Mu8","p")
	legend.AddEntry(legendHist4,"Mu17_Ele8_X","p")
	legend.AddEntry(legendHist5,"Ele17_X_Mu8","p")
	
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
	if isMC:
		if os.path.isfile("shelves/triggerEff_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label)):
			centralVals = pickle.load(open("shelves/triggerEff_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label),"rb"))
		else:
			centralVals = centralValues(source,path,selection,runRange,isMC)
	else:
		if os.path.isfile("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label)):
			centralVals = pickle.load(open("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label),"rb"))
		else:
			centralVals = centralValues(source,path,selection,runRange,isMC)
	
				
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		#~ plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut	

		if  "Forward" in selection.name:
			plot.nBins = int(variable.nBins/2)
		denominators, nominators = getHistograms(path,source,plot,runRange,isMC,backgrounds)
		
		


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
		legend.AddEntry(effMuMu,"Mu17_Mu8 || Mu17_TkMu8","p")
		legend.AddEntry(effMuE,"Mu17_Ele8_X","p")
		legend.AddEntry(effEMu,"Ele17_X_Mu8","p")

		
		effEE.Draw("samep")
		effMuMu.Draw("samep")
		#~ effMuMuNoTrack.Draw("samep")
		effMuE.Draw("samep")
		effEMu.Draw("samep")

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		cmsExtra = "Private Work"

		latexCMS.DrawLatex(0.15,0.955,"CMS")
		latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))
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
		legend.AddEntry(effSF,"Ele_17_X_Ele8_X || Mu17_Mu8 || Mu17_TkMu8 ","p")
		legend.AddEntry(effOF,"Mu17_Ele8_X || Ele17_X_Mu8" ,"p")

		effSF.Draw("samep")
		effOF.Draw("samep")


		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		cmsExtra = "Private Work"

		latexCMS.DrawLatex(0.15,0.955,"CMS")
		latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))
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
		cmsExtra = "Private Work"

		latexCMS.DrawLatex(0.15,0.955,"CMS")
		latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))			

		
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
			
			
def studyTriggerBias(path,source,plots,selection,runRange,backgrounds):			
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
		legendHist3.SetMarkerColor(ROOT.kRed+2)
		legendHist4.SetMarkerColor(ROOT.kBlue)
		legendHist5.SetMarkerColor(ROOT.kBlue+2)
		
		legend.AddEntry(legendHist1,"Ele_17_X_Ele8_X","p")
		legend.AddEntry(legendHist2,"Mu17_Mu8 || Mu17_TkMu8","p")
		legend.AddEntry(legendHist3,"Mu17_Mu8","p")
		legend.AddEntry(legendHist4,"Mu17_Ele8_X","p")
		legend.AddEntry(legendHist5,"Ele17_X_Mu8","p")
		
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
		cmsExtra = "Simulation Private Work"

		latexCMS.DrawLatex(0.15,0.955,"CMS")
		latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))
		legend.Draw("same")
		print source
		if source == "HT" or source == "AlphaT":
			hCanvas.Print("fig/Triggereff_AlphaTSyst_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/Triggereff_AlphaTSyst_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))								
				


def singleLepton(path,selection,runRange,backgrounds):
	
	
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
	cmsExtra = "Private Work"

	latexCMS.DrawLatex(0.15,0.955,"CMS")
	latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))			
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
	parser.add_argument("-s", "--selection", dest = "selection" , nargs=1, default=["HighHTExclusive"],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", nargs=1, default="Full2012",
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")
	parser.add_argument("-w", "--preliminary", dest="preliminary", default=False,
						  help="plot is preliminary.")	
	parser.add_argument("-x", "--private", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-a", "--alphaT", action="store_true", dest="alphaT", default=False,
						  help="use alphaT triggers as baseline.")	
	parser.add_argument("-z", "--bias", action="store_true", dest="bias", default=False,
						  help="produce trigger bias studies.")	
	parser.add_argument("-t", "--trailing", action="store_true", dest="trailing", default=False,
						  help="trailing lepton pt dependence using single lepton trigger.")	
					
	args = parser.parse_args()





	if len(args.backgrounds) == 0:
		args.backgrounds = ["Rare","SingleTop","TTJets_SpinCorrelations","Diboson","DrellYanTauTau","DrellYan"]
	if len(args.plots) == 0:
		args.plots = ["nJetsPlotTrigger","leadingPtPlotTriggerTrailing10","leadingPtPlotTrigger","trailigPtPlotTrigger","trailigPtPlotTriggerLeading30","mllPlotTrigger","htPlotTrigger","metPlotTrigger","nVtxPlotTrigger","tralingEtaPlotTrigger"]
	
	if args.bias:
		args.mc = True
				
	path = pathes.triggerDataSetPath	
	if args.mc:
		path = pathes.triggerDataSetPathMC
	if args.trailing:
		path = pathes.triggerDataSetPathSingleLepton
	if args.alphaT:
		source = "alphaT"
	else:
		source = "PFHT"
	log.logHighlighted("Calculating trigger efficiencies on %s triggered dataset"%source)
	log.logHighlighted("Using trees from %s "%path)
	

	
	runRange = getRunRange(args.runRange)
	
	selection = getRegion(args.selection[0])
	
	if args.central:
		centralVal = centralValues(source,path,selection,runRange,args.mc,args.backgrounds)
		if args.mc:
			outFilePkl = open("shelves/triggerEff_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label),"w")
		else:
			outFilePkl = open("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label),"w")
		pickle.dump(centralVal, outFilePkl)
		outFilePkl.close()
		
	if args.dependencies:
		 dependencies(source,path,selection,args.plots,runRange,args.mc,args.backgrounds)	
	
	if args.bias:
		studyTriggerBias(path,source,args.plots,selection,runRange,args.backgrounds)
	if args.trailing:
		singleLepton(path,selection,runRange,args.backgrounds)				
				
main()
