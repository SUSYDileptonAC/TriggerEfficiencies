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

	dataPkls = loadPickles("shelves/triggerEff_HighHTExclusive_PFHT_Full2012.pkl")
	dataBarrelPkls = loadPickles("shelves/triggerEff_HighHTExclusiveCentral_PFHT_Full2012.pkl")
	dataEndcapPkls = loadPickles("shelves/triggerEff_HighHTExclusiveForward_PFHT_Full2012.pkl")
	mcPkls = loadPickles("shelves/triggerEff_HighHTExclusive_PFHT_Full2012_MC.pkl")
	mcBarrelPkls = loadPickles("shelves/triggerEff_HighHTExclusiveCentral_PFHT_Full2012_MC.pkl")
	mcEndcapPkls = loadPickles("shelves/triggerEff_HighHTExclusiveForward_PFHT_Full2012_MC.pkl")


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

\hline
& \multicolumn{3}{c}{MC, $|\eta|<2.4$ } \\
\hline

%s    
    \hline 
"""
	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f \\"+"\n"


	tableMC =""
	tableData =""
	run = "Full2012"
	
	tableData += lineTemplate%("ee",dataPkls[run]["EE"]["Nominator"],dataPkls[run]["EE"]["Denominator"],dataPkls[run]["EE"]["Efficiency"],max(dataPkls[run]["EE"]["UncertaintyUp"],dataPkls[run]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",dataPkls[run]["MuMu"]["Nominator"],dataPkls[run]["MuMu"]["Denominator"],dataPkls[run]["MuMu"]["Efficiency"],max(dataPkls[run]["MuMu"]["UncertaintyUp"],dataPkls[run]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",dataPkls[run]["EMu"]["Nominator"],dataPkls[run]["EMu"]["Denominator"],dataPkls[run]["EMu"]["Efficiency"],max(dataPkls[run]["EMu"]["UncertaintyUp"],dataPkls[run]["EMu"]["UncertaintyDown"]))



	tableMC += lineTemplate%("ee",mcPkls[run]["EE"]["Nominator"],mcPkls[run]["EE"]["Denominator"],mcPkls[run]["EE"]["Efficiency"],max(mcPkls[run]["EE"]["UncertaintyUp"],mcPkls[run]["EE"]["UncertaintyDown"]))	
	tableMC += lineTemplate%("$\mu\mu$",mcPkls[run]["MuMu"]["Nominator"],mcPkls[run]["MuMu"]["Denominator"],mcPkls[run]["MuMu"]["Efficiency"],max(mcPkls[run]["MuMu"]["UncertaintyUp"],mcPkls[run]["MuMu"]["UncertaintyDown"]))	
	tableMC += lineTemplate%("e$\mu$",mcPkls[run]["EMu"]["Nominator"],mcPkls[run]["EMu"]["Denominator"],mcPkls[run]["EMu"]["Efficiency"],max(mcPkls[run]["EMu"]["UncertaintyUp"],mcPkls[run]["EMu"]["UncertaintyDown"]))	


		
	saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Inclusive")


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

& \multicolumn{6}{c}{MC} \\
\hline
&  \multicolumn{3}{c|}{$|\eta|<1.4$ } & \multicolumn{3}{|c}{ at least 1 $|\eta| > 1.6$ } \\
\hline 
%s    
    \hline 
	
"""
	lineTemplate = r"%s & %d & %d & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f \\"+"\n"
	tableMC =""
	tableData =""
	run = "Full2012"

	tableData += lineTemplate%("ee",dataBarrelPkls[run]["EE"]["Nominator"],dataBarrelPkls[run]["EE"]["Denominator"],dataBarrelPkls[run]["EE"]["Efficiency"],max(dataBarrelPkls[run]["EE"]["UncertaintyUp"],dataBarrelPkls[run]["EE"]["UncertaintyDown"]),dataEndcapPkls[run]["EE"]["Nominator"],dataEndcapPkls[run]["EE"]["Denominator"],dataEndcapPkls[run]["EE"]["Efficiency"],max(dataEndcapPkls[run]["EE"]["UncertaintyUp"],dataEndcapPkls[run]["EE"]["UncertaintyDown"]))	
	tableData += lineTemplate%("$\mu\mu$",dataBarrelPkls[run]["MuMu"]["Nominator"],dataBarrelPkls[run]["MuMu"]["Denominator"],dataBarrelPkls[run]["MuMu"]["Efficiency"],max(dataBarrelPkls[run]["MuMu"]["UncertaintyUp"],dataBarrelPkls[run]["MuMu"]["UncertaintyDown"]),dataEndcapPkls[run]["MuMu"]["Nominator"],dataEndcapPkls[run]["MuMu"]["Denominator"],dataEndcapPkls[run]["MuMu"]["Efficiency"],max(dataEndcapPkls[run]["MuMu"]["UncertaintyUp"],dataEndcapPkls[run]["MuMu"]["UncertaintyDown"]))	
	tableData += lineTemplate%("e$\mu$",dataBarrelPkls[run]["EMu"]["Nominator"],dataBarrelPkls[run]["EMu"]["Denominator"],dataBarrelPkls[run]["EMu"]["Efficiency"],max(dataBarrelPkls[run]["EMu"]["UncertaintyUp"],dataBarrelPkls[run]["EMu"]["UncertaintyDown"]),dataEndcapPkls[run]["EMu"]["Nominator"],dataEndcapPkls[run]["EMu"]["Denominator"],dataEndcapPkls[run]["EMu"]["Efficiency"],max(dataEndcapPkls[run]["EMu"]["UncertaintyUp"],dataEndcapPkls[run]["EMu"]["UncertaintyDown"]))


	tableMC += lineTemplate%("ee",mcBarrelPkls[run]["EE"]["Nominator"],mcBarrelPkls[run]["EE"]["Denominator"],mcBarrelPkls[run]["EE"]["Efficiency"],max(mcBarrelPkls[run]["EE"]["UncertaintyUp"],mcBarrelPkls[run]["EE"]["UncertaintyDown"]),mcEndcapPkls[run]["EE"]["Nominator"],mcEndcapPkls[run]["EE"]["Denominator"],mcEndcapPkls[run]["EE"]["Efficiency"],max(mcEndcapPkls[run]["EE"]["UncertaintyUp"],mcEndcapPkls[run]["EE"]["UncertaintyDown"]))	
	tableMC += lineTemplate%("$\mu\mu$",mcBarrelPkls[run]["MuMu"]["Nominator"],mcBarrelPkls[run]["MuMu"]["Denominator"],mcBarrelPkls[run]["MuMu"]["Efficiency"],max(mcBarrelPkls[run]["MuMu"]["UncertaintyUp"],mcBarrelPkls[run]["MuMu"]["UncertaintyDown"]),mcEndcapPkls[run]["MuMu"]["Nominator"],mcEndcapPkls[run]["MuMu"]["Denominator"],mcEndcapPkls[run]["MuMu"]["Efficiency"],max(mcEndcapPkls[run]["MuMu"]["UncertaintyUp"],mcEndcapPkls[run]["MuMu"]["UncertaintyDown"]))	
	tableMC += lineTemplate%("e$\mu$",mcBarrelPkls[run]["EMu"]["Nominator"],mcBarrelPkls[run]["EMu"]["Denominator"],mcBarrelPkls[run]["EMu"]["Efficiency"],max(mcBarrelPkls[run]["EMu"]["UncertaintyUp"],mcBarrelPkls[run]["EMu"]["UncertaintyDown"]),mcEndcapPkls[run]["EMu"]["Nominator"],mcEndcapPkls[run]["EMu"]["Denominator"],mcEndcapPkls[run]["EMu"]["Efficiency"],max(mcEndcapPkls[run]["EMu"]["UncertaintyUp"],mcEndcapPkls[run]["EMu"]["UncertaintyDown"]))	


	saveTable(tableTemplate%(tableData,tableMC), "TriggerEffsExclusive_Seperated")



main()
