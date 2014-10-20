#!/usr/bin/env python



def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

	#~ print table
	
def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result

				  


def main():
	from sys import argv
	#~ allPkls = loadPickles("shelves/*.pkl")
	if argv[1] == "Exclusive":
#	dataPkls = loadPickles("shelves/triggerEff_Inclusive_%s_Run2012A+B+C.pkl"%argv[1])
#	dataBarrelPkls = loadPickles("shelves/triggerEff_Barrel_%s_Run2012A+B+C.pkl"%argv[1])
#	dataEndcapPkls = loadPickles("shelves/triggerEff_Endcap_%s_Run2012A+B+C.pkl"%argv[1])
		dataPkls = loadPickles("shelves/triggerEffExclusive_Inclusive_%s_Full2012.pkl"%argv[2])
		dataBarrelPkls = loadPickles("shelves/triggerEffExclusive_Barrel_%s_Full2012.pkl"%argv[2])
		dataEndcapPkls = loadPickles("shelves/triggerEffExclusive_Endcap_%s_Full2012.pkl"%argv[2])
		mcPkls = loadPickles("../MC/shelves/triggerEffExclusive_Inclusive_%s_Simulation.pkl"%argv[2])
		mcBarrelPkls = loadPickles("../MC/shelves/triggerEffExclusive_Barrel_%s_Simulation.pkl"%argv[2])
		mcEndcapPkls = loadPickles("../MC/shelves/triggerEffExclusive_Endcap_%s_Simulation.pkl"%argv[2])
	else:
		dataPkls = loadPickles("shelves/triggerEff_Inclusive_%s_Full2012.pkl"%argv[1])
		dataBarrelPkls = loadPickles("shelves/triggerEff_Barrel_%s_Full2012.pkl"%argv[1])
		dataEndcapPkls = loadPickles("shelves/triggerEff_Endcap_%s_Full2012.pkl"%argv[1])
		mcPkls = loadPickles("../MC/shelves/triggerEff_Inclusive_%s_Simulation.pkl"%argv[1])
		mcBarrelPkls = loadPickles("../MC/shelves/triggerEff_Barrel_%s_Simulation.pkl"%argv[1])
		mcEndcapPkls = loadPickles("../MC/shelves/triggerEff_Endcap_%s_Simulation.pkl"%argv[1])

	#~ print dataPkls
	
# Table for Inclusive

	tableTemplate =r"""
\begin{table}[hbp] \caption{Triggerefficiency-values for data and MC with OS, $p_T>20(20)\,\GeV$ and $H_T>200\,\GeV$ for the inclusive region.} 
\centering 
\renewcommand{\arraystretch}{1.2} 
\begin{tabular}{l|c|c|c}     

 & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ \\    

&\multicolumn{3}{c}{Data,$|\eta|<2.4$} \\
\hline
%s 
 
\end{tabular}  
\label{tab:EffValues_Inclusive}
\end{table}
"""
#\hline
#& \multicolumn{3}{c}{MC, $|\eta|<2.4$ } \\
#\hline

#%s    
    #\hline 

	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f \\"+"\n"


	tableMC =""
	tableData =""
	name = "default"
	run = "Full2012"

	tableData += lineTemplate%("ee",dataPkls[run][name]["EE"]["Nominator"],dataPkls[run][name]["EE"]["Denominator"],dataPkls[run][name]["EE"]["Efficiency"],max(dataPkls[run][name]["EE"]["UncertaintyUp"],dataPkls[run][name]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",dataPkls[run][name]["MuMu"]["Nominator"],dataPkls[run][name]["MuMu"]["Denominator"],dataPkls[run][name]["MuMu"]["Efficiency"],max(dataPkls[run][name]["MuMu"]["UncertaintyUp"],dataPkls[run][name]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",dataPkls[run][name]["EMu"]["Nominator"],dataPkls[run][name]["EMu"]["Denominator"],dataPkls[run][name]["EMu"]["Efficiency"],max(dataPkls[run][name]["EMu"]["UncertaintyUp"],dataPkls[run][name]["EMu"]["UncertaintyDown"]))

	#run = "Simulation"

	#tableMC += lineTemplate%("ee",mcPkls[run][name]["EE"]["Nominator"],mcPkls[run][name]["EE"]["Denominator"],mcPkls[run][name]["EE"]["Efficiency"],max(mcPkls[run][name]["EE"]["UncertaintyUp"],mcPkls[run][name]["EE"]["UncertaintyDown"]))	
	#tableMC += lineTemplate%("$\mu\mu$",mcPkls[run][name]["MuMu"]["Nominator"],mcPkls[run][name]["MuMu"]["Denominator"],mcPkls[run][name]["MuMu"]["Efficiency"],max(mcPkls[run][name]["MuMu"]["UncertaintyUp"],mcPkls[run][name]["MuMu"]["UncertaintyDown"]))	
	#tableMC += lineTemplate%("e$\mu$",mcPkls[run][name]["EMu"]["Nominator"],mcPkls[run][name]["EMu"]["Denominator"],mcPkls[run][name]["EMu"]["Efficiency"],max(mcPkls[run][name]["EMu"]["UncertaintyUp"],mcPkls[run][name]["EMu"]["UncertaintyDown"]))	

	if argv[1] == "Exclusive":
		
		saveTable(tableTemplate%(tableData), "TriggerEffsExclusive_Inclusive_%s"%argv[2])
	else:	
		saveTable(tableTemplate%(tableData), "TriggerEffs_Inclusive_%s"%argv[1])

# Table with Barrel and Endcap seperated


	tableTemplate =r"""
\begin{table}[hbp] \caption{Triggerefficiency-values for data and MC with OS, $p_T>20(20)\,\GeV$ and $H_T>200\,\GeV$ for central and forward region seperated.} 
\centering 
\renewcommand{\arraystretch}{1.2} 
\begin{tabular}{l|c|c|c|c|c|c}     

 & nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$ &  nominator & denominator & $\epsilon_{trigger} \pm \sigma_{stat}$  \\    
\hline

&\multicolumn{6}{c}{Data} \\
\hline
&  \multicolumn{3}{c|}{$|\eta|<1.4$ } & \multicolumn{3}{|c}{ at least 1 $|\eta| > 1.6$ }\\
\hline
%s 
 
\end{tabular}  
\label{tab:EffValues_Seperated}
\end{table}
"""
#& \multicolumn{6}{c}{MC} \\
#\hline
#&  \multicolumn{3}{c|}{$|\eta|<1.4$ } & \multicolumn{3}{|c}{ at least 1 $|\eta| > 1.6$ } \\
#\hline 
#%s    
    #\hline 
	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f \\"+"\n"


	tableMC =""
	tableData =""
	name = "default"
	run = "Full2012"

	tableData += lineTemplate%("ee",dataBarrelPkls[run][name]["EE"]["Nominator"],dataBarrelPkls[run][name]["EE"]["Denominator"],dataBarrelPkls[run][name]["EE"]["Efficiency"],max(dataBarrelPkls[run][name]["EE"]["UncertaintyUp"],dataBarrelPkls[run][name]["EE"]["UncertaintyDown"]),dataEndcapPkls[run][name]["EE"]["Nominator"],dataEndcapPkls[run][name]["EE"]["Denominator"],dataEndcapPkls[run][name]["EE"]["Efficiency"],max(dataEndcapPkls[run][name]["EE"]["UncertaintyUp"],dataEndcapPkls[run][name]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",dataBarrelPkls[run][name]["MuMu"]["Nominator"],dataBarrelPkls[run][name]["MuMu"]["Denominator"],dataBarrelPkls[run][name]["MuMu"]["Efficiency"],max(dataBarrelPkls[run][name]["MuMu"]["UncertaintyUp"],dataBarrelPkls[run][name]["MuMu"]["UncertaintyDown"]),dataEndcapPkls[run][name]["MuMu"]["Nominator"],dataEndcapPkls[run][name]["MuMu"]["Denominator"],dataEndcapPkls[run][name]["MuMu"]["Efficiency"],max(dataEndcapPkls[run][name]["MuMu"]["UncertaintyUp"],dataEndcapPkls[run][name]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",dataBarrelPkls[run][name]["EMu"]["Nominator"],dataBarrelPkls[run][name]["EMu"]["Denominator"],dataBarrelPkls[run][name]["EMu"]["Efficiency"],max(dataBarrelPkls[run][name]["EMu"]["UncertaintyUp"],dataBarrelPkls[run][name]["EMu"]["UncertaintyDown"]),dataEndcapPkls[run][name]["EMu"]["Nominator"],dataEndcapPkls[run][name]["EMu"]["Denominator"],dataEndcapPkls[run][name]["EMu"]["Efficiency"],max(dataEndcapPkls[run][name]["EMu"]["UncertaintyUp"],dataEndcapPkls[run][name]["EMu"]["UncertaintyDown"]))
	
	#run = "Simulation"

	#tableMC += lineTemplate%("ee",mcBarrelPkls[run][name]["EE"]["Nominator"],mcBarrelPkls[run][name]["EE"]["Denominator"],mcBarrelPkls[run][name]["EE"]["Efficiency"],max(mcBarrelPkls[run][name]["EE"]["UncertaintyUp"],mcBarrelPkls[run][name]["EE"]["UncertaintyDown"]),mcEndcapPkls[run][name]["EE"]["Nominator"],mcEndcapPkls[run][name]["EE"]["Denominator"],mcEndcapPkls[run][name]["EE"]["Efficiency"],max(mcEndcapPkls[run][name]["EE"]["UncertaintyUp"],mcEndcapPkls[run][name]["EE"]["UncertaintyDown"]))	
	#tableMC += lineTemplate%("$\mu\mu$",mcBarrelPkls[run][name]["MuMu"]["Nominator"],mcBarrelPkls[run][name]["MuMu"]["Denominator"],mcBarrelPkls[run][name]["MuMu"]["Efficiency"],max(mcBarrelPkls[run][name]["MuMu"]["UncertaintyUp"],mcBarrelPkls[run][name]["MuMu"]["UncertaintyDown"]),mcEndcapPkls[run][name]["MuMu"]["Nominator"],mcEndcapPkls[run][name]["MuMu"]["Denominator"],mcEndcapPkls[run][name]["MuMu"]["Efficiency"],max(mcEndcapPkls[run][name]["MuMu"]["UncertaintyUp"],mcEndcapPkls[run][name]["MuMu"]["UncertaintyDown"]))	
	#tableMC += lineTemplate%("e$\mu$",mcBarrelPkls[run][name]["EMu"]["Nominator"],mcBarrelPkls[run][name]["EMu"]["Denominator"],mcBarrelPkls[run][name]["EMu"]["Efficiency"],max(mcBarrelPkls[run][name]["EMu"]["UncertaintyUp"],mcBarrelPkls[run][name]["EMu"]["UncertaintyDown"]),mcEndcapPkls[run][name]["EMu"]["Nominator"],mcEndcapPkls[run][name]["EMu"]["Denominator"],mcEndcapPkls[run][name]["EMu"]["Efficiency"],max(mcEndcapPkls[run][name]["EMu"]["UncertaintyUp"],mcEndcapPkls[run][name]["EMu"]["UncertaintyDown"]))	

	if argv[1] == "Exclusive":	
		saveTable(tableTemplate%(tableData), "TriggerEffsExclusive_Seperated_%s"%argv[2])
	else:	
		saveTable(tableTemplate%(tableData), "TriggerEffs_Seperated_%s"%argv[1])


main()
