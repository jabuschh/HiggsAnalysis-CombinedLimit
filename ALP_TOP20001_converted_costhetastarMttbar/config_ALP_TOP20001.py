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

# fas = [
#     420,
#     520,
#     620,
#     800,
#     1000,
#     3500
# ]

# normalization systematics
rates = OrderedDict()
# rates["lumi_13TeV_fullRun2"] = 1.016
# rates["tttosemileptonic_rate"] = 1.1
# rates["alp_ttbar_signal_rate"] = 1.1
# rates["alp_ttbar_interference_rate"] = 1.1


# shape systematics: up/down variations
shapes = OrderedDict()
shapes["syst"] = ["TTToSemiLeptonic"]




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
    N1 = max([len(rate) for rate in rates] + [1]) + 5
    N2 = 8
    N3 = max([len(region) for region in regions]) + 2
    N4 = max([len(process) for process in processes] + [len(region) for region in region]) + 2

    for entry in list_inputdirs:

        year = entry[0]
        inputdir = entry[1]
        print(year)

        for region in regions:

            filename_out = "inputHistograms_" + signal_name + "_" + year + "_" + region + ".root"
            file_out = ROOT.TFile(filename_out, "RECREATE")

            for process in processes + data:
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
                if process == "ALP_ttbar_interference": # needed to correctly scale ALP interference (-1 moved to PhysicsModel)
                    hist_out.Scale(-1)
                hist_out.Write(region + "_" + process)

                if process == "data_obs": continue

                for shape in shapes:
                    if process in shapes[shape]:
                        hist_syst_up_in = file_in.Get(regions[region] + "_" + shape + "Up")
                        hist_syst_down_in = file_in.Get(regions[region] + "_" + shape + "Down")
                        hist_syst_up_out = hist_syst_up_in.Clone()
                        hist_syst_down_out = hist_syst_down_in.Clone()
                        if process == "ALP_ttbar_interference":
                            hist_syst_up_out.Scale(-1)
                            hist_syst_down_out.Scale(-1)
                        hist_syst_up_out.Write(region + "_" + process + "_" + shape + "Up")
                        hist_syst_down_out.Write(region + "_" + process + "_" + shape + "Down")
                file_in.Close()



            datacard_name = "datacard_" + signal_name + "_" + year + "_" + region + ".dat"
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
