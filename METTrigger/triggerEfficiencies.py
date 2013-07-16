### Calculates efficiencies of DiLepton Triggers in HT of alphaT triggered events
from messageLogger import messageLogger as log


from defs import mainConfig
from defs import dependendies
from defs import selections
import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1
from setTdrStyle import setTDRStyle
from helpers import readTrees, createHistoFromTree

if (__name__ == "__main__"):
	
	path = mainConfig.path
	source = mainConfig.source
	log.logHighlighted("Calculating trigger efficiencies on %s triggered dataset"%source)
	log.logHighlighted("Using trees from %s "%path)
	treesDenominatorEE = readTrees(path,source,"%s"%(source,),"EE")
	treesDenominatorMuMu = readTrees(path,source,"%s"%(source,),"MuMu")
	treesDenominatorEMu = readTrees(path,source,"%s"%(source,),"EMu")
	
	
	treesNominatorEE = readTrees(path,source,"%sHLTMET"%(source,),"EE")
	treesNominatorMuMu = readTrees(path,source,"%sHLTMET"%(source,),"MuMu")
	treesNominatorEMu = readTrees(path,source,"%sHLTMET"%(source,),"EMu")
	
	cuts = mainConfig.cuts
	variables = mainConfig.variables
	runs = mainConfig.runs

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
	import numpy as np
	for run in runs:
		log.logInfo("%s"%run.label)
		for cut in cuts:
			log.logInfo("%s"%cut.label1)
			
			for variable in variables:
				log.logInfo("%s"%variable.labelX)
				cutString = cut.cut%(run.runCut,variable.additionalCuts)
				log.logInfo("Full cut string: %s"%(cutString,))
				binning = [0,20,40,60,80,100,120,140,160,180,200,240,300,400]
				nNewBins = len(binning)-1
				#~ print nNewBins
				binning_array = np.array(binning,"d")
				firstBin = 0.
				if "eta" in variable.variable:
					firstBin = -2.6
				lastBin = variable.nBins*variable.binWidths
				denominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorEE.iteritems():
					if "DoubleElectron" in name:
						denominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorMuMu.iteritems():
					if "DoubleMu" in name: 
						denominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorEMu.iteritems():
					if "MuEG" in name:
						denominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())

				nominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorEE.iteritems():
					if "DoubleElectron" in name:
						nominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuMu.iteritems():
					if "DoubleMu" in name:
						nominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorEMu.iteritems():
					if "MuEG" in name:
						nominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				
				nominatorHistoEE = nominatorHistoEE.Rebin(nNewBins,"newHistEE",binning_array)
				nominatorHistoMuMu = nominatorHistoMuMu.Rebin(nNewBins,"newHistMuMu",binning_array)
				nominatorHistoEMu = nominatorHistoEMu.Rebin(nNewBins,"newHistEMu",binning_array)
				denominatorHistoEE = denominatorHistoEE.Rebin(nNewBins,"newHistEE2",binning_array)
				denominatorHistoMuMu = denominatorHistoMuMu.Rebin(nNewBins,"newHistMuMu2",binning_array)
				denominatorHistoEMu = denominatorHistoEMu.Rebin(nNewBins,"newHistEMu2",binning_array)
				#~ effEE = TEfficiency(nominatorHistoEE,denominatorHistoEE)
				#~ effEMu = TEfficiency(nominatorHistoEMu,denominatorHistoEMu)
				#~ effMuE = TEfficiency(nominatorHistoMuE,denominatorHistoEMu)
				#~ effMuMu = TEfficiency(nominatorHistoMuMu,denominatorHistoMuMu)
				#~ effMuMuNoTrack = TEfficiency(nominatorHistoMuMuNoTrack,denominatorHistoMuMu)
				#~ 
				#~ 

				effEE = TGraphAsymmErrors(nominatorHistoEE,denominatorHistoEE,"cp")
				effEMu = TGraphAsymmErrors(nominatorHistoEMu,denominatorHistoEMu,"cp")
				effMuMu = TGraphAsymmErrors(nominatorHistoMuMu,denominatorHistoMuMu,"cp")

		
				effEE.SetMarkerColor(ROOT.kBlack)
				effMuMu.SetMarkerColor(ROOT.kRed)
				effEMu.SetMarkerColor(ROOT.kBlue)
				effEE.SetLineColor(ROOT.kBlack)
				effMuMu.SetLineColor(ROOT.kRed)
				effEMu.SetLineColor(ROOT.kBlue)
				hCanvas.DrawFrame(firstBin,0,lastBin,1.2,"; %s ; Efficiency" %(variable.labelX))
				
				#~ fitEE = TF1("fitEE","[0]",20,100)
				#~ fitMuMu = TF1("fitMuMu","[0]",20,100)
				#~ fitMuMuNoTrack = TF1("fitMuMuNoTrack","[0]",20,100)
				#~ fitEMu = TF1("fitEMu","[0]",20,100)
				#~ fitMuE = TF1("fitMuE","[0]",20,100)
				#~ fitEE.SetLineColor(ROOT.kBlack)
				#~ fitMuMu.SetLineColor(ROOT.kRed)
				#~ fitMuMuNoTrack.SetLineColor(ROOT.kRed+2)
				#~ fitEMu.SetLineColor(ROOT.kBlue+2)
				#~ fitMuE.SetLineColor(ROOT.kBlue)
				#~ effEE.Fit("fitEE","BRQE","",20,100)
				#~ effMuMu.Fit("fitMuMu","BRQE","",20,100)
				#~ effMuMuNoTrack.Fit("fitMuMuNoTrack","BRQE","",20,100)
				#~ effEMu.Fit("fitEMu","BRQE","",20,100)
				#~ effMuE.Fit("fitMuE","BRQE","",20,100)
				
				legend.Clear()
				legend.AddEntry(effEE,"MET trigger in EE events","p")
				legend.AddEntry(effMuMu,"MET trigger in MuMu events","p")
				#~ legend.AddEntry(effMuMuNoTrack,"Mu17_Mu8 %.3f #pm %.3f"%(fitMuMuNoTrack.GetParameter(0),fitMuMuNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(effMuE,"Mu17_Ele8_X %.3f #pm %.3f"%(fitMuE.GetParameter(0),fitMuE.GetParError(0)),"p")
				legend.AddEntry(effEMu,"MET trigger in EMu events","p")

				
				effEE.Draw("samep")
				effMuMu.Draw("samep")
				#~ effMuMuNoTrack.Draw("samep")
				#~ effMuE.Draw("samep")
				effEMu.Draw("samep")
		
		
				latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				legend.Draw("same")
				hCanvas.Print("Triggereff_%s_%s_%s_%s.pdf"%(source,run.plotName,variable.plotName,variable.additionalPlotName))
				#~ hCanvas.Clear()
				
	

