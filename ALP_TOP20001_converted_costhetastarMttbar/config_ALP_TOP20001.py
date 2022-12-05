#!/usr/bin/env python2

import ROOT
import collections
import os
import shutil
import itertools
from collections import OrderedDict

inputdirs = {
    "fullRun2": "/nfs/dust/cms/user/jabuschh/ZprimeSemiLeptonic/RunII_106X_v2/fullRun2/TOP-20-001/forCombine_converted/"
}

# inputbasedir_pdf = "/nfs/dust/cms/user/jabuschh/uhh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/uncertainties/hists_pdf/"
# inputbasedir_mcscale = "/nfs/dust/cms/user/jabuschh/uhh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/uncertainties/hists_mcscale/"

signal_name = "ALP"

signals = [
    "ALP_ttbar_signal",
    "ALP_ttbar_interference",
]

backgrounds = [
    "TTToSemiLeptonic"
]

data = [
    "data_obs"
]

processes = signals + backgrounds

regions = OrderedDict()
regions["bin1"] = "TOP20001_cosThetastar_top_ttframe_bin1"
regions["bin2"] = "TOP20001_cosThetastar_top_ttframe_bin2"
regions["bin3"] = "TOP20001_cosThetastar_top_ttframe_bin3"
regions["bin4"] = "TOP20001_cosThetastar_top_ttframe_bin4"
regions["bin5"] = "TOP20001_cosThetastar_top_ttframe_bin5"
regions["bin6"] = "TOP20001_cosThetastar_top_ttframe_bin6"

fas = [
    420,
    520,
    620,
    800,
    1000,
    3500
]

# normalization systematics
rates = OrderedDict()
rates["lumi_13TeV_fullRun2"] = 1.016
rates["tttosemileptonic_rate"] = 1.1
rates["alp_ttbar_signal_rate"] = 1.1
rates["alp_ttbar_interference_rate"] = 1.1


# shape systematics: up/down variations
# shapes = OrderedDict()
# shapes["pdf"] = ["TTbar","ST","WJets","others","ALP_ttbar_signal","ALP_ttbar_interference"] # pdf uncertainty
# shapes["mcscale"] = ["TTbar","ST","WJets","others","ALP_ttbar_signal","ALP_ttbar_interference"] # mcscale uncertainty: envelope of muR and muF up/down combinations
# shapes["pu"] = ["TTbar","ST","WJets","others","ALP_ttbar_signal","ALP_ttbar_interference"] # pileup
# shapes["isr"] = ["TTbar","ST","WJets","others","ALP_ttbar_signal","ALP_ttbar_interference"] # initial state radiation
# shapes["fsr"] = ["TTbar","ST","WJets","others","ALP_ttbar_signal","ALP_ttbar_interference"] # final state radiation
# TODO: add JEC + JER





def nested_dict_iter(nested):
    for key, value in nested.iteritems():
        if isinstance(value, collections.Mapping):
            for inner_key, inner_value in nested_dict_iter(value):
                yield key, inner_key, inner_value
        else:
            yield key, value

def check_file(file_path):
    if not os.path.isfile(file_path):
        raise ValueError("file does not exist: " + str(file_path))

def pad(s, n_pad):
    s = str(s)
    n_pad = n_pad - len(s)
    return s + n_pad * " "


def createCombineInput():
    print("starting...")
    list_inputdirs = list(nested_dict_iter(inputdirs))

    for entry in list_inputdirs:

        year = entry[0]
        inputdir = entry[1]
        print(year)

        bins = []
        for fa, region in itertools.izip(fas, regions):
            filename_out = "inputHistograms_" + signal_name + "_" + year + "_fa" + str(fa) + ".root"
            file_out = ROOT.TFile(filename_out, "RECREATE")

            # the steps in fa correspond to the m(tt) bins considered: 420 GeV (bin 1), 520 GeV (bin 1+2), ..., 3500 GeV (all 6 bins)
            bins.extend([regions[region]])

            for process in processes + data:
                process_prefix = "uhh2.AnalysisModuleRunner."
                if process == "data_obs":
                    process_prefix += "DATA."
                else:
                    process_prefix += "MC."
                filename_in = inputdir + process_prefix + process + ".root"
                check_file(filename_in)
                file_in = ROOT.TFile(filename_in)

                for bin in bins:
                    hist_in = file_in.Get(bin)
                    file_out.cd()
                    hist_out = hist_in.Clone()
                    if process == "ALP_ttbar_interference": # needed to correctly scale ALP interference (-1 moved to PhysicsModel)
                        hist_out.Scale(-1)
                    hist_out.Write(bin[-4:] + "_" + process)


                    # if process == "data_obs": continue

                    # for shape in shapes:
                    #     if str(channel) == "muon" and shape.startswith("ele_"): continue
                    #     if str(channel) == "electron" and shape.startswith("mu_"): continue
                    #     if process in shapes[shape]:
                    #         if shape == "pdf":
                    #             hist_syst_up_in = file_in_pdf.Get(regions[region] + "/" + var + "_" + shape + "_up")
                    #             hist_syst_down_in = file_in_pdf.Get(regions[region] + "/" + var + "_" + shape + "_down")
                    #         elif shape == "mcscale":
                    #             hist_syst_up_in = file_in_mcscale.Get(regions[region] + "/" + var + "_" + shape + "_up")
                    #             hist_syst_down_in = file_in_mcscale.Get(regions[region] + "/" + var + "_" + shape + "_down")
                    #         else:
                    #             hist_syst_up_in = file_in.Get(regions[region] + "/" + var + "_" + shape + "_up")
                    #             hist_syst_down_in = file_in.Get(regions[region] + "/" + var + "_" + shape + "_down")
                    #         hist_syst_up_out = hist_syst_up_in.Clone()
                    #         hist_syst_down_out = hist_syst_down_in.Clone()
                    #         if process == "ALP_ttbar_interference":
                    #             hist_syst_up_out.Scale(-1)
                    #             hist_syst_down_out.Scale(-1)
                    #         hist_syst_up_out.Write(region + "_" + process + "_" + shape + "Up")
                    #         hist_syst_down_out.Write(region + "_" + process + "_" + shape + "Down")
                    # file_in.Close()

            # characters per column
            N1 = max([len(rate) for rate in rates] + [1]) + 2
            N2 = 8
            N3 = max([len(bin[-4:]) for bin in bins]) + 2
            N4 = max([len(process) for process in processes] + [len(bin[-4:]) for bin in bins]) + 2

            datacard_name = "datacard_" + signal_name + "_" + year + "_fa" + str(fa) + ".dat"
            with open(datacard_name, 'w') as datacard:
                datacard.write("# PARAMETERS\n")
                datacard.write("imax " + str(len(bins)) + " number of regions\n")
                datacard.write("jmax " + str(len(processes) - 1) + " number of processes -1\n")
                datacard.write("kmax *\n")
                datacard.write("shapes * * " + filename_out + " $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# regions\n")
                datacard.write("bin          " + "".join([pad(bin[-4:], N3) for bin in bins]) + "\n")
                datacard.write("observation  " + "".join([pad("-1", N3) for bin in bins]) + "\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# PROCESSES\n")
                datacard.write(pad("bin", N1 + N2) + "".join([pad(bin[-4:], N4) for bin in bins for process in processes]) + "\n")
                datacard.write(pad("process", N1 + N2) + "".join([pad(process, N4) for bin in bins for process in processes]) + "\n")
                datacard.write(pad("process", N1 + N2) + ("".join([pad(str(-s), N4) for s in range(len(signals))][::-1] + [pad(str(b+1), N4) for b in range(len(backgrounds))])) * len(bins) + "\n")
                datacard.write(pad("rate", N1 + N2) + "".join([pad("-1", N4) for bin in bins for process in processes]) + "\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# SYSTEMATICS\n")

                # normalization systematics
                for rate in rates:
                    datacard.write(pad(rate, N1) + pad("lnN", N2))
                    for bin in bins:
                        for process in processes:
                            if year in rate: # fullRun2 lumi
                                datacard.write(pad(rates[rate], N4))
                            elif process.lower() + "_rate" == rate: # cross sections
                                datacard.write(pad(rates[rate], N4))
                            else: # other
                                datacard.write(pad("-", N4))
                    datacard.write("\n")

                # shape systematics
                # for shape in shapes:
                #     if str(channel) == "muon" and shape.startswith("ele_"): continue
                #     if str(channel) == "electron" and shape.startswith("mu_"): continue
                #     datacard.write(pad(shape, N1) + pad("shape", N2))
                #     for process in processes:
                #         if process in shapes[shape]:
                #             datacard.write(pad("1.0", N4))
                #         else:
                #             datacard.write(pad("-", N4))
                #     datacard.write("\n")
                #
                # datacard.write((N1 + N2 - 2) * "-" + "\n")
                # datacard.write("* autoMCStats 0 0 1")

    print("done.")


if __name__ == "__main__":
    createCombineInput()
