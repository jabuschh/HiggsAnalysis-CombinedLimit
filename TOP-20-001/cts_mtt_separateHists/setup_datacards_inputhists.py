#!/usr/bin/env python2

import ROOT
import collections
import os
import shutil
import itertools
from collections import OrderedDict

inputdirs = {
    "fullRun2": "/nfs/dust/cms/user/jabuschh/uhh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/TOP-20-001/output_combine/"
}

signals = [
    "ALP_ttbar_signal",
    "ALP_ttbar_interference",
]

signals_forplotting = [
    "SIB_sqrtmu_minus3",
    "SIB_sqrtmu_minus2",
    "SIB_sqrtmu_minus1",
    "SIB_sqrtmu_plus1",
    "SIB_sqrtmu_plus2",
    "SIB_sqrtmu_plus3",
]

backgrounds = [
    "TTToSemiLeptonic"
]

data = [
    "data_obs"
]

processes = signals + backgrounds

regions = OrderedDict()
regions["bin1"] = "cts_mtt250To420"
regions["bin2"] = "cts_mtt420To520"
regions["bin3"] = "cts_mtt520To620"
regions["bin4"] = "cts_mtt620To800"
regions["bin5"] = "cts_mtt800To1000"
regions["bin6"] = "cts_mtt1000To3500"


# normalization systematics
rates = OrderedDict()
rates["lumi_13TeV_fullRun2"] = 1.016

# shape systematics: up/down variations
shapes = OrderedDict()
shapes["datasyst"] = ["TTToSemiLeptonic"]
shapes["mcscale"]  = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
shapes["pu"]       = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
shapes["pdf"]      = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
shapes["isr"]      = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
shapes["fsr"]      = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]


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

    # characters per column
    N1 = max([len(rate) for rate in rates] + [5]) + 5
    N2 = 8
    N3 = max([len(region) for region in regions]) + 2
    N4 = max([len(process) for process in processes] + [len(region) for region in region]) + 2

    for entry in list_inputdirs:

        year = entry[0]
        inputdir = entry[1]
        print(year)

        for region in regions:

            filename_out = "inputHistograms_" + year + "_" + region + ".root"
            file_out = ROOT.TFile(filename_out, "RECREATE")

            for process in signals + signals_forplotting + backgrounds + data:
                process_prefix = "uhh2.AnalysisModuleRunner."
                if process == "data_obs":
                    process_prefix += "DATA."
                else:
                    process_prefix += "MC."
                filename_in = inputdir + process_prefix + process + ".root"
                check_file(filename_in)
                file_in = ROOT.TFile(filename_in)
                hist_in = file_in.Get(regions[region])

                file_out.cd()
                hist_out = hist_in.Clone()
                hist_out.Write(region + "_" + process)

                if process == "data_obs": continue

                for shape in shapes:
                    if process in shapes[shape]:
                        hist_syst_up_in = file_in.Get(regions[region] + "_" + shape + "_up")
                        hist_syst_down_in = file_in.Get(regions[region] + "_" + shape + "_down")
                        hist_syst_up_out = hist_syst_up_in.Clone()
                        hist_syst_down_out = hist_syst_down_in.Clone()
                        hist_syst_up_out.Write(region + "_" + process + "_" + shape + "Up")
                        hist_syst_down_out.Write(region + "_" + process + "_" + shape + "Down")
                file_in.Close()

            datacard_name = "datacard_" + year + "_" + region + ".dat"
            with open(datacard_name, 'w') as datacard:
                datacard.write("# PARAMETERS\n")
                datacard.write("imax 1 number of regions\n")
                datacard.write("jmax " + str(len(processes) - 1) + " number of processes -1\n")
                datacard.write("kmax *\n")
                datacard.write("shapes * * " + filename_out + " $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# regions\n")
                datacard.write("bin          " + "".join([pad(region, N3)]) + "\n")
                datacard.write("observation  " + "".join([pad("-1", N3)]) + "\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# PROCESSES\n")
                datacard.write(pad("bin", N1 + N2) + "".join([pad(region, N4) for process in processes]) + "\n")
                datacard.write(pad("process", N1 + N2) + "".join([pad(process, N4) for process in processes]) + "\n")
                datacard.write(pad("process", N1 + N2) + ("".join([pad(str(-s), N4) for s in range(len(signals))][::-1] + [pad(str(b+1), N4) for b in range(len(backgrounds))])) + "\n")
                datacard.write(pad("rate", N1 + N2) + "".join([pad("-1", N4) for process in processes]) + "\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# SYSTEMATICS\n")

                # normalization systematics
                for rate in rates:
                    datacard.write(pad(rate, N1) + pad("lnN", N2))
                    for process in processes:
                        if year in rate: # fullRun2 lumi
                            datacard.write(pad(rates[rate], N4))
                        elif process.lower() + "_rate" == rate: # cross sections
                            datacard.write(pad(rates[rate], N4))
                        else: # other
                            datacard.write(pad("-", N4))
                    datacard.write("\n")

                # shape systematics
                for shape in shapes:
                    datacard.write(pad(shape, N1) + pad("shape", N2))
                    for process in processes:
                        if process in shapes[shape]:
                            datacard.write(pad("1.0", N4))
                        else:
                            datacard.write(pad("-", N4))
                    datacard.write("\n")

                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("* autoMCStats 0 0 1")

    print("done.")


if __name__ == "__main__":
    createCombineInput()
