*** |  (C) 2006-2022 Potsdam Institute for Climate Impact Research (PIK)
*** |  authors, and contributors see CITATION.cff file. This file is part
*** |  of REMIND and licensed under AGPL-3.0-or-later. Under Section 7 of
*** |  AGPL-3.0, you are granted additional permissions described in the
*** |  REMIND License Exception, version 1.0 (see LICENSE file).
*** |  Contact: remind@pik-potsdam.de
*** SOF ./modules/35_transport/edge_esm/output.gms

$ifthen.calibrate %CES_parameters% == "load"
  Execute "Rscript -e 'edgeTransport::toolIterativeEDGETransport(reporting=TRUE)'";
$endif.calibrate

*** EOF ./modules/35_transport/edge_esm/output.gms
