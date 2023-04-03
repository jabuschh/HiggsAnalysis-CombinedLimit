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

vars = OrderedDict()
vars["mttbar"] = "semilep_ditop_mass"

bins = [
    "bin1",
    "bin2",
    "bin3",
    "bin4",
    "bin5",
    "bin6",
    "bin7",
    "bin8",
    "bin9",
    "bin10",
    "bin11",
    "bin12",
    "bin13",
    "bin14",
    "bin15"
]

fas = [
    400,
    480,
    560,
    640,
    720,
    800,
    900,
    1000,
    1150,
    1300,
    1500,
    1700,
    2000,
    2300,
    3500
]

# normalization systematics
rates = OrderedDict()
# rates["lumi_13TeV_fullRun2"] = 1.016
# rates["tttosemileptonic_rate"] = 1.1
# rates["alp_ttbar_signal_rate"] = 1.1
# rates["alp_ttbar_interference_rate"] = 1.1


# shape systematics: up/down variations
shapes = OrderedDict()
# shapes["syst"] = ["TTToSemiLeptonic"]


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
    N3 = max([len(var) for var in vars]) + 2
    N4 = max([len(process) for process in processes] + [len(var) for var in vars]) + 2

    for entry in list_inputdirs:

        year = entry[0]
        inputdir = entry[1]
        print(year)

        for bin in bins:

            filename_out = "inputHistograms_" + signal_name + "_" + year + "_" + bin + ".root"
            file_out = ROOT.TFile(filename_out, "RECREATE")
            datacard_name = "datacard_" + signal_name + "_" + year + "_" + bin + ".dat"

            for var in vars:

                bincontent = -1
                binerror = -1
                for process in processes + data:
                    process_prefix = "uhh2.AnalysisModuleRunner."
                    if process == "data_obs":
                        process_prefix += "DATA."
                    else:
                        process_prefix += "MC."
                    filename_in = inputdir + process_prefix + process + ".root"
                    check_file(filename_in)
                    file_in = ROOT.TFile(filename_in)

                    hist_in = file_in.Get(vars[var])
                    bincontent = hist_in.GetBinContent(int(bin[3:]))
                    binerror = hist_in.GetBinError(int(bin[3:]))

                    if process == "ALP_ttbar_interference": # needed to correctly scale ALP interference (-1 moved to PhysicsModel)
                        bincontent *= -1

                    file_out.cd()
                    hist_out = ROOT.TH1F(var + "_" + bin + "_" + process, var + "_" + bin + "_" + process, 1, 0, 1)
                    hist_out.SetBinContent(1, bincontent)
                    hist_out.SetBinError(1, binerror)
                    hist_out.Write(var + "_" + bin + "_" + process)

                    if process == "data_obs": continue

                    with open(datacard_name, 'w') as datacard:
                        datacard.write("# PARAMETERS\n")
                        datacard.write("imax " + str(len(bins)) + " number of bins\n")
                        datacard.write("jmax " + str(len(backgrounds)) + " number of backgrounds\n")
                        datacard.write("kmax 1 number of nuisance parameters\n")
                        # datacard.write("shapes * * " + filename_out + " $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n")
                        datacard.write((N1 + N2 - 2) * "-" + "\n")
                        datacard.write("# vars\n")
                        datacard.write("bin          " + "".join([pad(bin, N3)]) + "\n")
                        datacard.write("observation  " + "".join([pad("-1", N3)]) + "\n")
                        datacard.write((N1 + N2 - 2) * "-" + "\n")
                        datacard.write("# PROCESSES\n")
                        datacard.write(pad("bin", N1 + N2) + "".join([pad(bin, N4) for process in processes]) + "\n")
                        datacard.write(pad("process", N1 + N2) + "".join([pad(process, N4) for process in processes]) + "\n")
                        datacard.write(pad("process", N1 + N2) + ("".join([pad(str(-s), N4) for s in range(len(signals))][::-1] + [pad(str(b+1), N4) for b in range(len(backgrounds))]))+ "\n")
                        datacard.write(pad("rate", N1 + N2) + "".join([pad(bincontent, N4) for process in processes]) + "\n")
                        datacard.write((N1 + N2 - 2) * "-" + "\n")
                        datacard.write("# SYSTEMATICS\n")

                        # add syst as rate uncert (extract form up/down hists)


                        # normalization systematics
                        for rate in rates:
                            datacard.write(pad(rate, N1) + pad("lnN", N2))
                            for var in vars:
                                for process in processes:
                                    if year in rate: # fullRun2 lumi
                                        datacard.write(pad(rates[rate], N4))
                                    elif process.lower() + "_rate" == rate: # cross sections
                                        datacard.write(pad(rates[rate], N4))
                                    else: # other
                                        datacard.write(pad("-", N4))
                            datacard.write("\n")

                        # # shape systematics
                        # for shape in shapes:
                        #     datacard.write(pad(shape, N1) + pad("shape", N2))
                        #     for process in processes:
                        #         if process in shapes[shape]:
                        #             datacard.write(pad("1.0", N4))
                        #         else:
                        #             datacard.write(pad("-", N4))
                        #     datacard.write("\n")

                        # datacard.write((N1 + N2 - 2) * "-" + "\n")
                        # datacard.write("* autoMCStats 0 0 1")

    print("done.")


if __name__ == "__main__":
    createCombineInput()
