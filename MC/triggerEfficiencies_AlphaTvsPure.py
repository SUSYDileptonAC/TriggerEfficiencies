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
config.read("/home/jan/Doktorarbeit/Dilepton/SubmitScripts/Input/Master53X.ini")


etaCuts = {"Inclusive":"((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) ",
			  "Barrel":"abs(eta1)<1.4  && abs(eta2) < 1.4",
			  "Endcap":"1.6<=TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) )",
			}
logEtaCuts = {"Inclusive":"|eta|<2.4",
        		  "Barrel":"|eta|<1.4",
        		  "Endcap":"min one 1.6<|eta|<2.4"
        		}
means = {"Inclusive":"1.014",
        		  "Barrel":"1.010",
        		  "Endcap":"1.028"
        		}
meansExclusive = {"Inclusive":"1.014",
        		  "Barrel":"1.015",
        		  "Endcap":"1.096"
        		}
 
errs = {"Inclusive":"1.014",
        		  "Barrel":"0.064",
        		  "Endcap":"0.064"
        		}
errsExclusive = {"Inclusive":"1.014",
        		  "Barrel":"0.064",
        		  "Endcap":"0.064"
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
	path = mainConfig.path

	if len(argv) ==1:
		log.logHighlighted("No lepton eta selection specified, using inclusive!")
		region = "Inclusive"
	else:
		region = argv[1]

	source = ""
	treesDenominatorEENoTrig = readTrees(path,source,"%s"%(source,),"EE")
	treesDenominatorMuMuNoTrig = readTrees(path,source,"%s"%(source,),"MuMu")
	treesDenominatorEMuNoTrig = readTrees(path,source,"%s"%(source,),"EMu")
	
	
	treesNominatorEENoTrig = readTrees(path,source,"HLTDiEle%s"%(source,),"EE")
	treesNominatorMuMuNoTrig = readTrees(path,source,"HLTDiMu%s"%(source,),"MuMu")
	treesNominatorMuMuNoTrackNoTrig = readTrees(path,source,"HLTDiMuNoTrackerMuon%s"%(source,),"MuMu")
	treesNominatorMuEGNoTrig = readTrees(path,source,"HLTMuEG%s"%(source,),"EMu")
	


	source = "HT"
	log.logHighlighted("Calculating trigger efficiencies on %s triggered dataset"%source)
	log.logHighlighted("Using trees from %s "%path)
	treesDenominatorEE = readTrees(path,source,"%s"%(source,),"EE")
	treesDenominatorMuMu = readTrees(path,source,"%s"%(source,),"MuMu")
	treesDenominatorEMu = readTrees(path,source,"%s"%(source,),"EMu")
	
	
	treesNominatorEE = readTrees(path,source,"HLTDiEle%s"%(source,),"EE")
	treesNominatorMuMu = readTrees(path,source,"HLTDiMu%s"%(source,),"MuMu")
	treesNominatorMuMuNoTrack = readTrees(path,source,"HLTDiMuNoTrackerMuon%s"%(source,),"MuMu")
	treesNominatorMuEG = readTrees(path,source,"HLTMuEG%s"%(source,),"EMu")
	eventCounts = totalNumberOfGeneratedEvents(path,source,"%s"%(source,))

	etaCut = etaCuts[region]
	logEtaCut = logEtaCuts[region]	
	cuts = mainConfig.cuts
	variables = mainConfig.variables
	runs = mainConfig.runs

	

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

	lumi = 12000
	
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
	latex.SetTextSize(0.035)
	latex.SetNDC(True)

	intlumi = ROOT.TLatex()
	intlumi.SetTextAlign(12)
	intlumi.SetTextSize(0.03)
	intlumi.SetNDC(True)					
	
	for run in runs:
		log.logInfo("%s"%run.label)
		for cut in cuts:
			log.logInfo("%s"%cut.label1)
			#~ cutStringTemp = cut.cut%(run.runCut,"deltaR > 0.3","")	
			for variable in variables:
				log.logInfo("%s"%variable.labelX)
				cutString = cut.cut%(run.runCut,variable.additionalCuts,"&& %s") %(etaCut)       			
				cutStringEMu = cut.cut%(run.runCut,variable.additionalCuts," && pt1 > 20 && %s") %(etaCut)
				cutStringMuE = cut.cut%(run.runCut,variable.additionalCuts," && pt2 > 20 && %s") %(etaCut)
				log.logInfo("Full cut string: %s"%(cutString,))

				
				firstBin = variable.firstBin
				#~ if "eta" in variable.variable:
					#~ firstBin = -2.4
				lastBin = variable.nBins*variable.binWidths
				
				
				plot = Plot(variable.variable,cutString,variable.labelX,"Efficiency",variable.nBins,firstBin,lastBin)
				plotEMu = Plot(variable.variable,cutStringEMu,variable.labelX,"Efficiency",variable.nBins,firstBin,lastBin)
				plotMuE = Plot(variable.variable,cutStringMuE,variable.labelX,"Efficiency",variable.nBins,firstBin,lastBin)				
	
				denominatorStackEE = TheStack(processes,lumi,plot,treesDenominatorEE,"None",1.0,1.0,1.0)		
				denominatorStackMuMu = TheStack(processes,lumi,plot,treesDenominatorMuMu,"None",1.0,1.0,1.0)		
				denominatorStackMuEG = TheStack(processes,lumi,plot,treesDenominatorEMu,"None",1.0,1.0,1.0)	
					
				nominatorStackEE = TheStack(processes,lumi,plot,treesNominatorEE,"None",1.0,1.0,1.0)		
				nominatorStackMuMu = TheStack(processes,lumi,plot,treesNominatorMuMu,"None",1.0,1.0,1.0)		
				#~ nominatorStackMuMu = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
				#~ nominatorStackMuMuNoTrack = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrack,"None",1.0,1.0,1.0)		
				nominatorStackMuEG = TheStack(processes,lumi,plot,treesNominatorMuEG,"None",1.0,1.0,1.0)		
	
				denominatorStackEENoTrig = TheStack(processes,lumi,plot,treesDenominatorEENoTrig,"None",1.0,1.0,1.0)		
				denominatorStackMuMuNoTrig = TheStack(processes,lumi,plot,treesDenominatorMuMuNoTrig,"None",1.0,1.0,1.0)		
				denominatorStackMuEGNoTrig = TheStack(processes,lumi,plot,treesDenominatorEMuNoTrig,"None",1.0,1.0,1.0)	
					
				nominatorStackEENoTrig = TheStack(processes,lumi,plot,treesNominatorEENoTrig,"None",1.0,1.0,1.0)		
				nominatorStackMuMuNoTrig = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrig,"None",1.0,1.0,1.0)		
				#~ nominatorStackMuMuNoTrig = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrackNoTrig,"None",1.0,1.0,1.0)		
				#~ nominatorStackMuMuNoTrackNoTrig = TheStack(processes,lumi,plot,treesNominatorMuMuNoTrackNoTrig,"None",1.0,1.0,1.0)		
				nominatorStackMuEGNoTrig = TheStack(processes,lumi,plot,treesNominatorMuEGNoTrig,"None",1.0,1.0,1.0)		
		
				denominatorHistoEE = denominatorStackEE.theHistogram
				denominatorHistoMuMu = denominatorStackMuMu.theHistogram
				denominatorHistoMuEG = denominatorStackMuEG.theHistogram
				
				nominatorHistoEE = nominatorStackEE.theHistogram
				nominatorHistoMuMu = nominatorStackMuMu.theHistogram
				#~ nominatorHistoMuMuNoTrack = nominatorStackMuMuNoTrack.theHistogram
				nominatorHistoMuEG = nominatorStackMuEG.theHistogram
		
				denominatorHistoEENoTrig = denominatorStackEENoTrig.theHistogram
				denominatorHistoMuMuNoTrig = denominatorStackMuMuNoTrig.theHistogram
				denominatorHistoMuEGNoTrig = denominatorStackMuEGNoTrig.theHistogram
				
				nominatorHistoEENoTrig = nominatorStackEENoTrig.theHistogram
				nominatorHistoMuMuNoTrig = nominatorStackMuMuNoTrig.theHistogram
				#~ nominatorHistoMuMuNoTrackNoTrig = nominatorStackMuMuNoTrackNoTrig.theHistogram
				nominatorHistoMuEGNoTrig = nominatorStackMuEGNoTrig.theHistogram

		
	
				
				denominatorHistoSF = denominatorHistoEE.Clone()
				denominatorHistoSF.Add(denominatorHistoMuMu.Clone())
				denominatorHistoOF = denominatorHistoMuEG.Clone()
				
				nominatorHistoSF = nominatorHistoEE.Clone()
				nominatorHistoSF.Add(nominatorHistoMuMu.Clone())
				
				nominatorHistoOF = nominatorHistoMuEG.Clone()
				

				
				
				denominatorHistoSFNoTrig = denominatorHistoEENoTrig.Clone()
				denominatorHistoSFNoTrig.Add(denominatorHistoMuMuNoTrig.Clone())
				denominatorHistoOFNoTrig = denominatorHistoMuEGNoTrig.Clone()
				
				nominatorHistoSFNoTrig = nominatorHistoEENoTrig.Clone()				
				nominatorHistoSFNoTrig.Add(nominatorHistoMuMuNoTrig.Clone())
				
				nominatorHistoOFNoTrig = nominatorHistoMuEGNoTrig.Clone()
				
				effSF = TGraphAsymmErrors(nominatorHistoSF,denominatorHistoSF,"cp")
				#~ effSFNoTrack = TGraphAsymmErrors(nominatorHistoSFNoTrack,denominatorHistoSF,"cp")
				effOF = TGraphAsymmErrors(nominatorHistoOF,denominatorHistoOF,"cp")
				
				effSFNoTrig = TGraphAsymmErrors(nominatorHistoSFNoTrig,denominatorHistoSFNoTrig,"cp")
				#~ effSFNoTrackNoTrig = TGraphAsymmErrors(nominatorHistoSFNoTrackNoTrig,denominatorHistoSFNoTrig,"cp")
				effOFNoTrig = TGraphAsymmErrors(nominatorHistoOFNoTrig,denominatorHistoOFNoTrig,"cp")




				effRatioSF = efficiencyRatio(effSF,effSFNoTrig)
				effRatioOF = efficiencyRatio(effOF,effOFNoTrig)
				
				effRatioSF.SetMarkerStyle(21)
				effRatioOF.SetMarkerStyle(22)
				effRatioOF.SetMarkerColor(ROOT.kBlue)
				effRatioOF.SetLineColor(ROOT.kBlue)
				
				#~ hCanvas.DrawFrame(firstBin,0.6,lastBin,1.4,"; %s ; Efficiency #alpha_{T} based / True Efficiency" %(variable.labelX))
				hCanvas.DrawFrame(firstBin,0.8,lastBin,1.2,"; %s ; Measured Efficiency / True Efficiency" %(variable.labelX))


				x= array("f",[firstBin, lastBin]) 
				#~ y= array("f", [1.175, 1.175]) # 1.237
				y= array("f", [1.0, 1.0]) # 1.237
				ex= array("f", [0.,0.])
				ey= array("f", [0.01, 0.01])
				ge= ROOT.TGraphErrors(2, x, y, ex, ey)
				ge.SetFillColor(ROOT.kOrange-9)
				ge.SetFillStyle(1001)
				ge.SetLineColor(ROOT.kWhite)
				#~ ge.Draw("SAME 3")

				sfLine= ROOT.TF1("sfLine","1.0",firstBin, lastBin)
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
				#~ legend.AddEntry(ge,"1.0 #pm 1%","f")


		
		
				latex.DrawLatex(0.15, 0.96, "CMS Private Work  #sqrt{s} = 8 TeV, %s    #scale[0.6]{#int}Ldt = %s fb^{-1}"%(run.label,run.lumi))
				intlumi.DrawLatex(0.6,0.65,"#splitline{"+cut.label1+"}{"+variable.additionalCutsLabel+"}")
				legend.Draw("same")
				print source
				if source == "HT" or source == "AlphaT":
					hCanvas.Print("fig/Triggereff_AlphaTSyst_%s_%s_%s_%s_%s_%s.pdf"%(source,region,cut.name,run.plotName,variable.plotName,variable.additionalPlotName))
				else:
					hCanvas.Print("fig/Triggereff_AlphaTSyst_%s_%s_%s_%s_%s.pdf"%(cut.name,region,run.plotName,variable.plotName,variable.additionalPlotName))	
				
				
	
