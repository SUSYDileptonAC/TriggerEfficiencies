### Functions for data handling ###
import ROOT
from ROOT import TH1F, THStack
from defs import mainConfig
from ConfigParser import ConfigParser
config = ConfigParser()
config.read("/home/jan/Doktorarbeit/Dilepton/projects/SubmitScripts/Input/Master53X.ini")

config42 = ConfigParser()
config42.read("/home/jan/Doktorarbeit/Dilepton/projects/SubmitScripts/Input/Input/Master53X.ini")





def readTreeFromFile(path,tree, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV22DileptonTriggerEfficiency%sFinalTrees/%sDileptonTree"%(path,tree, dileptonCombination))
	#~ print "%s/cutsV22DileptonTrigger%sFinalTrees/%sDileptonTree"%(path,tree, dileptonCombination)
	

	return result
	
	
def totalNumberOfGeneratedEvents(path,source,tree):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}

	for sampleName, filePath in getFilePathsAndSampleNames(path,source,tree).iteritems():
		#~ print filePath
		rootFile = TFile(filePath, "read")
		result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)				
	return result
	
def readTrees(path,source,tree, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	print tree
	for sampleName, filePath in getFilePathsAndSampleNames(path,source,tree).iteritems():
		#~ print sampleName
		result[sampleName] = readTreeFromFile(filePath, tree,dileptonCombination)
		
	return result


	
def getFilePathsAndSampleNames(path,source,tree):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	#~ print path	
	#~ print tree
	#~ print "%s/sw532*cutV22DileptonTrigger*.root"%(path,)
	for filePath in glob("%s/sw532*cutsV22DileptonTrigger*.root"%(path,)):		
		#~ print filePath
		sampleName = match(".*sw532v.*\.cutsV22DileptonTrigger.*\.(.*).root", filePath).groups()[0]			
		#for the python enthusiats: yield sampleName, filePath is more efficient here :)
		result[sampleName] = filePath
	return result


	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1):
	"""
	tree: tree to create histo from)
	variable: variable to plot (must be a branch of the tree)
	weight: weights to apply (e.g. "var1*(var2 > 15)" will use weights from var1 and cut on var2 > 15
	nBins, firstBin, lastBin: number of bins, first bin and last bin (same as in TH1F constructor)
	nEvents: number of events to process (-1 = all)
	"""
	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable
	name = "%x"%(randint(0, maxint))
	#~ print tree
	#~ print variable
	#~ print weight
	#~ print nBins
	#~ print firstBin
	#~ print lastBin
	result = TH1F(name, "", nBins, firstBin, lastBin)
	result.Sumw2()

	#~ print name
	tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
	#~ tree.Scan("%s>>%s"%(variable, name), weight,"runNr:lumiSec:eventNr")
	return result


def createMyColors():
    iIndex = 2000
    from defs import defineMyColors
    from defs import myColors

    containerMyColors = []
    for color in defineMyColors.keys():
        tempColor = ROOT.TColor(iIndex,
            float(defineMyColors[color][0]) / 255, float(defineMyColors[color][1]) / 255, float(defineMyColors[color][2]) / 255)
        containerMyColors.append(tempColor)

        myColors.update({ color: iIndex })
        iIndex += 1

    return containerMyColors
    
def getDataHist(plot,tree1,tree2="None"):
	histo = TH1F()
	histo2 = TH1F()
	if mainConfig.compare2011 or (mainConfig.plot2011 and mainConfig.plot53X):
		dataname = "MergedData2011"

	else: 
		dataname = "MergedData"

	for name, tree in tree1.iteritems():
		if name == dataname:
			#~ print "hier"
			histo = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
	if tree2 != "None":		
		for name, tree in tree2.iteritems():
			if name == dataname:
				#~ print "hier"
				histo2 = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
				histo.Add(histo2.Clone())		
	return histo	
				
def getDataHist42(plot,tree1,tree2="None"):
	histo = TH1F()
	histo2 = TH1F()

	for name, tree in tree1.iteritems():
		if name == "Data2011_42":
			#~ print "hier"
			histo = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
	if tree2 != "None":		
		for name, tree in tree2.iteritems():
			if name == "Data2011_42":
				#~ print "hier"
				histo2 = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
				histo.Add(histo2.Clone())		
	return histo			
    
class Process:
	samples = []
	xsecs = []
	nEvents = []
	label = ""
	theColor = 0
	theLineColor = 0 
	histo = ROOT.TH1F()
	uncertainty = 0.
	scaleFac = 1.
	
	def __init__(self, samplename=["none"],Counts={"none":-1},labels = "none",color=0,lineColor=0,uncertainty=0.,scaleFac=1.):
		self.samples = []
		self.xsecs = []
		self.nEvents = []
		self.label = labels
		self.theColor = color
		self.theLineColor = lineColor
		self.histo.SetLineColor(lineColor)
		self.histo.SetFillColor(color)
		self.uncertainty = uncertainty
		self.scaleFac = scaleFac
		for sample in samplename:
			self.samples.append(sample)
			if mainConfig.plot2011:
				self.xsecs.append(eval(config42.get(sample,"crosssection")))
			else:
				self.xsecs.append(eval(config.get(sample,"crosssection")))
			self.nEvents.append(Counts[sample])

		
	def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.):
		nEvents=-1
		self.histo = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		#~ plot.cuts = plot.cuts.replace("met","met*%f"%(shift,))
		#~ plot.cuts = plot.cuts.replace("ht","ht*%f"%(shift,))	
		for index, sample in enumerate(self.samples):

			for name, tree in tree1.iteritems(): 
				if name == sample:
					tempHist = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)		
					tempHist.Scale((lumi*scalefacTree1*self.xsecs[index]/self.nEvents[index]))
					self.histo.Add(tempHist.Clone("%s_%s"%(name,index)))
			if tree2 != "None":		
				for name, tree in tree2.iteritems(): 
					if name == sample:
						tempHist = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
						tempHist.Scale((lumi*self.xsecs[index]*scalefacTree2/self.nEvents[index]))

						self.histo.Add(tempHist.Clone("%s_%s"%(name,index)))
		self.histo.SetFillColor(self.theColor)
		self.histo.SetLineColor(self.theLineColor)
		self.histo.GetXaxis().SetTitle(plot.xaxis) 
		self.histo.GetYaxis().SetTitle(plot.yaxis)	
		#~ plot.cuts = plot.cuts.replace("met*%f"%(shift,),"met")
		#~ plot.cuts = plot.cuts.replace("ht*%f"%(shift,),"ht")				
		return self.histo   
		
		 
class TheStack:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = ROOT.TH1F()	
	theHistogramXsecUp = ROOT.TH1F()
	theHistogramXsecDown = ROOT.TH1F()
	def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0):
		from ROOT import THStack
		self.theStack = THStack()
		self.theHistogram = ROOT.TH1F()
		self.theHistogram.Sumw2()
		self.theHistogramXsecDown = ROOT.TH1F()
		self.theHistogramXsecUp = ROOT.TH1F()
		self.theHistogram = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		self.theHistogramXsecDown = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		self.theHistogramXsecUp = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for process in processes:
			name = process.label
			temphist = TH1F()
			temphist.Sumw2()
			temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2)
			self.theStack.Add(temphist.Clone("%s_unscaled"%(name,)))
			self.theHistogram.Add(temphist.Clone("%s_unscaledHist"%(name,)))
			temphist2 = temphist.Clone("%s_temp1"%(name,))
			temphist2.Scale(1-process.uncertainty)
			self.theHistogramXsecDown.Add(temphist2.Clone("%s_scaledDown"%(name,)))
			temphist3 = temphist.Clone("%s_temp2"%(name,))
			temphist3.Scale(1+process.uncertainty)
			self.theHistogramXsecUp.Add(temphist3.Clone("%s_scaledDown"%(name,)))

class Process:
	samples = []
	xsecs = []
	nEvents = []
	label = ""
	theColor = 0
	theLineColor = 0 
	histo = ROOT.TH1F()
	uncertainty = 0.
	scaleFac = 1.
	
	def __init__(self, samplename=["none"],Counts={"none":-1},labels = "none",color=0,lineColor=0,uncertainty=0.,scaleFac=1.):
		self.samples = []
		self.xsecs = []
		self.nEvents = []
		self.label = labels
		self.theColor = color
		self.theLineColor = lineColor
		self.histo.SetLineColor(lineColor)
		self.histo.SetFillColor(color)
		self.uncertainty = uncertainty
		self.scaleFac = scaleFac
		for sample in samplename:
			self.samples.append(sample)
			
			self.xsecs.append(eval(config.get(sample,"crosssection")))
			self.nEvents.append(Counts[sample])
			#~ print self.nEvents
			
	#~ def createCombinedHistogram(self,lumi,plot,trees):
		#~ self.histo = TH1F("hist","hist",plot.nBins,plot.firstBin,plot.lastBin)
		#~ for index, sample in enumerate(self.samples):
			#~ for name, tree in trees.iteritems(): 
				#~ if name == sample:
					#~ tempHist = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
					#~ tempHist.Scale(lumi*self.xsecs[index]/self.nEvents[index])
					#~ self.histo.Add(tempHist.Clone())
		#~ self.histo.SetFillColor(self.theColor)
		#~ self.histo.SetLineColor(self.theLineColor)
		#~ self.histo.GetXaxis().SetTitle(plot.xaxis) 
		#~ self.histo.GetYaxis().SetTitle(plot.yaxis)			
		#~ return self.histo
		
	def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.):
		self.histo = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		#~ plot.cuts = plot.cuts.replace("met","met*%f"%(shift,))
		#~ plot.cuts = plot.cuts.replace("ht","ht*%f"%(shift,))	
		for index, sample in enumerate(self.samples):
			#~ print scalefacTree1
			#~ print scalefacTree2
			for name, tree in tree1.iteritems(): 
				if name == sample:
					tempHist = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
					#~ print "-------------------"
					#~ print lumi
					#~ print scalefacTree1
					#~ print self.xsecs[index]
					#~ print self.nEvents[index]
					#~ print "-------------------"
					#~ print name 
					#~ print "Scalefac :"
					#~ print (lumi*self.xsecs[index]*scalefacTree1/self.nEvents[index])
					#~ print tempHist.GetEntries()					
					tempHist.Scale((lumi*scalefacTree1*self.xsecs[index]/self.nEvents[index]))
					self.histo.Add(tempHist.Clone())
			if tree2 != "None":		
				for name, tree in tree2.iteritems(): 
					if name == sample:
						tempHist = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
						tempHist.Scale((lumi*self.xsecs[index]*scalefacTree2/self.nEvents[index]))

						self.histo.Add(tempHist.Clone())
		self.histo.SetFillColor(self.theColor)
		self.histo.SetLineColor(self.theLineColor)
		self.histo.GetXaxis().SetTitle(plot.xaxis) 
		self.histo.GetYaxis().SetTitle(plot.yaxis)	
		#~ plot.cuts = plot.cuts.replace("met*%f"%(shift,),"met")
		#~ plot.cuts = plot.cuts.replace("ht*%f"%(shift,),"ht")
		#~ print self.scaleFac
		#~ self.histo.Scale(self.scaleFac)					
		return self.histo

#~ def StackIt(processes,lumi,plot,trees):
	#~ from ROOT import THStack
	#~ theStack = THStack()
	#~ for process in processes:
		#~ temphist = process.createCombinedHistogram(lumi,plot,trees)
		#~ theStack.Add(temphist.Clone())
		#~ print process.label
		#~ 
	#~ return theStack	
class TheStack:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = ROOT.TH1F()	
	theHistogramXsecUp = ROOT.TH1F()
	theHistogramXsecDown = ROOT.TH1F()
	def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0):
		self.theStack = THStack()
		self.theHistogram = ROOT.TH1F()
		self.theHistogram.Sumw2()
		self.theHistogramXsecDown = ROOT.TH1F()
		self.theHistogramXsecUp = ROOT.TH1F()
		self.theHistogram = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		self.theHistogramXsecDown = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		self.theHistogramXsecUp = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		for process in processes:
			temphist = TH1F()
			temphist.Sumw2()
			temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2)
			#~ temphist.Scale(scalefac)
			self.theStack.Add(temphist.Clone())
			self.theHistogram.Add(temphist.Clone())
			temphist2 = temphist.Clone()
			temphist2.Scale(1-process.uncertainty)
			self.theHistogramXsecDown.Add(temphist2.Clone())
			temphist3 = temphist.Clone()
			temphist3.Scale(1+process.uncertainty)
			self.theHistogramXsecUp.Add(temphist3.Clone())
			#~ print process.label
			#~ print process.uncertainty
			#~ print scalefacTree1
			#~ print temphist.Integral(temphist.FindBin(15),temphist.FindBin(70))
		
		
		
#~ def getDataHist(trees,plot):
	#~ histo = TH1F()
	#~ for name, tree in trees.iteritems():
		#~ if name == "MergedData":
			#~ print "hier"
			#~ histo = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
	#~ return histo				
def getDataHist(plot,tree1,tree2="None"):

	histo = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
	for name, tree in tree1.iteritems():
		if "Run2012D" not in name:
			histo.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
	if (tree2 != "None"):
		for name, tree in tree2.iteritems():
			if "Run2012D" not in name:
				histo.Add(createHistoFromTree(tree,plot.variable,plot.cuts,plot.nBins,plot.firstBin,plot.lastBin).Clone())
	
	return histo	
	
class Plot:
	
	variable= "none"
	cuts	= "none"
	xaxis   = "none"
	yaxis	= "none"
	nBins	= 0
	firstBin = 0
	lastBin = 0
	def __init__(self, var="none",cut="none",axislabel="none",yaxislabel="none",bins=0,bin1=0,binlast=0):
		self.variable=var
		self.cuts=cut
		self.xaxis=axislabel
		self.yaxis=yaxislabel
		self.nBins=bins
		self.firstBin=bin1
		self.lastBin=binlast
