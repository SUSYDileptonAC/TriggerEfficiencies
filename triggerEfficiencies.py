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
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, kWhite
ROOT.gROOT.SetBatch(True)


from defs import getRegion, getPlot, getRunRange, Backgrounds,theCuts

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
			
		newEff.SetPoint(i,xValue,yValue)
		newEff.SetPointError(i,xError,xError,yErrorDown,yErrorUp)
		
	return newEff
	
def efficiencyRatioGeometricMean(eff1,eff2,eff3,source):
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


		if source == "SingleLepton":
			if pointY3!=0 and pointY2!=0 and pointY3!=0:
				yValue = (pointY1*pointY2)/pointY3**2
				xValue = pointX1
				xError = errX			
				yErrorUp = math.sqrt((errY1Up/pointY1)**2 + (errY2Up/pointY2)**2 + (errY3Up/pointY3)**2)				
				yErrorDown = math.sqrt((errY1Down/pointY1)**2 + (errY2Down/pointY2)**2 + (errY3Down/pointY3)**2)
			else:
				yValue = 0
				xValue = pointX1
				xError = errX
				yErrorUp =0
				yErrorDown = 0
		else:
			if pointY1!=0 and pointY2!=0 and pointY3!=0:
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
			
		newEff.SetPoint(i,xValue,yValue)
		newEff.SetPointError(i,xError,xError,yErrorDown,yErrorUp)
		
	return newEff
	
def efficiencyRatioSF(eff1,eff2,):
	newEff = TGraphAsymmErrors(eff1.GetN())
	for i in range(0,eff1.GetN()):
		pointX1 = ROOT.Double(0.)
		pointX2 = ROOT.Double(0.)
		pointY1 = ROOT.Double(0.)
		pointY2 = ROOT.Double(0.)
		
		isSuccesful1 = eff1.GetPoint(i,pointX1,pointY1)
		isSuccesful2 = eff2.GetPoint(i,pointX2,pointY2)
		errY1Up = eff1.GetErrorYhigh(i)
		errY1Down = eff1.GetErrorYlow(i)
		errY2Up = eff2.GetErrorYhigh(i)
		errY2Down = eff2.GetErrorYlow(i)
		
		errX = eff1.GetErrorX(i)
		
		if pointY1!=0 and pointY2!=0:
			yValue = pointY1/pointY2
			xValue = pointX1
			xError = errX			
			yErrorUp = math.sqrt( (  1. / pointY2  * errY1Up )**2 + (  pointY1 / pointY2**2  * errY2Down )**2 )				
			yErrorDown = math.sqrt( (  1. / pointY2  * errY1Down )**2 + (  pointY1 / pointY2**2  * errY2Up )**2 )					
		else:
			yValue = 0
			xValue = pointX1
			xError = errX
			yErrorUp =0
			yErrorDown = 0
					
		newEff.SetPoint(i,xValue,yValue)
		newEff.SetPointError(i,xError,xError,yErrorDown,yErrorUp)
		
	return newEff


def getHistograms(path,plot,runRange,isMC,backgrounds,source):
	
	if not isMC:
		treesEE = readTrees(path,"EE",modifier = "TriggerPFHT")
		treesMuMu = readTrees(path,"MuMu", modifier = "TriggerPFHT")
		treesEMu = readTrees(path,"EMu", modifier = "TriggerPFHT")
			
		denominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for name, tree in treesEE.iteritems():
			if name == "MergedData":
				denominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
		denominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for name, tree in treesMuMu.iteritems():
			if name == "MergedData":
				denominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())		
		denominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for name, tree in treesEMu.iteritems():
			if name == "MergedData":
				denominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
				
		cutsEE = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && %s"%theCuts.triggerCuts.EE.cut)
		cutsOF = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && %s"%theCuts.triggerCuts.EM.cut)
		cutsMuMu = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && %s"%theCuts.triggerCuts.MM.cut)


		nominatorHistoEE = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for name, tree in treesEE.iteritems():
			if name == "MergedData":
				nominatorHistoEE.Add(createHistoFromTree(tree,plot.variable,cutsEE,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
		nominatorHistoMuMu = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for name, tree in treesMuMu.iteritems():
			if name == "MergedData":
				nominatorHistoMuMu.Add(createHistoFromTree(tree,plot.variable,cutsMuMu,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
		nominatorHistoMuEG = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for name, tree in treesEMu.iteritems():
			if name == "MergedData":
				nominatorHistoMuEG.Add(createHistoFromTree(tree,plot.variable,cutsOF,plot.nBins,plot.firstBin,plot.lastBin,binning=plot.binning).Clone())
	else:
		treesEE = readTrees(path,"EE")
		treesMuMu = readTrees(path,"MuMu")
		treesEMu = readTrees(path,"EMu")
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		nominatorStackEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,useTriggerEmulation=True)	
		nominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesMuMu,"None",1.0,1.0,1.0,useTriggerEmulation=True)
		nominatorStackMuEG = TheStack(processes,runRange.lumi,plot,treesEMu,"None",1.0,1.0,1.0,useTriggerEmulation=True)
		
		denominatorStackEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0)		
		denominatorStackMuMu = TheStack(processes,runRange.lumi,plot,treesMuMu,"None",1.0,1.0,1.0)	
		denominatorStackMuEG = TheStack(processes,runRange.lumi,plot,treesEMu,"None",1.0,1.0,1.0)	
			
		denominatorHistoEE = denominatorStackEE.theHistogram
		denominatorHistoMuMu = denominatorStackMuMu.theHistogram
		denominatorHistoMuEG = denominatorStackMuEG.theHistogram
		
		nominatorHistoEE = nominatorStackEE.theHistogram
		nominatorHistoMuMu = nominatorStackMuMu.theHistogram
		nominatorHistoMuEG = nominatorStackMuEG.theHistogram
			
		
	return {"EE":denominatorHistoEE,"MuMu":denominatorHistoMuMu,"MuEG":denominatorHistoMuEG} , {"EE":nominatorHistoEE,"MuMu":nominatorHistoMuMu ,"MuEG":nominatorHistoMuEG}

def centralValues(source,path,selection,runRange,isMC,backgrounds):
	
	
	if "Central" in selection.name:
		err = systematics.trigger.central.val
	elif "Forward" in selection.name:
		err = systematics.trigger.forward.val
	else:
		err = systematics.trigger.inclusive.val
	
	#~ print selection
	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		
	plot.firstBin = 20
	plot.lastBin = 10000
	plot.nBins = 1
	plot.cuts = plot.cuts.replace("mll","p4.M()")
	plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")	
	plot.cuts = plot.cuts.replace("triggerSummary > 0 &&","")	
	plot.variable = plot.variable.replace("mll","p4.M()")
	if 	plot.variable == "pt":
		plot.variable = plot.variable.replace("pt","p4.Pt()")
	
	counts = {runRange.label:{}}	

	denominators, nominators = getHistograms(path,plot,runRange,isMC,backgrounds,source)
	
	counts[runRange.label]["EE"] = getEfficiency(nominators["EE"], denominators["EE"],plot.cuts)
	counts[runRange.label]["MuMu"] = getEfficiency(nominators["MuMu"], denominators["MuMu"],plot.cuts)
	counts[runRange.label]["EMu"] = getEfficiency(nominators["MuEG"], denominators["MuEG"],plot.cuts)
	counts[runRange.label]["RT"] = (counts[runRange.label]["EE"]["Efficiency"]*counts[runRange.label]["MuMu"]["Efficiency"])**0.5 / counts[runRange.label]["EMu"]["Efficiency"]
	counts[runRange.label]["RTErrSyst"] =  counts[runRange.label]["RT"]*(err**2/(2*counts[runRange.label]["MuMu"]["Efficiency"])**2+ err**2/(2*counts[runRange.label]["EE"]["Efficiency"])**2 + err**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5
	counts[runRange.label]["RTErrStat"] =  counts[runRange.label]["RT"]*(max(counts[runRange.label]["EE"]["UncertaintyUp"],counts[runRange.label]["EE"]["UncertaintyDown"])**2/(2*counts[runRange.label]["EE"]["Efficiency"])**2+ max(counts[runRange.label]["MuMu"]["UncertaintyUp"],counts[runRange.label]["MuMu"]["UncertaintyDown"])**2/(2*counts[runRange.label]["MuMu"]["Efficiency"])**2 + max(counts[runRange.label]["EMu"]["UncertaintyUp"],counts[runRange.label]["EMu"]["UncertaintyDown"])**2/(counts[runRange.label]["EMu"]["Efficiency"])**2)**0.5

	return counts



def dependencies(source,path,selection,plots,runRange,isMC,backgrounds,cmsExtra):

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	

	legend = TLegend(0.575, 0.16, 0.9, 0.4)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	
	legendHist1 = TH1F()
	legendHist2 = TH1F()
	legendHist3 = TH1F()
	
	legendHist1.SetMarkerColor(ROOT.kBlack)
	legendHist2.SetMarkerColor(ROOT.kRed)
	legendHist3.SetMarkerColor(ROOT.kBlue)
	
	legend.AddEntry(legendHist1,"ee","p")
	legend.AddEntry(legendHist2,"#mu#mu","p")
	legend.AddEntry(legendHist3,"e#mu","p")
	
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
	latexSelection = ROOT.TLatex()
	#~ latexSelection.SetTextFont(42)
	latexSelection.SetTextSize(0.03)
	latexSelection.SetNDC(True)		
	


	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)		
	if isMC:
		if os.path.isfile("shelves/triggerEff_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label)):
			centralVals = pickle.load(open("shelves/triggerEff_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label),"rb"))
		else:
			centralVals = centralValues(source,path,selection,runRange,isMC,backgrounds)
		if os.path.isfile("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label)):
			centralValsData = pickle.load(open("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label),"rb"))
		else:
			centralValsData = centralValues(source,path,selection,runRange,False,backgrounds)
	else:
		if os.path.isfile("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label)):
			centralVals = pickle.load(open("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label),"rb"))
		else:
			centralVals = centralValues(source,path,selection,runRange,isMC,backgrounds)
		
				
	
	for name in plots:
		if isMC:
			plotData = getPlot(name)
			plotData.addRegion(selection)
			#~ plot.cleanCuts()
			plotData.cuts = plotData.cuts % runRange.runCut
			plotData.cuts = plotData.cuts.replace("mll","p4.M()")
			plotData.cuts = plotData.cuts.replace("pt > 25","p4.Pt() > 25")
			plotData.cuts = plotData.cuts.replace("triggerSummary > 0 &&","")
			plotData.variable = plotData.variable.replace("mll","p4.M()")
			if 	plotData.variable == "pt":	
				plotData.variable = plotData.variable.replace("pt","p4.Pt()")	
	
			name = name+"MC"
		plot = getPlot(name)
		plot.addRegion(selection)
		#~ plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut
		plot.cuts = plot.cuts.replace("mll","p4.M()")
		plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
		plot.cuts = plot.cuts.replace("triggerSummary > 0 &&","")
		plot.variable = plot.variable.replace("mll","p4.M()")
		if 	plot.variable == "pt":	
			plot.variable = plot.variable.replace("pt","p4.Pt()")	
		
		
		#~ if  "Forward" in selection.name:
			#~ plot.nBins = int(plot.nBins/2)
		denominators, nominators = getHistograms(path,plot,runRange,isMC,backgrounds,source)
		
		effEE = TGraphAsymmErrors(nominators["EE"],denominators["EE"],"cp")
		effMuMu = TGraphAsymmErrors(nominators["MuMu"],denominators["MuMu"],"cp")

		denominatorHistoOF = denominators["MuEG"].Clone()
		nominatorHistoOF = nominators["MuEG"].Clone()
		effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cp")
		
		if isMC:
			denominatorsData, nominatorsData = getHistograms(locations.triggerDataSetPath,plotData,runRange,False,backgrounds,source)	
		
			effEEData = TGraphAsymmErrors(nominatorsData["EE"],denominatorsData["EE"],"cp")
			effMuMuData = TGraphAsymmErrors(nominatorsData["MuMu"],denominatorsData["MuMu"],"cp")

			denominatorHistoOFData = denominatorsData["MuEG"].Clone()
			nominatorHistoOFData = nominatorsData["MuEG"].Clone()
			effOFData = TGraphAsymmErrors(nominatorHistoOFData,denominatorHistoOFData,"cp")
			
		

		effEE.SetMarkerColor(ROOT.kBlack)
		effMuMu.SetMarkerColor(ROOT.kRed)
		effOF.SetMarkerColor(ROOT.kBlue)
		effEE.SetLineColor(ROOT.kBlack)
		effMuMu.SetLineColor(ROOT.kRed)
		effOF.SetLineColor(ROOT.kBlue)
		effEE.SetMarkerStyle(20)
		effMuMu.SetMarkerStyle(21)
		effOF.SetMarkerStyle(22)	
					
		plotPad.DrawFrame(plot.firstBin,0.5,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
		
		selectionLabel = selection.latex
		
		if plot.variable == "nJets":
			selectionLabel = selectionLabel.replace("#notin (n_{jets}#geq 2 & p_{T}^{miss} > 100 GeV)", "p_{T}^{miss} < 100 GeV")
		if plot.variable == "met":
			selectionLabel = selectionLabel.replace("#notin (n_{jets}#geq 2 & p_{T}^{miss} > 100 GeV)", "n_{jets}=1")
		

		
		legend.Clear()
				
		
		legend.AddEntry(effEE,"ee","p")
		legend.AddEntry(effMuMu,"#mu#mu","p")
		legend.AddEntry(effOF,"e#mu","p")

		
		effEE.Draw("samep")
		effMuMu.Draw("samep")
		effOF.Draw("samep")
		
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	
		#~ yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		latexSelection.DrawLatex(0.20,0.25,selectionLabel)
		
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
		
		nominatorHistoOF = nominators["MuEG"].Clone()
		
		effSF = TGraphAsymmErrors(nominatorHistoSF,denominatorHistoSF,"cp")
		effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cp")



		effSF.SetMarkerColor(ROOT.kBlack)
		effOF.SetMarkerColor(ROOT.kBlue)
		effSF.SetLineColor(ROOT.kBlack)
		effOF.SetLineColor(ROOT.kBlue)
		effSF.SetMarkerStyle(20)
		effOF.SetMarkerStyle(22)
		
		effSFNoFit = effSF.Clone()
		effOFNoFit = effSF.Clone()
		
	
		plotPad.DrawFrame(plot.firstBin,0.5,plot.lastBin,1.2,"; %s ; Efficiency" %(plot.xaxis))
		

		legend.Clear()
					
		legend.AddEntry(effSF,"ee and #mu#mu","p")
		legend.AddEntry(effOF,"e#mu" ,"p")

		effSF.Draw("samep")
		effOF.Draw("samep")


		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	
		#~ yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		latexSelection.DrawLatex(0.20,0.25,selectionLabel)
		legend.Draw("same")
		if isMC:
			hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
		else:	
			hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))

		if source == "SingleLepton":
			plotPad.DrawFrame(plot.firstBin,.6,plot.lastBin,1.4,"; %s ; R_{T}" %(plot.xaxis))
		else:
			plotPad.DrawFrame(plot.firstBin,.6,plot.lastBin,1.4,"; %s ; R_{T}" %(plot.xaxis))

		
		effSFvsOF = efficiencyRatioGeometricMean(effEE,effMuMu,effOF,source)
		if isMC:
			effSFvsOFData = efficiencyRatioGeometricMean(effEEData,effMuMuData,effOFData,source)
			effSFvsOF.SetLineColor(ROOT.kGreen-2)
			effSFvsOF.SetMarkerColor(ROOT.kGreen-2)
			effSFvsOF.SetMarkerStyle(21)
			
		x= array("f",[plot.firstBin, plot.lastBin]) 
		if isMC:
			yData= array("f", [float(centralValsData[runRange.label]["RT"]), float(centralValsData[runRange.label]["RT"])]) 
			sfLineData= ROOT.TF1("sfLine",str(centralValsData[runRange.label]["RT"]),plot.firstBin, plot.lastBin)
		y= array("f", [float(centralVals[runRange.label]["RT"]), float(centralVals[runRange.label]["RT"])]) 
		sfLine= ROOT.TF1("sfLine",str(centralVals[runRange.label]["RT"]),plot.firstBin, plot.lastBin)
		if isMC:
			eyData= array("f", [float(centralValsData[runRange.label]["RTErrSyst"]), float(centralValsData[runRange.label]["RTErrSyst"])])					
			eyData= array("f", [float(centralVals[runRange.label]["RTErrSyst"]), float(centralVals[runRange.label]["RTErrSyst"])])					
			exData= array("f", [0.,0.])
			
			ge= ROOT.TGraphErrors(2, x, yData, exData, eyData)
			ge.SetFillColor(ROOT.kOrange-9)
			ge.SetFillStyle(1001)
			ge.SetLineColor(ROOT.kWhite)
			ge.Draw("SAME 3")
		else:	
			ey= array("f", [float(centralVals[runRange.label]["RTErrSyst"]), float(centralVals[runRange.label]["RTErrSyst"])])					
			ex= array("f", [0.,0.])
			
			ge= ROOT.TGraphErrors(2, x, y, ex, ey)
			ge.SetFillColor(ROOT.kOrange-9)
			ge.SetFillStyle(1001)
			ge.SetLineColor(ROOT.kWhite)
			ge.Draw("SAME 3")
		
		
		effSFvsOF.Draw("samep")
		if isMC:
			effSFvsOFData.Draw("samep")
		
		
		sfLine.SetLineColor(ROOT.kGreen-2)
		sfLine.SetLineWidth(3)
		sfLine.SetLineStyle(2)
		sfLine.Draw("SAME")		
		
		if isMC:		
			sfLineData.SetLineColor(ROOT.kBlack)
			sfLineData.SetLineWidth(3)
			sfLineData.SetLineStyle(2)
			sfLineData.Draw("SAME")				
		
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			#~ cmsExtra = "Preliminary"
			cmsExtraLabel = cmsExtra.replace("#splitline{Private Work}{Simulation}","Private Work")
			#~ yLabelPos = 0.84	
		else:
			#~ yLabelPos = 0.84
			cmsExtraLabel = cmsExtra	
		yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtraLabel))	
		
		
		legend.Clear()
								
		if isMC:
			legend.AddEntry(effSFvsOF,"R_{T} MC","p")
			legend.AddEntry(effSFvsOFData,"R_{T} Data","p")
		else:
			legend.AddEntry(effSFvsOF,"R_{T}","p")
		if isMC:		
			legend.AddEntry(sfLine,"Mean R_{T} MC: %.3f"%(centralVals[runRange.label]["RT"]),"l") 
			legend.AddEntry(sfLineData,"Mean R_{T} Data: %.3f"%(centralValsData[runRange.label]["RT"]),"l") 
		else:
			legend.AddEntry(sfLine,"Mean R_{T}: %.3f"%(centralVals[runRange.label]["RT"]),"l") 
				
		legend.AddEntry(ge,"syst. uncert. Data","f") 
		legend.Draw("same")		
		latexSelection.DrawLatex(0.20,0.25,selectionLabel)
		ROOT.gPad.RedrawAxis()
		if isMC:
			hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s_MC.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))		
		else:
			hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s.pdf"%(source,selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
			
			
			
def main():


	parser = argparse.ArgumentParser(description='Trigger efficiency measurements.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="use MC, default is to use data.")
	parser.add_argument("-n", "--new", action="store_true", dest="new", default=False,
						  help="new approach, using single lepton for dependencies.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", action ="append", default=[],
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")								
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
				
	path = locations.triggerDataSetPath	
	if args.mc:
		path = locations.dataSetPath

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
	

	
	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)
			

			
			if args.central:
				centralVal = centralValues(source,path,selection,runRange,args.mc,args.backgrounds)	
				if args.mc:
					outFilePkl = open("shelves/triggerEff_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label),"w")
				else:
					outFilePkl = open("shelves/triggerEff_%s_%s_%s.pkl"%(selection.name,source,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(source,path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra)	
				
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/triggerEff_%s_%s_%s_MC.pkl %s/shelves"%(selection.name,source,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves/triggerEff_%s_%s_%s.pkl %s/shelves"%(selection.name,source,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())								
					
main()
