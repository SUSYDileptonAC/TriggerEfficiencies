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
logEtaCuts = {"Inclusive":"|eta|<2.4",
        		  "Barrel":"|eta|<1.4",
        		  "Endcap":"min one 1.6<|eta|<2.4"
        		}
means = {"Inclusive":"1.014",
        		  "Barrel":"1.01",
        		  "Endcap":"1.10"
        		}
meansExclusive = {"Inclusive":"1.014",
        		  "Barrel":"1.01",
        		  "Endcap":"1.10"
        		}
 
errs = {"Inclusive":"1.014",
        		  "Barrel":"0.06",
        		  "Endcap":"0.07"
        		}
errsExclusive = {"Inclusive":"1.014",
        		  "Barrel":"0.06",
        		  "Endcap":"0.07"
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
	treesDenominatorEE = readTrees(path,source,"%s"%(source,),"EE")
	treesDenominatorMuMu = readTrees(path,source,"%s"%(source,),"MuMu")
	treesDenominatorEMu = readTrees(path,source,"%s"%(source,),"EMu")
	
	
	treesNominatorEE = readTrees(path,source,"%sHLTDiEle"%(source,),"EE")
	treesNominatorMuMu = readTrees(path,source,"%sHLTDiMu"%(source,),"MuMu")
	treesNominatorMuMuNoTrack = readTrees(path,source,"%sHLTDiMuNoTrackerMuon"%(source,),"MuMu")
	treesNominatorEMu = readTrees(path,source,"%sHLTEleMu"%(source,),"EMu")
	treesNominatorMuE = readTrees(path,source,"%sHLTMuEle"%(source,),"EMu")
	treesNominatorMuEG = readTrees(path,source,"%sHLTMuEG"%(source,),"EMu")
	
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
	
	result = ""
	
	for run in runs:
		log.logInfo("%s"%run.label)
		
		
		for cut in cuts:
			log.logInfo("%s" %cut.label1)
			
		
			
			
			for variable in variables:
				if region == "Endcap":
					variable.nBins = int(variable.nBins/2)
					variable.binWidths = variable.binWidths*2
				log.logInfo("%s"%variable.labelX)
				cutString = cut.cut%(run.runCut,variable.additionalCuts,"&& %s") %(etaCut)       			
				cutStringEMu = cut.cut%(run.runCut,variable.additionalCuts," && pt1 > 20 && %s") %(etaCut)
				cutStringMuE = cut.cut%(run.runCut,variable.additionalCuts," && pt2 > 20 && %s") %(etaCut)
				log.logInfo("Full cut string: %s"%(cutString,))
				
				firstBin = variable.firstBin
				
				#~ if "eta" in variable.variable:
					#~ firstBin = -2.4
				lastBin = variable.nBins*variable.binWidths
				denominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorEE.iteritems():
					#~ print name
					denominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorMuMu.iteritems():
					#~ print name
					denominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorEMu.iteritems():
					#~ print name
					denominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutStringEMu,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoMuE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorEMu.iteritems():
					#~ print name
					denominatorHistoMuE.Add(createHistoFromTree(tree,variable.variable,cutStringMuE,variable.nBins,firstBin,lastBin).Clone())
				denominatorHistoMuEG = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesDenominatorEMu.iteritems():
					#~ print name
					denominatorHistoMuEG.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())

				nominatorHistoEE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorEE.iteritems():
					#~ print name
					nominatorHistoEE.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuMu.iteritems():
					#~ print name
					nominatorHistoMuMu.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuMuNoTrack = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuMuNoTrack.iteritems():
					#~ print name
					nominatorHistoMuMuNoTrack.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuE = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuE.iteritems():
					#~ print name
					nominatorHistoMuE.Add(createHistoFromTree(tree,variable.variable,cutStringMuE,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoEMu = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorEMu.iteritems():
					#~ print name
					nominatorHistoEMu.Add(createHistoFromTree(tree,variable.variable,cutStringEMu,variable.nBins,firstBin,lastBin).Clone())
				nominatorHistoMuEG = TH1F("","",variable.nBins,firstBin,lastBin)
				for name, tree in treesNominatorMuEG.iteritems():
					#~ print name
					nominatorHistoMuEG.Add(createHistoFromTree(tree,variable.variable,cutString,variable.nBins,firstBin,lastBin).Clone())
#~ 
		#~ 
				#~ effEE = TEfficiency(nominatorHistoEE,denominatorHistoEE)
				#~ effEMu = TEfficiency(nominatorHistoEMu,denominatorHistoEMu)
				#~ effMuE = TEfficiency(nominatorHistoMuE,denominatorHistoEMu)
				#~ effMuMu = TEfficiency(nominatorHistoMuMu,denominatorHistoMuMu)
				#~ effMuMuNoTrack = TEfficiency(nominatorHistoMuMuNoTrack,denominatorHistoMuMu)
				#~ 
				#~ 

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
		
		
				latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.55,0.65,"#splitline{"+logEtaCut+", "+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				legend.Draw("same")
				hCanvas.Print("fig/Triggereff_%s_%s_%s_%s_%s_%s.pdf"%(source,region,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
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
				
				effSFNoFit = effSF.Clone()
				effSFNoTrackNoFit = effSF.Clone()
				effOFNoFit = effSF.Clone()
				
			
				hCanvas.DrawFrame(firstBin,0,lastBin,1.2,"; %s ; Efficiency" %(variable.labelX))
				
				fitSF = TF1("fitSF","[0]",fitStart,fitEnd)
				fitSFNoTrack = TF1("fitSFNoTrack","[0]",fitStart,fitEnd)
				fitOF = TF1("fitOF","[0]",fitStart,fitEnd)
				fitSF.SetLineColor(ROOT.kBlack)
				fitSFNoTrack.SetLineColor(ROOT.kRed)
				fitOF.SetLineColor(ROOT.kBlue)
				#~ effSF.Fit("fitSF","BRQE","",fitStart,fitEnd)
				#~ effSFNoTrack.Fit("fitSFNoTrack","BRQE","",fitStart,fitEnd)
				#~ effOF.Fit("fitOF","BRQE","",fitStart,fitEnd)




				legend.Clear()
				legend.AddEntry(effSF,"Ele_17_X_Ele8_X || Mu17_Mu8 || Mu17_TkMu8 ","p")
				#~ legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				legend.AddEntry(effOF,"Mu17_Ele8_X || Ele17_X_Mu8" ,"p")
				#~ legend.AddEntry(effSF,"Same Flavour  %.3f #pm %.3f"%(fitSF.GetParameter(0),fitSF.GetParError(0)),"p")
				#~ legend.AddEntry(effSFNoTrack,"Mu17_Mu8 || Ele_17_X_Ele8_X %.3f #pm %.3f"%(fitSFNoTrack.GetParameter(0),fitSFNoTrack.GetParError(0)),"p")
				#~ legend.AddEntry(effOF,"Opposite Flavour %.3f #pm %.3f"%(fitOF.GetParameter(0),fitOF.GetParError(0)),"p")


				#~ effSFNoTrack.Draw("samep")
				effSF.Draw("samep")
				effOF.Draw("samep")

		
		
				latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.55,0.65,"#splitline{"+logEtaCut+", "+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				legend.Draw("same")
	
				hCanvas.Print("fig/Triggereff_SFvsOF_%s_%s_%s_%s_%s_%s.pdf"%(source,region,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))

				hCanvas.DrawFrame(firstBin,.4,lastBin,1.6,"; %s ; Efficiency SF / Efficiency OF" %(variable.labelX))

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
				
				effSFvsOF = efficiencyRatio(effSF,effOF)

				x= array("f",[firstBin, lastBin]) 
				#~ y= array("f", [1.175, 1.175]) # 1.237
				if "Exclusive" in cut.name:
					y= array("f", [float(meansExclusive[region]), float(meansExclusive[region])]) # 1.237
					ey= array("f", [float(meansExclusive[region])*float(errsExclusive[region]), float(meansExclusive[region])*float(errsExclusive[region])])
					sfLine= ROOT.TF1("sfLine",meansExclusive[region],firstBin, lastBin)
				else:	
					y= array("f", [float(means[region]), float(means[region])]) # 1.237
					ey= array("f", [float(means[region])*float(errs[region]), float(means[region])*float(errs[region])])					
					sfLine= ROOT.TF1("sfLine",means[region],firstBin, lastBin)
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
				

				latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.55,0.65,"#splitline{"+logEtaCut+", "+cut.label1+"}{"+variable.additionalCutsLabel+"}")

				
				legend.Clear()
				legend.AddEntry(effSFvsOF,"Triggerefficiency SF/OF","p")
				if "Exclusive" in cut.name: 
					legend.AddEntry(sfLine,"Mean SF vs OF: %s"%(meansExclusive[region]),"l") 
					legend.AddEntry(ge,"Mean SF vs OF #pm 6.4%","f") 
				else:	
					legend.AddEntry(sfLine,"Mean SF vs OF: %s"%(means[region]),"l") 
					legend.AddEntry(ge,"Mean SF vs OF #pm 6.4%","f") 
				legend.Draw("same")
				ROOT.gPad.RedrawAxis()
				hCanvas.Print("fig/Triggereff_SFvsOF_Syst_%s_%s_%s_%s_%s_%s.pdf"%(source,region,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
		
