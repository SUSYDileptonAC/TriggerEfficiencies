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
config.read("/.automount/home/home__home4/institut_1b/jschulte/Doktorarbeit/Dilepton/SubmitScripts/Input/Master53X.ini")


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
	import pickle
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
	TT_Dileptonic = Process(Backgrounds.TT_Dileptonic.subprocesses,eventCounts,Backgrounds.TT_Dileptonic.label,Backgrounds.TT_Dileptonic.fillcolor,Backgrounds.TT_Dileptonic.linecolor,Backgrounds.TT_Dileptonic.uncertainty,1)	
	#~ TT_MCatNLO = Process(Backgrounds.TT_MCatNLO.subprocesses,eventCounts,Backgrounds.TT_MCatNLO.label,Backgrounds.TT_MCatNLO.fillcolor,Backgrounds.TT_MCatNLO.linecolor,Backgrounds.TT_MCatNLO.uncertainty,1)	
	Diboson = Process(Backgrounds.Diboson.subprocesses,eventCounts,Backgrounds.Diboson.label,Backgrounds.Diboson.fillcolor,Backgrounds.Diboson.linecolor,Backgrounds.Diboson.uncertainty,1)	
	Rare = Process(Backgrounds.Rare.subprocesses,eventCounts,Backgrounds.Rare.label,Backgrounds.Rare.fillcolor,Backgrounds.Rare.linecolor,Backgrounds.Rare.uncertainty,1)	
	DY = Process(Backgrounds.DrellYan.subprocesses,eventCounts,Backgrounds.DrellYan.label,Backgrounds.DrellYan.fillcolor,Backgrounds.DrellYan.linecolor,Backgrounds.DrellYan.uncertainty,1)	
	SingleTop = Process(Backgrounds.SingleTop.subprocesses,eventCounts,Backgrounds.SingleTop.label,Backgrounds.SingleTop.fillcolor,Backgrounds.SingleTop.linecolor,Backgrounds.SingleTop.uncertainty,1)	

	#~ processes = [TT,Diboson,Rare,DY,SingleTop]
	processes = [TT_Dileptonic]
	#~ processes = [Rare]

	lumi = 9200
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	
	legend = TLegend(0.3, 0.13, 0.95, 0.5)
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
	latex.SetTextSize(0.035)
	latex.SetNDC(True)

	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)					
	
	for run in runs:
		log.logInfo("%s"%run.label)
		
		

		lineTemplate = r"%(title)50s & $%(EE).1f\pm%(totalsEE).1f$ &$ %(MuMu).1f\pm%(totalsMuMu).1f$ &$ %(EMu).1f\pm%(totalsEMu).1f$ &$ %(nSF).1f\pm%(statSF).1f\pm%(systSF).1f$ &$ %(nOF).1f\pm%(statOF).1f\pm%(systOF).1f$& $%(nS)3.1f\pm%(statS).1f\pm%(systS).1f$ \\"+"\n"
		
		cutString = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20  && ht > 200  && %s)"%(run.runCut)
		#~ cutString = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20  && ht > 150 && met > 50  && %s)"%(run.runCut)
		
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
		
		
		outFilePkl = open("shelves/triggerEff_%s_%s.pkl"%(source,run.label),"w")
		pickle.dump(counts, outFilePkl)
		outFilePkl.close()				
		#~ outFile = open("triggerEfficiencies_%s.tex"%run.label,"w")
		#~ outFile.write(triggerTable)
		#~ outFile.close()		
		
		cutString = "weight*(chargeProduct < 0  && abs(eta1)<1.4  && abs(eta2) < 1.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20  && ht > 200  && %s)"%(run.runCut)
		#~ cutString = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && pt1 > 20 && pt2 > 20  && ht > 150 && met > 50  && %s)"%(run.runCut)
		
		firstBin = 20
		counts = {run.label:{}}
		#~ if "eta" in variable.variable:
			#~ firstBin = -2.4
		lastBin = 1000
		nBins = 1
		plot = Plot("pt1",cutString,"bla","Efficiency",nBins,firstBin,lastBin)

		denominatorStackEE2 = TheStack(processes,lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
		denominatorStackMuMu2 = TheStack(processes,lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
		#~ denominatorStackEMu = TheStack(processes,lumi,plotEMu,treesDenominatorEMu,"None",1.0,1.0,1.0)	
		#~ denominatorStackMuE = TheStack(processes,lumi,plotMuE,treesDenominatorEMu,"None",1.0,1.0,1.0)	
		denominatorStackMuEG2 = TheStack(processes,lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
			
		nominatorStackEE2 = TheStack(processes,lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
		nominatorStackMuMu2 = TheStack(processes,lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)		
		#~ nominatorStackMuMuNoTrack = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
		#~ nominatorStackEMu = TheStack(processes,lumi,plotEMu,treesNominatorEMu,"None",1.0,1.0,1.0)		
		#~ nominatorStackMuE = TheStack(processes,lumi,plotMuE,treesNominatorMuE,"None",1.0,1.0,1.0)		
		nominatorStackMuEG2 = TheStack(processes,lumi,plot,treesNominatorMuEG,"None",1.0,1.0,1.0)		

		denominatorHistoEE = denominatorStackEE2.theHistogram
		print denominatorHistoEE.GetEntries()
		denominatorHistoMuMu = denominatorStackMuMu2.theHistogram
		#~ denominatorHistoEMu = denominatorStackEMu.theHistogram
		#~ denominatorHistoMuE = denominatorStackMuE.theHistogram
		denominatorHistoMuEG = denominatorStackMuEG2.theHistogram
		
		nominatorHistoEE = nominatorStackEE2.theHistogram
		nominatorHistoMuMu = nominatorStackMuMu2.theHistogram
		#~ nominatorHistoMuMuNoTrack = nominatorStackMuMuNoTrack.theHistogram
		#~ nominatorHistoEMu = nominatorStackEMu.theHistogram
		#~ nominatorHistoMuE = nominatorStackMuE.theHistogram
		nominatorHistoMuEG = nominatorStackMuEG2.theHistogram						
		
		counts[run.label]["default"] = {}
		
		counts[run.label]["default"]["EE"] = getCounts(nominatorHistoEE, denominatorHistoEE,cutString)
		counts[run.label]["default"]["MuMu"] = getCounts(nominatorHistoMuMu, denominatorHistoMuMu,cutString)
		counts[run.label]["default"]["EMu"] = getCounts(nominatorHistoMuEG, denominatorHistoMuEG,cutString)
		
		print "working"
		outFilePkl = open("shelves/triggerEff_Barrel_%s_%s.pkl"%(source,run.label),"w")
		pickle.dump(counts, outFilePkl)
		outFilePkl.close()				
		#~ outFile = open("triggerEfficiencies_%s.tex"%run.label,"w")
		#~ outFile.write(triggerTable)
		#~ outFile.close()		
		
		
		
		
		
		
		
		
		for cut in cuts:
			log.logInfo("%s"%cut.label1)

			
			for variable in variables:
				log.logInfo("%s"%variable.labelX)
				cutString = cut.cut%(run.runCut,variable.additionalCuts,"")
				cutStringEMu = cut.cut%(run.runCut,variable.additionalCuts," && pt1 > 20")
				cutStringMuE = cut.cut%(run.runCut,variable.additionalCuts," && pt2 > 20")
				log.logInfo("Full cut string: %s"%(cutString,))
				
				firstBin = variable.firstBin
				#~ if "eta" in variable.variable:
					#~ firstBin = -2.4
				lastBin = variable.nBins*variable.binWidths
				
				
				plot = Plot(variable.variable,cutString,variable.labelX,"Efficiency",variable.nBins,firstBin,lastBin)
				plotEMu = Plot(variable.variable,cutStringEMu,variable.labelX,"Efficiency",variable.nBins,firstBin,lastBin)
				plotMuE = Plot(variable.variable,cutStringMuE,variable.labelX,"Efficiency",variable.nBins,firstBin,lastBin)
				
				#~ denominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesDenominatorEE.iteritems():

					#~ denominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				#~ denominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesDenominatorMuMu.iteritems():

					#~ denominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				#~ denominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesDenominatorEMu.iteritems():

					#~ denominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
#~ 
				#~ nominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorEE.iteritems():

					#~ nominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				#~ nominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorMuMu.iteritems():

					#~ nominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				#~ nominatorHistoMuMuNoTrack = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorMuMuNoTrack.iteritems():

					#~ nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				#~ nominatorHistoMuE = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorMuE.iteritems():

					#~ nominatorHistoMuE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				#~ nominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorEMu.iteritems():

					#~ nominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
#~ 
		#~ 
				denominatorStackEE = TheStack(processes,lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
				denominatorStackMuMu = TheStack(processes,lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
				denominatorStackEMu = TheStack(processes,lumi,plotEMu,treesDenominatorEMu,"None",1.0,1.0,1.0)	
				denominatorStackMuE = TheStack(processes,lumi,plotMuE,treesDenominatorEMu,"None",1.0,1.0,1.0)	
				denominatorStackMuEG = TheStack(processes,lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
					
				nominatorStackEE = TheStack(processes,lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
				nominatorStackMuMu = TheStack(processes,lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)		
				nominatorStackMuMuNoTrack = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
				nominatorStackEMu = TheStack(processes,lumi,plotEMu,treesNominatorEMu,"None",1.0,1.0,1.0)		
				nominatorStackMuE = TheStack(processes,lumi,plotMuE,treesNominatorMuE,"None",1.0,1.0,1.0)		
				nominatorStackMuEG = TheStack(processes,lumi,plot,treesNominatorMuEG,"None",1.0,1.0,1.0)		
		
				denominatorHistoEE = denominatorStackEE.theHistogram
				denominatorHistoMuMu = denominatorStackMuMu.theHistogram
				denominatorHistoEMu = denominatorStackEMu.theHistogram
				denominatorHistoMuE = denominatorStackMuE.theHistogram
				denominatorHistoMuEG = denominatorStackMuEG.theHistogram
				
				nominatorHistoEE = nominatorStackEE.theHistogram
				nominatorHistoMuMu = nominatorStackMuMu.theHistogram
				nominatorHistoMuMuNoTrack = nominatorStackMuMuNoTrack.theHistogram
				nominatorHistoEMu = nominatorStackEMu.theHistogram
				nominatorHistoMuE = nominatorStackMuE.theHistogram
				nominatorHistoMuEG = nominatorStackMuEG.theHistogram
		
		
				#~ effEE = TEfficiency(nominatorHistoEE,denominatorHistoEE)
				#~ effEMu = TEfficiency(nominatorHistoEMu,denominatorHistoEMu)
				#~ effMuE = TEfficiency(nominatorHistoMuE,denominatorHistoEMu)
				#~ effMuMu = TEfficiency(nominatorHistoMuMu,denominatorHistoMuMu)
				#~ effMuMuNoTrack = TEfficiency(nominatorHistoMuMuNoTrack,denominatorHistoMuMu)
				#~ 
				#~ 

				effEE = TGraphAsymmErrors(nominatorHistoEE,denominatorHistoEE,"n")
				effEMu = TGraphAsymmErrors(nominatorHistoEMu,denominatorHistoEMu,"n")
				effMuE = TGraphAsymmErrors(nominatorHistoMuE,denominatorHistoMuE,"n")
				effMuMu = TGraphAsymmErrors(nominatorHistoMuMu,denominatorHistoMuMu,"n")
				effMuMuNoTrack = TGraphAsymmErrors(nominatorHistoMuMuNoTrack,denominatorHistoMuMu,"n")
		
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
				
				hCanvas.DrawFrame(firstBin,0,lastBin,1.2,"; %s ; Efficiency" %(variable.labelX))
				
				fitStart = variable.fitStart
				fitEnd = variable.fitEnd
				print fitStart, fitEnd
				
				fitEE = TF1("fitEE","[0]",fitStart,fitEnd)
				fitMuMu = TF1("fitMuMu","[0]",fitStart,fitEnd)
				fitMuMuNoTrack = TF1("fitMuMuNoTrack","[0]",fitStart,fitEnd)
				fitEMu = TF1("fitEMu","[0]",fitStart,fitEnd)
				fitMuE = TF1("fitMuE","[0]",fitStart,fitEnd)
				fitEE.SetLineColor(ROOT.kBlack)
				fitMuMu.SetLineColor(ROOT.kRed)
				fitMuMuNoTrack.SetLineColor(ROOT.kRed+2)
				fitEMu.SetLineColor(ROOT.kBlue+2)
				fitMuE.SetLineColor(ROOT.kBlue)
				effEE.Fit("fitEE","BRQE","",fitStart,fitEnd)
				effMuMu.Fit("fitMuMu","BRQE","",fitStart,fitEnd)
				effMuMuNoTrack.Fit("fitMuMuNoTrack","BRQE","",fitStart,fitEnd)
				effEMu.Fit("fitEMu","BRQE","",fitStart,fitEnd)
				effMuE.Fit("fitMuE","BRQE","",fitStart,fitEnd)
				
				
				legend.Clear()
				legend.AddEntry(effEE,"Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitEE.GetParameter(0),fitEE.GetParError(0)),"p")
				legend.AddEntry(effMuMu,"Mu17_Mu8 || Mu17_TkMu8 %.3f #pm %.3f"%(fitMuMu.GetParameter(0),fitMuMu.GetParError(0)),"p")
				legend.AddEntry(effMuMuNoTrack,"Mu17_Mu8 %.3f #pm %.3f"%(fitMuMuNoTrack.GetParameter(0),fitMuMuNoTrack.GetParError(0)),"p")
				legend.AddEntry(effMuE,"Mu17_Ele8_X %.3f #pm %.3f"%(fitMuE.GetParameter(0),fitMuE.GetParError(0)),"p")
				legend.AddEntry(effEMu,"Ele17_X_Mu8 %.3f #pm %.3f"%(fitEMu.GetParameter(0),fitEMu.GetParError(0)),"p")

				
				effEE.Draw("samep")
				effMuMu.Draw("samep")
				effMuMuNoTrack.Draw("samep")
				effMuE.Draw("samep")
				effEMu.Draw("samep")
		
		
				#~ latex.DrawLatex(0.15, 0.96, "CMS Simulation  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				latex.DrawLatex(0.15, 0.96, "CMS Private Work  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				legend.Draw("same")
				if source == "HT" or source == "AlphaT":
					hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s.pdf"%(source,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
				else:
					hCanvas.Print("fig/Triggereff_%s_%s_%s_%s.pdf"%(cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
				#~ hCanvas.Clear()
				
				denominatorHistoSF = denominatorHistoEE.Clone()
				denominatorHistoOF = denominatorHistoMuEG.Clone()
				denominatorHistoSF.Add(denominatorHistoMuMu.Clone())
				
				nominatorHistoSF = nominatorHistoEE.Clone()
				nominatorHistoSFNoTrack = nominatorHistoEE.Clone()
				
				nominatorHistoSF.Add(nominatorHistoMuMu.Clone())
				nominatorHistoSFNoTrack.Add(nominatorHistoMuMuNoTrack.Clone())
				
				nominatorHistoOF = nominatorHistoMuEG.Clone()
				
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
				hCanvas.DrawFrame(firstBin,0,lastBin,1.2,"; %s ; Efficiency" %(variable.labelX))
				
				fitSF = TF1("fitSF","[0]",fitStart,fitEnd)
				fitSFNoTrack = TF1("fitSFNoTrack","[0]",fitStart,fitEnd)
				fitOF = TF1("fitOF","[0]",fitStart,fitEnd)
				fitSF.SetLineColor(ROOT.kBlack)
				fitSFNoTrack.SetLineColor(ROOT.kRed)
				fitOF.SetLineColor(ROOT.kBlue)
				effSF.Fit("fitSF","BRQE","",fitStart,fitEnd)
				effSFNoTrack.Fit("fitSFNoTrack","BRQE","",fitStart,fitEnd)
				effOF.Fit("fitOF","BRQE","",fitStart,fitEnd)




				legend.Clear()
				legend.AddEntry(effSF,"Ele_17_X_Ele8_X || Mu17_Mu8 || Mu17_TkMu8  %.3f #pm %.3f"%(fitSF.GetParameter(0),fitSF.GetParError(0)),"p")
				legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				legend.AddEntry(effOF,"Mu17_Ele8_X || Ele17_X_Mu8 %.3f #pm %.3f"%(fitOF.GetParameter(0),fitOF.GetParError(0)),"p")

#~ 
				#~ legend.AddEntry(effSF,"Same Flavour  %.3f #pm %.3f"%(fitSF.GetParameter(0),fitSF.GetParError(0)),"p")
				#~ legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(effOF,"Opposite Flavour %.3f #pm %.3f"%(fitOF.GetParameter(0),fitOF.GetParError(0)),"p")


				effSFNoTrack.Draw("samep")
				effSF.Draw("samep")
				effOF.Draw("samep")

		
		
				latex.DrawLatex(0.15, 0.96, "CMS Private Work  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				legend.Draw("same")

				if source == "HT" or source == "AlphaT":
					hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s.pdf"%(source,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
				else:
					hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s.pdf"%(cut.name,run.plotName,variable.plotName,variable.additionalPlotName))	
				
				
				hCanvas.DrawFrame(firstBin,.4,lastBin,1.6,"; %s ; Efficiency SF / Efficiency OF" %(variable.labelX))
				
	
				effSFvsOF = efficiencyRatio(effSF,effOF)

				x= array("f",[firstBin, lastBin]) 
				#~ y= array("f", [1.175, 1.175]) # 1.237
				y= array("f", [1.015, 1.015]) # 1.237
				ex= array("f", [0.,0.])
				ey= array("f", [0.064, 0.064])
				ge= ROOT.TGraphErrors(2, x, y, ex, ey)
				ge.SetFillColor(ROOT.kOrange-9)
				ge.SetFillStyle(1001)
				ge.SetLineColor(ROOT.kWhite)
				ge.Draw("SAME 3")
				
				effSFvsOF.Draw("samep")
				
				sfLine= ROOT.TF1("sfLine","1.015",firstBin, lastBin)
				sfLine.SetLineColor(ROOT.kBlack)
				sfLine.SetLineWidth(3)
				sfLine.SetLineStyle(2)
				sfLine.Draw("SAME")				
				

				latex.DrawLatex(0.15, 0.96, "CMS Private Work  #sqrt{s} = 8 TeV, %s"%(run.label))
				intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")

				
				legend.Clear()
				legend.AddEntry(effSFvsOF,"Triggerefficiency SF/OF","p") 
				legend.AddEntry(sfLine,"Mean SF vs OF: 1.015","l") 
				legend.AddEntry(ge,"Mean SF vs OF #pm 6.4%","f") 
				legend.Draw("same")
				ROOT.gPad.RedrawAxis()
				if source == "HT" or source == "AlphaT":
					hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s.pdf"%(source,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
				else:
					hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s.pdf"%(cut.name,run.plotName,variable.plotName,variable.additionalPlotName))	

