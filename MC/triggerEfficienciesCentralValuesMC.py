### Calculates efficiencies of DiLepton Triggers in HT of alphaT triggered events
from messageLogger import messageLogger as log

from ConfigParser import ConfigParser
from array import array
import math
from defs import mainConfig
from defs import dependendies
from defs import selections, Backgrounds
import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1
from setTdrStyle import setTDRStyle
from helpers import readTrees, createHistoFromTree, TheStack, Process, Plot, totalNumberOfGeneratedEvents

config = ConfigParser()
config.read("/user/schomakers/SubmitScripts/Input/Master53X.ini")


baseCut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20 && p4.M()>20 && ht > 200  && %s)"
baseCutExclusive = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20 && p4.M()>20 && ht > 200 && !(nJets >= 2 && met > 100) && %s)"
cutStrings = {
		"Inclusive":baseCut%("((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && %s"),
		"Barrel":baseCut%("abs(eta1)<1.4  && abs(eta2) < 1.4 && %s"),
		"Endcap":baseCut%("1.6<=TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && %s")
	}
cutStringsExclusive = {
		"Inclusive":baseCutExclusive%("((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && %s"),
		"Barrel":baseCutExclusive%("abs(eta1)<1.4  && abs(eta2) < 1.4 && %s"),
		"Endcap":baseCutExclusive%("1.6<=TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && %s")
	}



def getCounts(nominatorHisto, denominatorHisto,cutString):
	eff = TGraphAsymmErrors(nominatorHisto,denominatorHisto,"cp")

	n= {
		"Nominator": nominatorHisto.Integral(),
		"Denominator": denominatorHisto.Integral(),
		"Efficiency": nominatorHisto.Integral()/denominatorHisto.Integral(),
		"UncertaintyUp": eff.	GetErrorYhigh(0),
		"UncertaintyDown": eff.	GetErrorYlow(0),
		}
	print  n
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
		#~ print pointY1
		#~ print pointY2


		if pointX2!=0:
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

if (__name__ == "__main__"):
	from sys import argv
	import pickle
	if len(argv) ==1:
		log.logHighlighted("No lepton eta selection specified, using inclusive!")
		region = "Inclusive"
	else:
		region = argv[1]
		
	path = mainConfig.path
	source = mainConfig.source
	log.logHighlighted("Calculating trigger efficiencies on %s triggered dataset"%source)
	log.logHighlighted("Using trees from %s "%path)
	treesDenominatorEE = readTrees(path,source,"%s"%(source,),"EE")
	treesDenominatorMuMu = readTrees(path,source,"%s"%(source,),"MuMu")
	treesDenominatorEMu = readTrees(path,source,"%s"%(source,),"EMu")
	
	
	treesNominatorEE = readTrees(path,source,"HLTDiEle%s"%(source,),"EE")
	treesNominatorMuMu = readTrees(path,source,"HLTDiMu%s"%(source,),"MuMu")
	treesNominatorMuMuNoTrack = readTrees(path,source,"HLTDiMuNoTrackerMuon%s"%(source,),"MuMu")
	treesNominatorEMu = readTrees(path,source,"HLTEleMu%s"%(source,),"EMu")
	treesNominatorMuE = readTrees(path,source,"HLTMuEle%s"%(source,),"EMu")
	treesNominatorMuEG = readTrees(path,source,"HLTMuEG%s"%(source,),"EMu")
	

	
	cuts = mainConfig.cuts
	variables = mainConfig.variables
	runs = mainConfig.runs

	eventCounts = totalNumberOfGeneratedEvents(path,source,"%s"%(source,))

	TTJets = Process(Backgrounds.TTJets.subprocesses,eventCounts,Backgrounds.TTJets.label,Backgrounds.TTJets.fillcolor,Backgrounds.TTJets.linecolor,Backgrounds.TTJets.uncertainty,1)	
	TT = Process(Backgrounds.TT.subprocesses,eventCounts,Backgrounds.TT.label,Backgrounds.TT.fillcolor,Backgrounds.TT.linecolor,Backgrounds.TT.uncertainty,1)	
	#~ TT_MCatNLO = Process(Backgrounds.TT_MCatNLO.subprocesses,eventCounts,Backgrounds.TT_MCatNLO.label,Backgrounds.TT_MCatNLO.fillcolor,Backgrounds.TT_MCatNLO.linecolor,Backgrounds.TT_MCatNLO.uncertainty,1)	
	Diboson = Process(Backgrounds.Diboson.subprocesses,eventCounts,Backgrounds.Diboson.label,Backgrounds.Diboson.fillcolor,Backgrounds.Diboson.linecolor,Backgrounds.Diboson.uncertainty,1)	
	Rare = Process(Backgrounds.Rare.subprocesses,eventCounts,Backgrounds.Rare.label,Backgrounds.Rare.fillcolor,Backgrounds.Rare.linecolor,Backgrounds.Rare.uncertainty,1)	
	DY = Process(Backgrounds.DrellYan.subprocesses,eventCounts,Backgrounds.DrellYan.label,Backgrounds.DrellYan.fillcolor,Backgrounds.DrellYan.linecolor,Backgrounds.DrellYan.uncertainty,1)	
	SingleTop = Process(Backgrounds.SingleTop.subprocesses,eventCounts,Backgrounds.SingleTop.label,Backgrounds.SingleTop.fillcolor,Backgrounds.SingleTop.linecolor,Backgrounds.SingleTop.uncertainty,1)	

	processes = [TT,Diboson,Rare,DY,SingleTop]
	#~ processes = [Rare]

	lumi = 9200
	
			
	
	for run in runs:
		log.logInfo("%s"%run.label)
		
		

		lineTemplate = r"%(title)50s & $%(EE).1f\pm%(totalsEE).1f$ &$ %(MuMu).1f\pm%(totalsMuMu).1f$ &$ %(EMu).1f\pm%(totalsEMu).1f$ &$ %(nSF).1f\pm%(statSF).1f\pm%(systSF).1f$ &$ %(nOF).1f\pm%(statOF).1f\pm%(systOF).1f$& $%(nS)3.1f\pm%(statS).1f\pm%(systS).1f$ \\"+"\n"
		
		cutString = cutStrings[region]%(run.runCut)
		print cutString
		
		firstBin = 20
		counts = {run.label:{}}
		#~ if "eta" in variable.variable:
			#~ firstBin = -2.4
		lastBin = 1000
		nBins = 1
		plot = Plot("pt1",cutString,"bla","Efficiency",nBins,firstBin,lastBin)

		denominatorStackEE = TheStack(processes,lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
		denominatorStackMuMu = TheStack(processes,lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
		#~ denominatorStackEMu = TheStack(processes,lumi,plotEMu,treesDenominatorEMu,"None",1.0,1.0,1.0)	
		#~ denominatorStackMuE = TheStack(processes,lumi,plotMuE,treesDenominatorEMu,"None",1.0,1.0,1.0)	
		denominatorStackMuEG = TheStack(processes,lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
			
		nominatorStackEE = TheStack(processes,lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
		nominatorStackMuMu = TheStack(processes,lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)		
		#~ nominatorStackMuMuNoTrack = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
		#~ nominatorStackEMu = TheStack(processes,lumi,plotEMu,treesNominatorEMu,"None",1.0,1.0,1.0)		
		#~ nominatorStackMuE = TheStack(processes,lumi,plotMuE,treesNominatorMuE,"None",1.0,1.0,1.0)		
		nominatorStackMuEG = TheStack(processes,lumi,plot,treesNominatorMuEG,"None",1.0,1.0,1.0)		

		denominatorHistoEE = denominatorStackEE.theHistogram
		print denominatorHistoEE.GetEntries()
		denominatorHistoMuMu = denominatorStackMuMu.theHistogram
		#~ denominatorHistoEMu = denominatorStackEMu.theHistogram
		#~ denominatorHistoMuE = denominatorStackMuE.theHistogram
		denominatorHistoMuEG = denominatorStackMuEG.theHistogram
		
		nominatorHistoEE = nominatorStackEE.theHistogram
		nominatorHistoMuMu = nominatorStackMuMu.theHistogram
		#~ nominatorHistoMuMuNoTrack = nominatorStackMuMuNoTrack.theHistogram
		#~ nominatorHistoEMu = nominatorStackEMu.theHistogram
		#~ nominatorHistoMuE = nominatorStackMuE.theHistogram
		nominatorHistoMuEG = nominatorStackMuEG.theHistogram						
		
		counts[run.label]["default"] = {}
		
		counts[run.label]["default"]["EE"] = getCounts(nominatorHistoEE, denominatorHistoEE,cutString)
		counts[run.label]["default"]["MuMu"] = getCounts(nominatorHistoMuMu, denominatorHistoMuMu,cutString)
		counts[run.label]["default"]["EMu"] = getCounts(nominatorHistoMuEG, denominatorHistoMuEG,cutString)
		
		
		outFilePkl = open("shelves/triggerEff_%s_%s_%s.pkl"%(region,source,run.label),"w")
		pickle.dump(counts, outFilePkl)
		outFilePkl.close()		
		
				
		cutString = cutStringsExclusive[region]%(run.runCut)
		print cutString
		
		firstBin = 20
		counts = {run.label:{}}
		#~ if "eta" in variable.variable:
			#~ firstBin = -2.4
		lastBin = 1000
		nBins = 1
		plot = Plot("pt1",cutString,"bla","Efficiency",nBins,firstBin,lastBin)

		denominatorStackEE = TheStack(processes,lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
		denominatorStackMuMu = TheStack(processes,lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
		#~ denominatorStackEMu = TheStack(processes,lumi,plotEMu,treesDenominatorEMu,"None",1.0,1.0,1.0)	
		#~ denominatorStackMuE = TheStack(processes,lumi,plotMuE,treesDenominatorEMu,"None",1.0,1.0,1.0)	
		denominatorStackMuEG = TheStack(processes,lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
			
		nominatorStackEE = TheStack(processes,lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
		nominatorStackMuMu = TheStack(processes,lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)		
		#~ nominatorStackMuMuNoTrack = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
		#~ nominatorStackEMu = TheStack(processes,lumi,plotEMu,treesNominatorEMu,"None",1.0,1.0,1.0)		
		#~ nominatorStackMuE = TheStack(processes,lumi,plotMuE,treesNominatorMuE,"None",1.0,1.0,1.0)		
		nominatorStackMuEG = TheStack(processes,lumi,plot,treesNominatorMuEG,"None",1.0,1.0,1.0)		

		denominatorHistoEE = denominatorStackEE.theHistogram
		print denominatorHistoEE.GetEntries()
		denominatorHistoMuMu = denominatorStackMuMu.theHistogram
		#~ denominatorHistoEMu = denominatorStackEMu.theHistogram
		#~ denominatorHistoMuE = denominatorStackMuE.theHistogram
		denominatorHistoMuEG = denominatorStackMuEG.theHistogram
		
		nominatorHistoEE = nominatorStackEE.theHistogram
		nominatorHistoMuMu = nominatorStackMuMu.theHistogram
		#~ nominatorHistoMuMuNoTrack = nominatorStackMuMuNoTrack.theHistogram
		#~ nominatorHistoEMu = nominatorStackEMu.theHistogram
		#~ nominatorHistoMuE = nominatorStackMuE.theHistogram
		nominatorHistoMuEG = nominatorStackMuEG.theHistogram						
		
		counts[run.label]["default"] = {}
		
		counts[run.label]["default"]["EE"] = getCounts(nominatorHistoEE, denominatorHistoEE,cutString)
		counts[run.label]["default"]["MuMu"] = getCounts(nominatorHistoMuMu, denominatorHistoMuMu,cutString)
		counts[run.label]["default"]["EMu"] = getCounts(nominatorHistoMuEG, denominatorHistoMuEG,cutString)
		
		
		outFilePkl = open("shelves/triggerEffExclusive_%s_%s_%s.pkl"%(region,source,run.label),"w")
		pickle.dump(counts, outFilePkl)
		outFilePkl.close()				
