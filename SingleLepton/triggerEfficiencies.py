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


etaCuts = {"Inclusive":"((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) ",
			  "Barrel":"abs(eta1)<1.4  && abs(eta2) < 1.4",
			  "Endcap":"1.6<=TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) )",
			}
logEtaCuts = {"Inclusive":"|#eta|<2.4",
        		  "Barrel":"Central",
        		  "Endcap":"Forward"
        		}


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

	if len(argv) ==1:
		log.logHighlighted("No lepton eta selection specified, using inclusive!")
		region = "Inclusive"
	else:
		region = argv[1]
	
	path = mainConfig.path
	source = "Electron"
	log.logHighlighted("Calculating trigger efficiencies on %s triggered dataset"%source)
	log.logHighlighted("Using trees from %s "%path)
	treesDenominatorElectronEE = readTrees(path,source,"","EE")
	treesDenominatorElectronMuMu = readTrees(path,source,"","MuMu")
	treesDenominatorElectronEMu = readTrees(path,source,"","EMu")
	
	
	
	treesNominatorElectronEE = readTrees(path,source,"HLTDiEle","EE")
	treesNominatorElectronMuMu = readTrees(path,source,"HLTDiMu","MuMu")
	treesNominatorElectronMuMuNoTrack = readTrees(path,source,"HLTDiMuNoTrackerMuon","MuMu")
	treesNominatorElectronEMu = readTrees(path,source,"HLTEleMu","EMu")
	treesNominatorElectronMuE = readTrees(path,source,"HLTMuEle","EMu")
	treesNominatorElectronMuEG = readTrees(path,source,"HLTMuEG","EMu")
	
	source = "Muon"
	
	treesDenominatorMuonEE = readTrees(path,source,"","EE")
	treesDenominatorMuonMuMu = readTrees(path,source,"","MuMu")
	treesDenominatorMuonEMu = readTrees(path,source,"","EMu")
	
	
	treesNominatorMuonEE = readTrees(path,source,"HLTDiEle","EE")
	treesNominatorMuonMuMu = readTrees(path,source,"HLTDiMu","MuMu")
	treesNominatorMuonMuMuNoTrack = readTrees(path,source,"HLTDiMuNoTrackerMuon","MuMu")
	treesNominatorMuonEMu = readTrees(path,source,"HLTEleMu","EMu")
	treesNominatorMuonMuE = readTrees(path,source,"HLTMuEle","EMu")
	treesNominatorMuonMuEG = readTrees(path,source,"HLTMuEG","EMu")	


	etaCut = etaCuts[argv[1]]
	logEtaCut = logEtaCuts[argv[1]]
	
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
	
	for run in runs:
		log.logInfo("%s"%run.label)
		for cut in cuts:
			log.logInfo("%s"%cut.label1)
			
			for variable in variables:
				log.logInfo("%s"%variable.labelX)
				cutString = cut.cut%(run.runCut,variable.additionalCuts,"&& %s"%(etaCut) )				
				cutStringEE = cut.cut%(run.runCut,variable.additionalCuts,"&& matchesSingleElectron2 == 1 && %s"%(etaCut) )				
				cutStringMuMu = cut.cut%(run.runCut,variable.additionalCuts,"&& matchesSingleMuon2 == 1 && %s"%(etaCut) )				
				cutStringEMu = cut.cut%(run.runCut,variable.additionalCuts," && pt1 > 20 && matchesSingleElectron1 == 1 && %s"%(etaCut) )
				cutStringMuE = cut.cut%(run.runCut,variable.additionalCuts," && pt2 > 20 && matchesSingleMuon2 == 1 && %s"%(etaCut) )
				cutStringMuE2 = cut.cut%(run.runCut,variable.additionalCuts," && pt2 > 20 && matchesSingleMuon2 == 1 && matchesMuETrailing1==1 && %s"%(etaCut) )
				#~ cutString = ""				
				#~ cutStringEMu = ""
				#~ cutStringMuE = ""
				#~ cutStringMuE2 = ""
				#~ cutStringEMu = cut.cut%(run.runCut,variable.additionalCuts," && pt1 > 20")
				#~ cutStringMuE = cut.cut%(run.runCut,variable.additionalCuts," && pt2 > 20")
				log.logInfo("Full cut string: %s"%(cutString,))
				
				firstBin = variable.firstBin
				
				#~ if "eta" in variable.variable:
					#~ firstBin = -2.4
				lastBin = variable.nBins*variable.binWidths
				denominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorElectronEE.iteritems():
					#~ print name
					denominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutStringEE,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorMuonMuMu.iteritems():
					#~ print name
					denominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutStringMuMu,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorElectronEMu.iteritems():
					#~ print name
					denominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutStringEMu,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoMuE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorMuonEMu.iteritems():
					#~ print name
					denominatorHistoMuE.Add(createHistoFromTree(tree,variable.variable,cutStringMuE,variable.nBins,firstBin,lastBin).Clone())
				#~ denominatorHistoMuEG = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesDenominatorEMu.iteritems():
					#~ print name
					#~ denominatorHistoMuEG.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())

				nominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorElectronEE.iteritems():
					#~ print name
					nominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutStringEE,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuonMuMu.iteritems():
					#~ print name
					nominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutStringMuMu,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuMuNoTrack = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuonMuMuNoTrack.iteritems():
					#~ print name
					nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,variable.variable,cutStringMuMu,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuE = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorMuonMuE.iteritems():
				for name, tree in treesNominatorMuonMuE.iteritems():
					print name
					nominatorHistoMuE.Add(createHistoFromTree(tree,variable.variable,cutStringMuE,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorElectronEMu.iteritems():
					#~ print name
					nominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutStringEMu,variable.nBins,firstBin,lastBin).Clone())
				#~ nominatorHistoMuEG = TH1F("","",variable.nBins,firstBin,lastBin)
				#~ for name, tree in treesNominatorMuEG.iteritems():
					#~ print name
					#~ nominatorHistoMuEG.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
#~ 
		#~ 
				#~ effEE = TEfficiency(nominatorHistoEE,denominatorHistoEE)
				#~ effEMu = TEfficiency(nominatorHistoEMu,denominatorHistoEMu)
				#~ effMuE = TEfficiency(nominatorHistoMuE,denominatorHistoEMu)
				#~ effMuMu = TEfficiency(nominatorHistoMuMu,denominatorHistoMuMu)
				#~ effMuMuNoTrack = TEfficiency(nominatorHistoMuMuNoTrack,denominatorHistoMuMu)
				#~ 
				#~ 
				print nominatorHistoMuE.Integral()
				print denominatorHistoMuE.Integral()
				effEE = TGraphAsymmErrors(nominatorHistoEE,denominatorHistoEE,"cp")
				effEMu = TGraphAsymmErrors(nominatorHistoEMu,denominatorHistoEMu,"cp")
				effMuE = TGraphAsymmErrors(nominatorHistoMuE,denominatorHistoMuE,"cp")
				effMuMu = TGraphAsymmErrors(nominatorHistoMuMu,denominatorHistoMuMu,"cp")
				effMuMuNoTrack = TGraphAsymmErrors(nominatorHistoMuMuNoTrack,denominatorHistoMuMu,"cp")
		
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
				effEE.Fit("fitEE","BRQE","",40,fitEnd)
				effMuMu.Fit("fitMuMu","BRQE","",40,fitEnd)
				effMuMuNoTrack.Fit("fitMuMuNoTrack","BRQE","",40,fitEnd)
				effEMu.Fit("fitEMu","BRQE","",40,fitEnd)
				effMuE.Fit("fitMuE","BRQE","",40,fitEnd)
				
				legend.Clear()
				#~ legend.AddEntry(effEE,"Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitEE.GetParameter(0),fitEE.GetParError(0)),"p")
				#~ legend.AddEntry(effMuMu,"Mu17_Mu8 || Mu17_TkMu8 %.3f #pm %.3f"%(fitMuMu.GetParameter(0),fitMuMu.GetParError(0)),"p")
				#~ legend.AddEntry(effMuMuNoTrack,"Mu17_Mu8 %.3f #pm %.3f"%(fitMuMuNoTrack.GetParameter(0),fitMuMuNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(effMuE,"Mu17_Ele8_X %.3f #pm %.3f"%(fitMuE.GetParameter(0),fitMuE.GetParError(0)),"p")
				#~ legend.AddEntry(effEMu,"Ele17_X_Mu8 %.3f #pm %.3f"%(fitEMu.GetParameter(0),fitEMu.GetParError(0)),"p")
				legend.AddEntry(effEE,"Dielectron_X %.3f #pm %.3f"%(fitEE.GetParameter(0),fitEE.GetParError(0)),"p")
				legend.AddEntry(effMuMu,"Dimuon incl. tracker muon %.3f #pm %.3f"%(fitMuMu.GetParameter(0),fitMuMu.GetParError(0)),"p")
				legend.AddEntry(effMuMuNoTrack,"Dimuon %.3f #pm %.3f"%(fitMuMuNoTrack.GetParameter(0),fitMuMuNoTrack.GetParError(0)),"p")
				legend.AddEntry(effMuE,"OF muon leading %.3f #pm %.3f"%(fitMuE.GetParameter(0),fitMuE.GetParError(0)),"p")
				legend.AddEntry(effEMu,"OF ele leading %.3f #pm %.3f"%(fitEMu.GetParameter(0),fitEMu.GetParError(0)),"p")

				
				effEE.Draw("samep")
				effMuMu.Draw("samep")
				effMuMuNoTrack.Draw("samep")
				effMuE.Draw("samep")
				effEMu.Draw("samep")
		
		
				latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%run.lumi)
				cmsExtra = "Private Work"

				latexCMS.DrawLatex(0.15,0.955,"CMS")
				latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))			
				#~ latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.2,0.9,"#splitline{"+logEtaCut+", "+cut.label1+"}{"+variable.additionalCutsLabel+"}")	
				legend.Draw("same")
				
				
				line1 = ROOT.TLine(20,0,20,1.05)
				line1.SetLineColor(ROOT.kBlue+3)

				line1.SetLineWidth(2)
				line1.SetLineStyle(2)

				line1.Draw("same")				
							
				hCanvas.Print("Triggereff_%s_%s_%s_%s_%s_%s.pdf"%(source,region,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
				#~ hCanvas.Clear()
				
				#~ denominatorHistoSF = denominatorHistoEE.Clone()
				#~ denominatorHistoOF = denominatorHistoMuEG.Clone()
				#~ denominatorHistoSF.Add(denominatorHistoMuMu.Clone())
				#~ 
				#~ nominatorHistoSF = nominatorHistoEE.Clone()
				#~ nominatorHistoSFNoTrack = nominatorHistoEE.Clone()
				#~ 
				#~ nominatorHistoSF.Add(nominatorHistoMuMu.Clone())
				#~ nominatorHistoSFNoTrack.Add(nominatorHistoMuMuNoTrack.Clone())
				#~ 
				#~ nominatorHistoOF = nominatorHistoMuEG.Clone()
				#~ 
				#~ effSF = TGraphAsymmErrors(nominatorHistoSF,denominatorHistoSF,"cp")
				#~ effSFNoTrack = TGraphAsymmErrors(nominatorHistoSFNoTrack,denominatorHistoSF,"cp")
				#~ effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cp")
#~ 
#~ 
#~ 
				#~ effSF.SetMarkerColor(ROOT.kBlack)
				#~ effSFNoTrack.SetMarkerColor(ROOT.kRed)
				#~ effOF.SetMarkerColor(ROOT.kBlue)
				#~ effSF.SetLineColor(ROOT.kBlack)
				#~ effSFNoTrack.SetLineColor(ROOT.kRed)
				#~ effOF.SetLineColor(ROOT.kBlue)
				#~ effSF.SetMarkerStyle(20)
				#~ effSFNoTrack.SetMarkerStyle(21)
				#~ effOF.SetMarkerStyle(22)
				#~ 
				#~ effSFNoFit = effSF.Clone()
				#~ effSFNoTrackNoFit = effSF.Clone()
				#~ effOFNoFit = effSF.Clone()
				#~ 
			#~ 
				#~ hCanvas.DrawFrame(firstBin,0,lastBin,1.2,"; %s ; Efficiency" %(variable.labelX))
				#~ 
				#~ fitSF = TF1("fitSF","[0]",fitStart,fitEnd)
				#~ fitSFNoTrack = TF1("fitSFNoTrack","[0]",fitStart,fitEnd)
				#~ fitOF = TF1("fitOF","[0]",fitStart,fitEnd)
				#~ fitSF.SetLineColor(ROOT.kBlack)
				#~ fitSFNoTrack.SetLineColor(ROOT.kRed)
				#~ fitOF.SetLineColor(ROOT.kBlue)
				#~ effSF.Fit("fitSF","BRQE","",fitStart,fitEnd)
				#~ effSFNoTrack.Fit("fitSFNoTrack","BRQE","",fitStart,fitEnd)
				#~ effOF.Fit("fitOF","BRQE","",fitStart,fitEnd)
#~ 
#~ 
#~ 
#~ 
				#~ legend.Clear()
				#~ legend.AddEntry(effSF,"Ele_17_X_Ele8_X || Mu17_Mu8 || Mu17_TkMu8  %.3f #pm %.3f"%(fitSF.GetParameter(0),fitSF.GetParError(0)),"p")
				#~ legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(effOF,"Mu17_Ele8_X || Ele17_X_Mu8 %.3f #pm %.3f"%(fitOF.GetParameter(0),fitOF.GetParError(0)),"p")
				#~ legend.AddEntry(effSF,"Same Flavour  %.3f #pm %.3f"%(fitSF.GetParameter(0),fitSF.GetParError(0)),"p")
				#~ legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(effOF,"Opposite Flavour %.3f #pm %.3f"%(fitOF.GetParameter(0),fitOF.GetParError(0)),"p")


				#~ effSFNoTrack.Draw("samep")
				#~ effSF.Draw("samep")
				#~ effOF.Draw("samep")
#~ 
		#~ 
		#~ 
				#~ latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				#~ intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				#~ legend.Draw("same")
	#~ 
				#~ hCanvas.Print("Triggereff_SFvsOF_%s_%s_%s_%s_%s.pdf"%(source,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
#~ 
				#~ hCanvas.DrawFrame(firstBin,.4,lastBin,1.6,"; %s ; Efficiency SF / Efficiency OF" %(variable.labelX))

				#~ effSFNoFit = effSF.Clone()
				#~ effSFNoTrackNoFit = effSFNoTrack.Clone()
				#~ effOFNoFit = effOF.Clone()
				#~ 
				#~ effSFNoFit.Draw("samep")
				#~ effOFNoFit.Draw("samep")
				#~ 
				#~ sfLine= ROOT.TF1("sfLine","0.966",firstBin, lastBin)
				#~ sfLine.SetLineColor(ROOT.kBlack)
				#~ sfLine.SetLineWidth(3)
				#~ sfLine.SetLineStyle(2)
				#~ sfLine.Draw("SAME")
				#~ 
				#~ ofLine= ROOT.TF1("sfLine","0.921",firstBin, lastBin)
				#~ ofLine.SetLineColor(ROOT.kBlue)
				#~ ofLine.SetLineWidth(3)
				#~ ofLine.SetLineStyle(2)
				#~ ofLine.Draw("SAME")
				#~ legend.Clear()
				#~ legend.AddEntry(effSFNoFit,"Same Flavour","p")
				#~ legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(sfLine,"SF Efficiency: 0.966","p")				
				#~ legend.AddEntry(effOFNoFit,"Opposite Flavour","p")				
				#~ legend.AddEntry(ofLine,"OF Efficiency: 0.921","p")	
				
				#~ effSFvsOF = efficiencyRatio(effSF,effOF)
#~ 
				#~ x= array("f",[firstBin, lastBin]) 
				#~ y= array("f", [1.175, 1.175]) # 1.237
				#~ y= array("f", [1.032, 1.032]) # 1.237
				#~ ex= array("f", [0.,0.])
				#~ ey= array("f", [0.03, 0.03])
				#~ ge= ROOT.TGraphErrors(2, x, y, ex, ey)
				#~ ge.SetFillColor(ROOT.kOrange-9)
				#~ ge.SetFillStyle(1001)
				#~ ge.SetLineColor(ROOT.kWhite)
				#~ ge.Draw("SAME 3")
				#~ 
				#~ effSFvsOF.Draw("samep")
				#~ 
				#~ sfLine= ROOT.TF1("sfLine","1.032",firstBin, lastBin)
				#~ sfLine.SetLineColor(ROOT.kBlack)
				#~ sfLine.SetLineWidth(3)
				#~ sfLine.SetLineStyle(2)
				#~ sfLine.Draw("SAME")				
				#~ 
#~ 
				#~ latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				#~ intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")
#~ 
				#~ 
				#~ legend.Clear()
				#~ legend.AddEntry(effSFvsOF,"Triggerefficiency SF/OF","p") 
				#~ legend.AddEntry(sfLine,"Mean SF vs OF: 1.032","l") 
				#~ legend.AddEntry(ge,"Mean SF vs OF #pm 3%","f") 
				#~ legend.Draw("same")
				#~ ROOT.gPad.RedrawAxis()
				#~ hCanvas.Print("Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s.pdf"%(source,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
							
