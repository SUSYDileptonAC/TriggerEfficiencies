MAKEtriggerEff = python triggerEfficiencies.py
MAKEtriggerEffCentralValues = python triggerEfficienciesCentralValues.py
MAKEtriggerEffTables = python makeTriggerEffTables.py

AN_PATH = /home/jan/Doktorarbeit/Dilepton/projects/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots

shelves: 
	mkdir shelves

TriggerEfficiencies: triggerEfficiencies.py shelves
	$(MAKEtriggerEff) Barrel
	$(MAKEtriggerEff) Endcap
	$(MAKEtriggerEff) Inclusive

TriggerEfficienciesCentralValues: triggerEfficienciesCentralValues.py shelves
	$(MAKEtriggerEffCentralValues) Barrel
	$(MAKEtriggerEffCentralValues) Endcap
	$(MAKEtriggerEffCentralValues) Inclusive

TriggerEfficienciesTables: makeTriggerEffTables.py
	$(MAKEtriggerEffTables) Exclusive HT

	
		
		
copyAN:
	cp fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_nJets_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_nVtx_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_pt1_leadingPt30.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_Mll_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_MET_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_Eta1_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_nJets_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_nVtx_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_pt1_leadingPt30.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_Mll_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_MET_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_Eta1_pt2020.pdf $(AN_PLOTS)
	cp tab/table_TriggerEffsExclusive_Inclusive_HT.tex tab/table_TriggerEffsExclusive_Seperated_HT.tex $(AN_TABLES)
	

