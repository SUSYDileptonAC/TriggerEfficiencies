MAKEtriggerEff = python triggerEfficiencies.py
MAKEtriggerEffCentralValues = python triggerEfficienciesCentralValuesMC.py

AN_PATH = /user/schomakers/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots

shelves: 
	mkdir shelves

TriggerEfficiencies: triggerEfficiencies.py shelves
		$(MAKEtriggerEff) Barrel
		$(MAKEtriggerEff) Endcap
		$(MAKEtriggerEff) Inclusive

TriggerEfficienciesCentralValues: triggerEfficienciesCentralValuesMC.py shelves
		$(MAKEtriggerEffCentralValues) Barrel
		$(MAKEtriggerEffCentralValues) Endcap
		$(MAKEtriggerEffCentralValues) Inclusive
		
		
copyAN:
	cp fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_nJets_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_nVtx_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_pt1_leadingPt30.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_Mll_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_MET_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Barrel_HighHT_Run92_Eta1_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_nJets_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_nVtx_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_pt1_leadingPt30.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_Mll_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_MET_pt2020.pdf fig/Triggereff_SFvsOF_Syst_AlphaT_Endcap_HighHT_Run92_Eta1_pt2020.pdf  $(AN_PLOTS)
	

