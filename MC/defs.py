from math import sqrt
import ROOT
class Constant:
	val = 0.
	printval = 0.
	err = 0.
	
class Constants:
	class Trigger:
		class EffEE(Constant):
			val = 0.912
			err = 0.912 * 0.05
		class EffEMu(Constant):
			val = 0.5*(0.918+0.883)
			err = 0.5*(0.918+0.883) * 0.05
			#~ val = 0.95
			#~ err = 0.5*(0.918+0.883) * 0.05

		class EffMuMu(Constant):
			val = 0.936
			err = 0.936 * 0.05

	class Pt2010:
		class RInOut(Constant):
			val = 0.1376
			err = sqrt(0.0014**2+0.0344**2)
		class RMuE(Constant):
			val =1.2
			err =1.2*0.1			
		
	class Pt2020:
		class RInOut(Constant):
			val =0.07
			err =0.07*0.25
		class RMuE(Constant):
			val =1.2
			err =1.2*0.1
	class Lumi:
		val = 12000
		printval = "12.0"
		err = 0.045*12000
		#~ val = 9200
		#~ printval = "9.2"
		#~ err = 0.045*9200
		#~ val = 5230
		#~ printval = "5.23"
		#~ err = 0.045*5230
		#~ val = 6770
		#~ printval = "6.77"
		#~ err = 0.045*6770
		#~ val = 5051
		#~ printval = "5.05"
		#~ err = 0.045*5051
		
class Signals:
	class SUSY1:
		subprocesses = ["SUSY_CMSSM_4610_202_Summer12"]
		label 		 = "CMSSM 4610/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed
		uncertainty	 = 0.
		scaleFac     = 1.
	class SUSY2:
		subprocesses = ["SUSY_CMSSM_4500_188_Summer12"]
		label 		 = "CMSSM 4500/188"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+1
		uncertainty	 = 0.
		scaleFac     = 1.
	class SUSY3:
		subprocesses = ["SUSY_CMSSM_4580_202_Summer12"]
		label 		 = "CMSSM 4580/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+2
		uncertainty	 = 0.
		scaleFac     = 1.
	class SUSY4:
		subprocesses = ["SUSY_CMSSM_4640_202_Summer12"]
		label 		 = "CMSSM 4640/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+3
		uncertainty	 = 0.
		scaleFac     = 1.
	class SUSY5:
		subprocesses = ["SUSY_CMSSM_4700_216_Summer12"]
		label 		 = "CMSSM 4700/216"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+4
		uncertainty	 = 0.
		scaleFac     = 1.
		
class Backgrounds:
	
	class TTJets:
		subprocesses = ["TTJets_madgraph_Summer12"]
		label = "Madgraph t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.15
		scaleFac     = 1.0
	class TTJetsSC:
		subprocesses = ["TTJets_MGDecays_madgraph_Summer12"]
		label = "Madgraph t#bar{t} w/SC"
		fillcolor = 855
		linecolor = ROOT.kBlack 
		uncertainty = 0.15
		scaleFac     = 1.0
	class TT:
		subprocesses = ["TT_Powheg_Summer12_v2"] 
		label = "Powheg t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.15
		scaleFac     = 1.0
		#~ scaleFac     = 0.71
	class TT_Dileptonic:
		subprocesses = ["TT_Dileptonic_Powheg_Summer12_v1"] 
		label = "Powheg t#bar{t} Dileptonic"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.15
		scaleFac     = 1.0
		#~ scaleFac     = 0.71
	class TT_MCatNLO:
		subprocesses = ["TT_MCatNLO_Summer12_v1"] 
		label = "MCatNLO t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.15
		scaleFac     = 1.0
		#~ scaleFac     = 0.71
	class Diboson:
		subprocesses = ["ZZJetsTo2L2Q_madgraph_Summer12","ZZJetsTo2L2Nu_madgraph_Summer12","ZZJetsTo4L_madgraph_Summer12","WZJetsTo3LNu_madgraph_Summer12","WZJetsTo2L2Q_madgraph_Summer12","WWJetsTo2L2Nu_madgraph_Summer12"]
		label = "WW,WZ,ZZ"
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
	class Rare:
		subprocesses = ["WWWJets_madgraph_Summer12","WWGJets_madgraph_Summer12","WWZNoGstarJets_madgraph_Summer12","TTGJets_madgraph_Summer12","WZZNoGstar_madgraph_Summer12","TTWJets_madgraph_Summer12","TTZJets_madgraph_Summer12","TTWWJets_madgraph_Summer12"]
		label = "Rare SM"
		fillcolor = 630
		linecolor = ROOT.kBlack
		uncertainty = 0.5
		scaleFac     = 1.		
	class DrellYan:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "Z+jets"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
	class SingleTop:
		subprocesses = ["TBar_tWChannel_Powheg_Summer12","TBar_tChannel_Powheg_Summer12","TBar_sChannel_Powheg_Summer12","T_tWChannel_Powheg_Summer12","T_tChannel_Powheg_Summer12","T_sChannel_Powheg_Summer12"]
		label = "t/#bar{t}+jets"
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.		
		
class runRanges:
	class RunA:
		plotName = "RunA"
		runCut = "runNr >= 190456 && runNr <=193621"
		label = "Run2012A"
		lumi = "0.8"
	class RunB:
		plotName ="RunB"
		runCut = "runNr >= 193834 && runNr <=196531"
		label = "Run2012B"
		lumi = "4.4"
	class RunAB:
		plotName = "RunAB"
		runCut = "runNr >= 190456 && runNr <=196531"
		label = "Run2012A+B"
		lumi = "5.2"
	class RunC:
		plotName = "RunC"
		runCut = "runNr >= 198022 && runNr <=203755"
		label = "Run2012C"
		lumi = "6.9"
	class RunABC:
		plotName = "RunABC"
		runCut = "runNr >= 190456 && runNr <=203755"
		label = "Run2012A+B+C"
		lumi = "12.0"
	class RunD:
		plotName = "RunD"
		runCut = "runNr >= 203773 && runNr <=209465"
		label = "Run2012D"
		lumi = "7.3"
	class Full2012:
		plotName = "Full2012"
		runCut = "runNr >= 190456 && runNr <=209465"
		label = "Full 2012"
		lumi = "19.4"
	class RunMC:
		plotName = "MC"
		runCut = "runNr == 1"
		label = "Simulation"
		lumi = "12.0"
class dependendies:
	class nJets_pt2010:
		plotName = "nJets"
		variable = "nJets"
		nBins = 10
		binWidths = 1
		firstBin = 0
		labelX = "N_{jets}"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) "
		additionalCutsLabel = "p_{T} > 20(10) GeV "
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 10		
	class nJets_pt2020:
		plotName = "nJets"
		variable = "nJets"
		nBins = 10
		binWidths = 1
		firstBin = 0		
		labelX = "N_{jets}"
		additionalCuts = "&& (pt1 > 20 && pt2 > 20) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 10		
	class leadingPt_trailing10:
		plotName = "pt2"
		variable = "(pt2>pt1)*pt2+(pt1>pt2)*pt1"
		nBins = 18
		binWidths = 5
		firstBin = 10
		labelX = "leading p_{T} [GeV]"
		additionalCuts = "&& ((pt2>pt1)*pt1+(pt1>pt2)*pt2) > 10"
		additionalCutsLabel = "trailing pt > 10 GeV"
		additionalPlotName = "trailingPt10"
		fitStart = 20
		fitEnd = 100		
	class leadingPt_trailing20:
		plotName = "pt2"
		variable = "(pt2>pt1)*pt2+(pt1>pt2)*pt1"
		nBins = 18
		binWidths = 5
		firstBin = 10
		labelX = "leading p_{T} [GeV]"
		additionalCuts = "&& ((pt2>pt1)*pt1+(pt1>pt2)*pt2) > 20"
		additionalCutsLabel = "trailing pt > 20 GeV"
		additionalPlotName = "trailingPt20"
		fitStart = 20
		fitEnd = 100		
	class trailingPt_leading20:
		plotName = "pt1"
		variable = "(pt2>pt1)*pt1+(pt1>pt2)*pt2"
		nBins = 18
		binWidths = 5
		firstBin = 10
		labelX = "trailing p_{T} [GeV]"
		additionalCuts = "&& ((pt2>pt1)*pt2+(pt1>pt2)*pt1) > 20"
		additionalCutsLabel = "leading pt > 20 GeV"
		additionalPlotName = "leadingPt20"
		fitStart = 20
		fitEnd = 100		
	class trailingPt_leading30:
		plotName = "pt1"
		variable = "(pt2>pt1)*pt1+(pt1>pt2)*pt2"
		nBins = 9
		binWidths = 10
		firstBin = 20
		labelX = "trailing p_{T} [GeV]"
		additionalCuts = "&& ((pt2>pt1)*pt2+(pt1>pt2)*pt1) > 30"
		additionalCutsLabel = "leading pt > 30 GeV"
		additionalPlotName = "leadingPt30"
		fitStart = 20
		fitEnd = 100		
	class mll_pt2020:
		plotName = "Mll"
		variable = "p4.M()"
		nBins = 19
		binWidths = 10
		firstBin = 15
		labelX = "m(ll) [GeV]"
		additionalCuts = "&& pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 20
		fitEnd = 200		
	class mll_pt2010:
		plotName = "Mll"
		variable = "p4.M()"
		nBins = 19
		binWidths = 10
		firstBin = 15
		labelX = "m(ll) [GeV]"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 20
		fitEnd = 200		
	class ptll_pt2020:
		plotName = "ptll"
		variable = "p4.Pt()"
		nBins = 19
		binWidths = 10
		firstBin = 15
		labelX = "p_{T}(ll) [GeV]"
		additionalCuts = "&& pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 200		
	class ptll_pt2010:
		plotName = "ptll"
		variable = "p4.Pt()"
		nBins = 19
		binWidths = 10
		firstBin = 15
		labelX = "p_T{}(ll) [GeV]"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 200		
	class met:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 200		
	class met_lowMll:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && p4.M() < 70"
		additionalCutsLabel = "p_{T} > 20(10) GeV m(ll) < 70 GeV"
		additionalPlotName = "pt2010_lowMll"
		fitStart = 0
		fitEnd = 200			
	class met_HighMll:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && p4.M() > 120"
		additionalCutsLabel = "p_{T} > 20(10) GeV m(ll) > 120 GeV"
		additionalPlotName = "pt2010_highMll"
		fitStart = 0
		fitEnd = 200			
	class met_pt2020:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "&& (pt1 > 20 && pt2 > 20 ) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 200			
	class met_pt2020_lowMll:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "&& (pt1 > 20 && pt2 > 20 ) && p4.M() < 70 "
		additionalCutsLabel = "p_{T} > 20 GeV m(ll) < 70 GeV"
		additionalPlotName = "pt2020_lowMll"
		fitStart = 0
		fitEnd = 200			
	class met_pt2020_HighMll:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "&& (pt1 > 20 && pt2 > 20 ) && p4.M() > 120 "
		additionalCutsLabel = "p_{T} > 20 GeV m(ll) > 120 GeV"
		additionalPlotName = "pt2020_highMll"
		fitStart = 0
		fitEnd = 200			
	class nVtx_pt2020:
		plotName = "nVtx"
		variable = "nVertices"
		nBins = 30
		binWidths = 1
		firstBin = 0
		labelX = "N_{Vertices}"
		additionalCuts = "&& (pt1 > 20 && pt2 > 20 ) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 30			
	class nVtx_pt2010:
		plotName = "nVtx"
		variable = "nVertices"
		nBins = 30
		binWidths = 1
		firstBin = 0
		labelX = "N_{Vertices}"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) ||(pt1>10 && pt2>20)) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 30					
	class eta1_pt2010:
		plotName = "Eta1"
		variable = "(pt2>pt1)*eta1+(pt1>pt2)*eta2"
		nBins = 13
		binWidths = 0.2
		firstBin = -2.4
		labelX = "#eta_{trailing lepton}"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = -2.4
		fitEnd = 2.4			
	class eta1_pt2020:
		plotName = "Eta1"
		variable = "(pt2>pt1)*eta1+(pt1>pt2)*eta2"
		nBins = 13
		binWidths = 0.2
		firstBin = -2.4
		labelX = "#eta_{trailing lepton}"
		additionalCuts = "&& pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = -2.4
		fitEnd = 2.4			
	class ht_pt2010:
		plotName = "HT"
		variable = "ht"
		nBins = 20
		binWidths = 20
		firstBin = 0
		labelX = "H_{T} [GeV]"
		additionalCuts = "&& ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 400			
	class ht_pt2020:
		plotName = "HT"
		variable = "ht"
		nBins = 20
		binWidths = 20
		firstBin = 0
		labelX = "H_{T} [GeV]"
		additionalCuts = "&& pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 400					

class selections:
	class inclusive:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && %s %s %s )"
		label1 = " |#eta| < 2.4 "
		name = "Inclusive"
	class HighMET:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && met > 100 && %s %s %s )"
		label1 = " |#eta| < 2.4 met > 100"
		name = "HighMET"
	class SignalCentral:
		cut = "weight*(chargeProduct < 0 && ((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && deltaR > 0.3 && %s %s %s )"
		label1 = " Signal region central"
		name = "SignalCentral"
	class SignalForward:
		cut = "weight*(chargeProduct < 0  && ((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  1.4 <= TMath::Max(abs(eta1),abs(eta2)) && deltaR > 0.3  && %s %s %s )"
		label1 = " Signal region forward"
		name = "SignalForward"
	class HighHT:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && ht > 200 && %s %s %s )"
		label1 = " |#eta| < 2.4  ht > 200"
		name = "HighHT"
	class HighHTCentral:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<1.4  && abs(eta2) < 1.4 && deltaR > 0.3  && ht > 200 && %s %s %s )"
		label1 = " |#eta| < 1.4  ht > 200"
		name = "HighHTCentral"
	class HighHTForward:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta2) < 2.4 && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && deltaR > 0.3  && ht > 200 && %s %s %s )"
		label1 = "at least one |#eta| > 1.6  ht > 200"
		name = "HighHTForward"
	class HighHTHighMET:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && ht > 150 && met > 50 && %s %s %s )"
		label1 = " |#eta| < 2.4  ht > 150 met > 50"
		name = "HighHTHighMET"
	class HighHTHighMETBarrel:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<1.4  && abs(eta2) < 1.4 && deltaR > 0.3  && ht > 150 && met > 50 && %s %s %s )"
		label1 = " |#eta| < 1.4  ht > 150 met > 50"
		name = "HighHTHighMETBarrel"
	class HighNJets:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3  && nJets >=2 && %s %s %s )"
		label1 = " |#eta| < 2.4  nJets >= 2"
		name = "HighnJets"
class mainConfig:
	path = "/home/jan/Trees/TriggerEfficiency"
	source = "HT"
	#~ cuts = [selections.HighHT,selections.HighHTHighMET,selections.HighMET]
	#~ cuts = [selections.HighHTHighMET,selections.HighHTHighMETBarrel]
	cuts = [selections.HighHTCentral,selections.HighHTForward]
	#~ cuts = [selections.HighNJets]
	variables = [dependendies.leadingPt_trailing20,dependendies.trailingPt_leading20,dependendies.trailingPt_leading30,dependendies.nJets_pt2020,dependendies.mll_pt2020,dependendies.ptll_pt2020,dependendies.eta1_pt2020,dependendies.met_pt2020,dependendies.met_pt2020_HighMll,dependendies.met_pt2020_lowMll,dependendies.nVtx_pt2020,dependendies.ht_pt2020]
	#~ variables = [dependendies.mll_pt2020,dependendies.ptll_pt2010,dependendies.ptll_pt2020,dependendies.met,dependendies.eta1_pt2010,dependendies.eta1_pt2020,dependendies.met_HighMll,dependendies.met_lowMll,dependendies.met_pt2020,dependendies.met_pt2020_HighMll,dependendies.met_pt2020_lowMll,dependendies.nVtx_pt2010,dependendies.nVtx_pt2020,dependendies.ht_pt2010,dependendies.ht_pt2020]
	#~ variables = [dependendies.met_pt2020_lowMll,dependendies.nVtx_pt2010,dependendies.nVtx_pt2020,dependendies.ht_pt2010,dependendies.ht_pt2020]
	#variables = [dependendies.trailingPt_leading30]

	runs = [runRanges.RunMC]
	
# Color definition
#==================
defineMyColors = {
        'Black' : (0, 0, 0),
        'White' : (255, 255, 255),
        'Red' : (255, 0, 0),
        'DarkRed' : (128, 0, 0),
        'Green' : (0, 255, 0),
        'Blue' : (0, 0, 255),
        'Yellow' : (255, 255, 0),
        'Orange' : (255, 128, 0),
        'DarkOrange' : (255, 64, 0),
        'Magenta' : (255, 0, 255),
        'KDEBlue' : (64, 137, 210),
        'Grey' : (128, 128, 128),
        'DarkGreen' : (0, 128, 0),
        'DarkSlateBlue' : (72, 61, 139),
        'Brown' : (70, 35, 10),

        'MyBlue' : (36, 72, 206),
        'MyDarkBlue' : (18, 36, 103),
        'MyGreen' : (70, 164, 60),
        'AnnBlueTitle' : (29, 47, 126),
        'AnnBlue' : (55, 100, 255),
#        'W11AnnBlue' : (0, 68, 204),
#        'W11AnnBlue' : (63, 122, 240),
    }


myColors = {
            'W11ttbar':  855,
            'W11singlet':  854,
            'W11ZLightJets':  401,
            'W11ZbJets':  400,
            'W11WJets':  842,
            'W11Diboson':  920,
            'W11AnnBlue': 856,
            'W11Rare':  630,
            }

