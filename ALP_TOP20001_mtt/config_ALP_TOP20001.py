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
vars["mtt"] = "mtt"

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
rates["lumi_13TeV_fullRun2"] = 1.016

# shape systematics: up/down variations
shapes = OrderedDict()
shapes["datasyst"] = ["TTToSemiLeptonic"]
shapes["mcscale"] = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
shapes["pu"] = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
shapes["pdf"] = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
# shapes["isr"] = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]
# shapes["fsr"] = ["TTToSemiLeptonic", "ALP_ttbar_signal", "ALP_ttbar_interference"]


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

        for fa in fas:

            filename_out = "inputHistograms_" + signal_name + "_" + year + "_fa" + str(fa) + ".root"
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

                    # restrict events to EFT validity var: mttbar <= fa
                    hist_in = file_in.Get(vars[var])
                    file_out.cd()
                    hist_out = hist_in.Clone()

                    Nbins = hist_out.GetNbinsX() + 2 # add underflow and overflow bin
                    for bin in range(Nbins):
                        if hist_out.GetBinLowEdge(bin) >= fa:
                            hist_out.SetBinContent(bin, 0.)
                            hist_out.SetBinError(bin, 0.) # needed for combine to ignore this bin
                    hist_out.Write(var + "_" + process)

                    if process == "data_obs": continue

                    for shape in shapes:
                        if process in shapes[shape]:
                            hist_syst_up_in = file_in.Get(vars[var] + "_" + shape + "_up")
                            hist_syst_down_in = file_in.Get(vars[var] + "_" + shape + "_down")
                            hist_syst_up_out = hist_syst_up_in.Clone()
                            hist_syst_down_out = hist_syst_down_in.Clone()

                            for bin in range(Nbins):
                                if hist_syst_up_out.GetBinLowEdge(bin) >= fa:
                                    hist_syst_up_out.SetBinContent(bin, 0.)
                                    hist_syst_up_out.SetBinError(bin, 0.) # needed for combine to ignore this bin
                                if hist_syst_down_out.GetBinLowEdge(bin) >= fa:
                                    hist_syst_down_out.SetBinContent(bin, 0.)
                                    hist_syst_down_out.SetBinError(bin, 0.) # needed for combine to ignore this bin

                            hist_syst_up_out.Write(var + "_" + process + "_" + shape + "Up")
                            hist_syst_down_out.Write(var + "_" + process + "_" + shape + "Down")
                    file_in.Close()

                # characters per column
                N1 = max([len(rate) for rate in rates] + [1]) + 5
                N2 = 8
                N3 = max([len(var) for var in vars]) + 2
                N4 = max([len(process) for process in processes] + [len(var) for var in vars]) + 2

                datacard_name = "datacard_" + signal_name + "_" + year + "_fa" + str(fa) + ".dat"
                with open(datacard_name, 'w') as datacard:
                    datacard.write("# PARAMETERS\n")
                    datacard.write("imax " + str(len(vars)) + " number of vars\n")
                    datacard.write("jmax " + str(len(processes) - 1) + " number of processes -1\n")
                    datacard.write("kmax *\n")
                    datacard.write("shapes * * " + filename_out + " $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n")
                    datacard.write((N1 + N2 - 2) * "-" + "\n")
                    datacard.write("# vars\n")
                    datacard.write("bin          " + "".join([pad(var, N3) for var in vars]) + "\n")
                    datacard.write("observation  " + "".join([pad("-1", N3) for var in vars]) + "\n")
                    datacard.write((N1 + N2 - 2) * "-" + "\n")
                    datacard.write("# PROCESSES\n")
                    datacard.write(pad("bin", N1 + N2) + "".join([pad(var, N4) for var in vars for process in processes]) + "\n")
                    datacard.write(pad("process", N1 + N2) + "".join([pad(process, N4) for var in vars for process in processes]) + "\n")
                    datacard.write(pad("process", N1 + N2) + ("".join([pad(str(-s), N4) for s in range(len(signals))][::-1] + [pad(str(b+1), N4) for b in range(len(backgrounds))])) * len(vars) + "\n")
                    datacard.write(pad("rate", N1 + N2) + "".join([pad("-1", N4)  for var in vars for process in processes]) + "\n")
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
