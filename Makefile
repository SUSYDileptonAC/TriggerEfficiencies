
tables: 
	python makeTriggerEffTables.py
remakeTables:
	python triggerEfficiencies.py -c -s HighHTExclusive -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -c -s HighHTExclusiveCentral -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -c -s HighHTExclusiveForward -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -c -s HighHTExclusive 
	python triggerEfficiencies.py -c -s HighHTExclusiveCentral 
	python triggerEfficiencies.py -c -s HighHTExclusiveForward 
	python makeTriggerEffTables.py

centralValues: 
	python triggerEfficiencies.py -c -s HighHTExclusive -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -c -s HighHTExclusiveCentral -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -c -s HighHTExclusiveForward -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -c -s HighHTExclusive 
	python triggerEfficiencies.py -c -s HighHTExclusiveCentral 
	python triggerEfficiencies.py -c -s HighHTExclusiveForward 

dependencies: 
	python triggerEfficiencies.py -d -s HighHTExclusive -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -d -s HighHTExclusiveCentral -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -d -s HighHTExclusiveForward -m -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -d -s HighHTExclusive 
	python triggerEfficiencies.py -d -s HighHTExclusiveCentral 
	python triggerEfficiencies.py -d -s HighHTExclusiveForward 

fitBias: 
	python triggerEfficiencies.py -z -s HighHTExclusive -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -z -s HighHTExclusiveCentral -b TTJets_SpinCorrelations
	python triggerEfficiencies.py -z -s HighHTExclusiveForward -b TTJets_SpinCorrelations

singleLepton:
	python triggerEfficiencies.py -t -s HighHTExclusive 
	python triggerEfficiencies.py -t -s HighHTExclusiveCentral 
	python triggerEfficiencies.py -t -s HighHTExclusiveForward
		

