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
	class Run92:
		plotName = "Run92"
		runCut = "runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)"
		label = "Run92"
		lumi = "9.2"
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
class dependendies:
	class nJets_pt2010:
		plotName = "nJets"
		variable = "nJets"
		nBins = 10
		binWidths = 1
		firstBin = 0
		labelX = "N_{jets}"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) "
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
		additionalCuts = "(pt1 > 20 && pt2 > 20) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 10		
	class leadingPt_trailing10:
		plotName = "pt2"
		variable = "(pt2>pt1)*pt2+(pt1>pt2)*pt1"
		nBins = 9
		binWidths = 10
		firstBin = 20
		labelX = "leading p_{T} [GeV]"
		additionalCuts = "((pt2>pt1)*pt1+(pt1>pt2)*pt2) > 10"
		additionalCutsLabel = "trailing pt > 10 GeV"
		additionalPlotName = "trailingPt10"
		fitStart = 20
		fitEnd = 100		
	class leadingPt_trailing20:
		plotName = "pt2"
		variable = "(pt2>pt1)*pt2+(pt1>pt2)*pt1"
		nBins = 9
		binWidths = 10
		firstBin = 20
		labelX = "leading p_{T} [GeV]"
		additionalCuts = "((pt2>pt1)*pt1+(pt1>pt2)*pt2) > 20"
		additionalCutsLabel = "trailing pt > 20 GeV"
		additionalPlotName = "trailingPt20"
		fitStart = 20
		fitEnd = 100			
	class trailingPt_leading20:
		plotName = "pt1"
		variable = "(pt2>pt1)*pt1+(pt1>pt2)*pt2"
		nBins = 9
		binWidths = 10
		firstBin = 20
		labelX = "trailing p_{T} [GeV]"
		additionalCuts = "((pt2>pt1)*pt2+(pt1>pt2)*pt1) > 20"
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
		additionalCuts = "((pt2>pt1)*pt2+(pt1>pt2)*pt1) > 30"
		additionalCutsLabel = "leading pt > 30 GeV"
		additionalPlotName = "leadingPt30"
		fitStart = 20
		fitEnd = 100			

	class mll_pt2020:
		plotName = "Mll"
		variable = "p4.M()"
		nBins = 9
		binWidths = 20
		firstBin = 20
		labelX = "m(ll) [GeV]"
		additionalCuts = "pt1 > 30 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 20
		fitEnd = 200			
	class mll_pt2010:
		plotName = "Mll"
		variable = "p4.M()"
		nBins = 9
		binWidths = 20
		firstBin = 20
		labelX = "m(ll) [GeV]"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 20
		fitEnd = 200			
	class ptll_pt2020:
		plotName = "ptll"
		variable = "p4.Pt()"
		nBins = 9
		binWidths = 20
		firstBin = 15
		labelX = "p_{T}(ll) [GeV]"
		additionalCuts = "pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 200			
	class ptll_pt2010:
		plotName = "ptll"
		variable = "p4.Pt()"
		nBins = 9
		binWidths = 20
		firstBin = 15
		labelX = "p_T{}(ll) [GeV]"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 200					
	class ht_pt2010:
		plotName = "HT"
		variable = "ht"
		nBins = 10
		binWidths = 40
		firstBin = 0
		labelX = "H_{T} [GeV]"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 400			
	class ht_pt2020:
		plotName = "HT"
		variable = "ht"
		nBins = 10
		binWidths = 40
		firstBin = 0
		labelX = "H_{T} [GeV]"
		additionalCuts = "pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 400			
	class met:
		plotName = "MET"
		variable = "met"
		nBins = 10
		binWidths = 20
		firstBin = 0
		labelX = "E_{T}^{miss} [GeV]"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
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
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && p4.M() < 70"
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
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && p4.M() > 120"
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
		additionalCuts = "(pt1 > 20 && pt2 > 20 ) "
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
		additionalCuts = "(pt1 > 20 && pt2 > 20 ) && p4.M() < 70 "
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
		additionalCuts = "(pt1 > 20 && pt2 > 20 ) && p4.M() > 120 "
		additionalCutsLabel = "p_{T} > 20 GeV m(ll) > 120 GeV"
		additionalPlotName = "pt2020_highMll"
		fitStart = 0
		fitEnd = 200			
	class nVtx_pt2020:
		plotName = "nVtx"
		variable = "nVertices"
		nBins = 15
		binWidths = 2
		firstBin = 0
		labelX = "N_{Vertices}"
		additionalCuts = "(pt1 > 20 && pt2 > 20 ) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 30			
	class nVtx_pt2010:
		plotName = "nVtx"
		variable = "nVertices"
		nBins = 15
		binWidths = 2
		firstBin = 0
		labelX = "N_{Vertices}"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) ||(pt1>10 && pt2>20)) "
		additionalCutsLabel = "p_{T} > 20 GeV "
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 30			
	class eta1_pt2010:
		plotName = "Eta1"
		variable = "abs((pt2>pt1)*eta1+(pt1>pt2)*eta2)"
		nBins = 8
		binWidths = 0.3
		firstBin = 0
		labelX = "#eta_{trailing lepton}"
		additionalCuts = "((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 ))"
		additionalCutsLabel = "p_{T} > 20(10) GeV"
		additionalPlotName = "pt2010"
		fitStart = 0
		fitEnd = 2.4			
	class eta1_pt2020:
		plotName = "Eta1"
		variable = "abs((pt2>pt1)*eta1+(pt1>pt2)*eta2)"
		nBins = 6
		binWidths = 0.4
		firstBin = 0
		labelX = "#eta_{trailing lepton}"
		additionalCuts = "pt1 > 20 && pt2 > 20"
		additionalCutsLabel = "p_{T} > 20 GeV"
		additionalPlotName = "pt2020"
		fitStart = 0
		fitEnd = 2.4				

class selections:
	class inclusive:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20  && %s && %s %s  )"
		label1 = " |#eta| < 2.4 "
		name = "Inclusive"
	class HighMET:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20 && met > 100 && %s && %s %s )"
		label1 = " |#eta| < 2.4 met > 100"
		name = "HighMET"
	class HighHT:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20 && ht > 200 && %s && %s %s )"
		#label1 = " |#eta| < 2.4  ht > 200"
		label1 = "ht > 200"
		name = "HighHT"
	class HighHTExclusive:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20 && ht > 200 && %s && !(nJets >= 2 && met > 100) && %s %s )"
		#label1 = " |#eta| < 2.4  ht > 200"
		label1 = "ht > 200"
		name = "HighHTExclusive"
	class HighHTHighMET:
		cut = "weight*(chargeProduct < 0  && abs(eta1)<2.4  && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20  && ht > 150 && met > 50 && %s && %s %s )"
		label1 = " |#eta| < 2.4  ht > 150 met > 50"
		name = "HighHTHighMET"	
		#~ name = "InclusiveBarrel"
		#~ name = "HighMETBarrel"
		#~ name = "HighHTBarrel"
		#~ name = "HighHTEndcap"

class mainConfig:
	path = "/home/jan/Trees/HTTreesSyncd"
	source = "AlphaT"
	cuts = [selections.HighHT]
	#~ cuts = [selections.HighHT,selections.HighHTBarrel]

	variables = [dependendies.leadingPt_trailing10,dependendies.leadingPt_trailing20,dependendies.trailingPt_leading20,dependendies.trailingPt_leading30,dependendies.mll_pt2020,dependendies.met_pt2020,dependendies.ht_pt2020,dependendies.nJets_pt2020,dependendies.nVtx_pt2020,dependendies.eta1_pt2020]
	#~ variables = [dependendies.eta1_pt2020]
	#~ runs = [runRanges.RunABC,runRanges.RunC,runRanges.RunA,runRanges.RunB,runRanges.RunD,runRanges.Full2012]
	#runs = [runRanges.RunABC]
	runs = [runRanges.Run92]
	
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

