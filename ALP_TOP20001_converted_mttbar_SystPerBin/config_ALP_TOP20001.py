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

# normalization systematics
rates = OrderedDict()
# rates["lumi_13TeV_fullRun2"] = 1.016
# rates["tttosemileptonic_rate"] = 1.1
# rates["alp_ttbar_signal_rate"] = 1.1
# rates["alp_ttbar_interference_rate"] = 1.1


# shape systematics: up/down variations
shapes = OrderedDict()
shapes["syst"] = ["TTToSemiLeptonic"]
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

        for bin in bins:

            filename_out = "inputHistograms_" + signal_name + "_" + year + "_" + bin + ".root"
            file_out = ROOT.TFile(filename_out, "RECREATE")

            for var in vars:
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
                    file_out.cd()
                    hist_out = hist_in.Clone()

                    if process == "ALP_ttbar_interference": # needed to correctly scale ALP interference (-1 moved to PhysicsModel)
                        hist_out.Scale(-1)

                    Nbins = hist_out.GetNbinsX() + 2 # add underflow and overflow bin
                    for b in range(Nbins):
                        # print(b)
                        # print(bin[3:])
                        # print(hist_out.GetBinContent(b))
                        # print(hist_out.GetBinContent(int(bin[3:])))
                        if b != int(bin[3:]):
                            hist_out.SetBinContent(b, 0.)
                            hist_out.SetBinError(b, 0.) # needed for combine to ignore this bin
                    hist_out.Write(bin + "_" + process)

                    if process == "data_obs": continue

                    for shape in shapes:
                        if process in shapes[shape]:
                            hist_syst_up_in = file_in.Get(vars[var] + "_" + shape + "Up")
                            hist_syst_down_in = file_in.Get(vars[var] + "_" + shape + "Down")
                            hist_syst_up_out = hist_syst_up_in.Clone()
                            hist_syst_down_out = hist_syst_down_in.Clone()
                            if process == "ALP_ttbar_interference":
                                hist_syst_up_out.Scale(-1)
                                hist_syst_down_out.Scale(-1)

                            for b in range(Nbins):
                                if b != int(bin[3:]):
                                    hist_syst_up_out.SetBinContent(b, 0.)
                                    hist_syst_up_out.SetBinError(b, 0.) # needed for combine to ignore this bin
                                    hist_syst_down_out.SetBinContent(b, 0.)
                                    hist_syst_down_out.SetBinError(b, 0.) # needed for combine to ignore this bin

                            hist_syst_up_out.Write(bin + "_" + process + "_" + shape + "Up")
                            hist_syst_down_out.Write(bin + "_" + process + "_" + shape + "Down")
                    file_in.Close()

                # characters per column
                N1 = max([len(rate) for rate in rates] + [1]) + 5
                N2 = 8
                N3 = max([len(var) for var in vars]) + 2
                N4 = max([len(process) for process in processes] + [len(var) for var in vars]) + 2

                datacard_name = "datacard_" + signal_name + "_" + year + "_" + bin + ".dat"
                with open(datacard_name, 'w') as datacard:
                    datacard.write("# PARAMETERS\n")
                    datacard.write("imax 1 number of bins\n")
                    datacard.write("jmax " + str(len(processes) - 1) + " number of processes -1\n")
                    datacard.write("kmax *\n")
                    datacard.write("shapes * * " + filename_out + " $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n")
                    datacard.write((N1 + N2 - 2) * "-" + "\n")
                    datacard.write("# vars\n")
                    datacard.write("bin          " + "".join([pad(bin, N3)]) + "\n")
                    datacard.write("observation  " + "".join([pad("-1", N3)]) + "\n")
                    datacard.write((N1 + N2 - 2) * "-" + "\n")
                    datacard.write("# PROCESSES\n")
                    datacard.write(pad("bin", N1 + N2) + "".join([pad(bin, N4)for process in processes]) + "\n")
                    datacard.write(pad("process", N1 + N2) + "".join([pad(process, N4)for process in processes]) + "\n")
                    datacard.write(pad("process", N1 + N2) + ("".join([pad(str(-s), N4) for s in range(len(signals))][::-1] + [pad(str(b+1), N4) for b in range(len(backgrounds))])) * len(vars) + "\n")
                    datacard.write(pad("rate", N1 + N2) + "".join([pad("-1", N4)for process in processes]) + "\n")
                    datacard.write((N1 + N2 - 2) * "-" + "\n")
                    datacard.write("# SYSTEMATICS\n")

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
