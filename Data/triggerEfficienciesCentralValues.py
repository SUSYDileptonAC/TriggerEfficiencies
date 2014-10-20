### Calculates efficiencies of DiLepton Triggers in HT of alphaT triggered events
from messageLogger import messageLogger as log

import math
from defs import mainConfig
from defs import dependendies
from defs import selections
import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1
from setTdrStyle import setTDRStyle
from helpers import readTrees, createHistoFromTree
from array import array

baseCut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20 && p4.M()>20 && ht > 200  && %s)"
baseCutExclusive = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20 && p4.M()>20 && ht > 200 && !(nJets >= 2 && met > 100) && %s)"
baseCutExclusiveNoHT = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20 && p4.M()>20 && !(nJets >= 2 && met > 100) && %s)"
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
cutStringsExclusiveNoHT = {
		"Inclusive":baseCutExclusiveNoHT%("((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && %s"),
		"Barrel":baseCutExclusiveNoHT%("abs(eta1)<1.4  && abs(eta2) < 1.4 && %s"),
		"Endcap":baseCutExclusiveNoHT%("1.6<=TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && %s")
	}



tableTemplate = r"""
\begin{tabular}{l|c|c|c|c}
Run Period & Trigger & $N_{nominator}$ & $N_{denominator}$ & efficiency\\
\hline
%s
\end{tabular}
"""

def getCounts(nominatorHisto, denominatorHisto,cutString):
	eff = TGraphAsymmErrors(nominatorHisto,denominatorHisto,"cp")
	effValue = ROOT.Double(0.)
	blubb = ROOT.Double(0.)
	intttt = eff.GetPoint(0,blubb,effValue)
	print effValue    
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
		#~ print pointY1
		#~ print pointY2


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
	
	if source == "PFHT":
	
		treesDenominatorEE = readTrees(path,source,"%s"%(source,),"EE")
		treesDenominatorMuMu = readTrees(path,source,"%s"%(source,),"MuMu")
		treesDenominatorEMu = readTrees(path,source,"%s"%(source,),"EMu")
		
		
		treesNominatorEE = readTrees(path,source,"%sHLTPFDiEle"%(source,),"EE")
		treesNominatorMuMu = readTrees(path,source,"%sHLTPFDiMu"%(source,),"MuMu")
		treesNominatorMuMuNoTrack = readTrees(path,source,"%sHLTPFDiMuNoTrackerMuon"%(source,),"MuMu")
		treesNominatorEMu = readTrees(path,source,"%sHLTPFEleMu"%(source,),"EMu")
		treesNominatorMuE = readTrees(path,source,"%sHLTPFMuEle"%(source,),"EMu")
		treesNominatorMuEG = readTrees(path,source,"%sHLTPFMuEG"%(source,),"EMu")
	else:
		treesDenominatorEE = readTrees(path,source,"%s"%(source,),"EE")
		treesDenominatorMuMu = readTrees(path,source,"%s"%(source,),"MuMu")
		treesDenominatorEMu = readTrees(path,source,"%s"%(source,),"EMu")
		
		
		treesNominatorEE = readTrees(path,source,"%sHLTDiEle"%(source,),"EE")
		treesNominatorMuMu = readTrees(path,source,"%sHLTDiMu"%(source,),"MuMu")
		treesNominatorMuMuNoTrack = readTrees(path,source,"%sHLTDiMuNoTrackerMuon"%(source,),"MuMu")
		treesNominatorEMu = readTrees(path,source,"%sHLTEleMu"%(source,),"EMu")
		treesNominatorMuE = readTrees(path,source,"%sHLTMuEle"%(source,),"EMu")
		treesNominatorMuEG = readTrees(path,source,"%sHLTMuEG"%(source,),"EMu")			
	cuts = mainConfig.cuts
	variables = mainConfig.variables
	runs = mainConfig.runs

					
	
	result = ""
	
	for run in runs:
		log.logInfo("%s"%run.label)
		
		
			
		lineTemplate = r"%(title)50s & $%(EE).1f\pm%(totalsEE).1f$ &$ %(MuMu).1f\pm%(totalsMuMu).1f$ &$ %(EMu).1f\pm%(totalsEMu).1f$ &$ %(nSF).1f\pm%(statSF).1f\pm%(systSF).1f$ &$ %(nOF).1f\pm%(statOF).1f\pm%(systOF).1f$& $%(nS)3.1f\pm%(statS).1f\pm%(systS).1f$ \\"+"\n"
		
		cutString = cutStrings[region]%(run.runCut)
		print cutString
		
		firstBin = 20
		counts = {run.label:{}}
		lastBin = 10000
		nBins = 1
		denominatorHistoEE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEE.iteritems():
			denominatorHistoEE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorMuMu.iteritems():
			denominatorHistoMuMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
			print denominatorHistoMuMu.GetEntries()
		denominatorHistoEMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoEMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoMuE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuEG = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoMuEG.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())

		nominatorHistoEE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorEE.iteritems():
			nominatorHistoEE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
			print nominatorHistoEE.GetEntries()
		nominatorHistoMuMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuMu.iteritems():
			nominatorHistoMuMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuMuNoTrack = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuMuNoTrack.iteritems():
			nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuE.iteritems():
			nominatorHistoMuE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoEMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorEMu.iteritems():
			nominatorHistoEMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuEG = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuEG.iteritems():
			nominatorHistoMuEG.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())							
		
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
		lastBin = 10000
		nBins = 1
		denominatorHistoEE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEE.iteritems():
			denominatorHistoEE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorMuMu.iteritems():
			denominatorHistoMuMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
			print denominatorHistoMuMu.GetEntries()
		denominatorHistoEMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoEMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoMuE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuEG = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoMuEG.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())

		nominatorHistoEE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorEE.iteritems():
			nominatorHistoEE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
			print nominatorHistoEE.GetEntries()
		nominatorHistoMuMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuMu.iteritems():
			nominatorHistoMuMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuMuNoTrack = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuMuNoTrack.iteritems():
			nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuE.iteritems():
			nominatorHistoMuE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoEMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorEMu.iteritems():
			nominatorHistoEMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuEG = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuEG.iteritems():
			nominatorHistoMuEG.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())							
		
		counts[run.label]["default"] = {}
		counts[run.label]["default"]["EE"] = getCounts(nominatorHistoEE, denominatorHistoEE,cutString)
		counts[run.label]["default"]["MuMu"] = getCounts(nominatorHistoMuMu, denominatorHistoMuMu,cutString)
		counts[run.label]["default"]["EMu"] = getCounts(nominatorHistoMuEG, denominatorHistoMuEG,cutString)
		
		
		outFilePkl = open("shelves/triggerEffExclusive_%s_%s_%s.pkl"%(region,source,run.label),"w")
		pickle.dump(counts, outFilePkl)
		outFilePkl.close()		
		
		
		cutString = cutStringsExclusiveNoHT[region]%(run.runCut)
		print cutString
		
		firstBin = 20
		counts = {run.label:{}}
		lastBin = 10000
		nBins = 1
		denominatorHistoEE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEE.iteritems():
			denominatorHistoEE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorMuMu.iteritems():
			denominatorHistoMuMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
			print denominatorHistoMuMu.GetEntries()
		denominatorHistoEMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoEMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoMuE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		denominatorHistoMuEG = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesDenominatorEMu.iteritems():
			denominatorHistoMuEG.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())

		nominatorHistoEE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorEE.iteritems():
			nominatorHistoEE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
			print nominatorHistoEE.GetEntries()
		nominatorHistoMuMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuMu.iteritems():
			nominatorHistoMuMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuMuNoTrack = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuMuNoTrack.iteritems():
			nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuE = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuE.iteritems():
			nominatorHistoMuE.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoEMu = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorEMu.iteritems():
			nominatorHistoEMu.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())
		nominatorHistoMuEG = TH1F("","",nBins,firstBin,lastBin)
		for name, tree in treesNominatorMuEG.iteritems():
			nominatorHistoMuEG.Add(createHistoFromTree(tree,"pt1",cutString,nBins,firstBin,lastBin).Clone())							
		
		counts[run.label]["default"] = {}
		counts[run.label]["default"]["EE"] = getCounts(nominatorHistoEE, denominatorHistoEE,cutString)
		counts[run.label]["default"]["MuMu"] = getCounts(nominatorHistoMuMu, denominatorHistoMuMu,cutString)
		counts[run.label]["default"]["EMu"] = getCounts(nominatorHistoMuEG, denominatorHistoMuEG,cutString)
		
		
		outFilePkl = open("shelves/triggerEffExclusiveNoHT_%s_%s_%s.pkl"%(region,source,run.label),"w")
		pickle.dump(counts, outFilePkl)
		outFilePkl.close()		
				
				
	
		
		
