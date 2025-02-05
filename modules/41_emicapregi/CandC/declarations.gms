*** |  (C) 2006-2022 Potsdam Institute for Climate Impact Research (PIK)
*** |  authors, and contributors see CITATION.cff file. This file is part
*** |  of REMIND and licensed under AGPL-3.0-or-later. Under Section 7 of
*** |  AGPL-3.0, you are granted additional permissions described in the
*** |  REMIND License Exception, version 1.0 (see LICENSE file).
*** |  Contact: remind@pik-potsdam.de
*** SOF ./modules/41_emicapregi/CandC/declarations.gms

parameter
p41_lambda(tall)                                "share parameter"
p41_shEmi2005(all_regi)                         "emission shares in 2005"
p41_co2eq(ttot,all_regi)                        "emissions from baseline run"
;

equations
q41_perm_alloc_cap(ttot,all_regi)               "emission permit allocation"
;
*** EOF ./modules/41_emicapregi/CandC/declarations.gms
