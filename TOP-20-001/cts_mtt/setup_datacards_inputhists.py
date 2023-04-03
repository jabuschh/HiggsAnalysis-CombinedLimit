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

backgrounds = [
    "TTToSemiLeptonic"
]

data = [
    "data_obs"
]

processes = signals + backgrounds

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

    # characters per column
    N1 = max([len(rate) for rate in rates] + [1]) + 5
    N2 = 8
    N3 = 6
    N4 = max([len(process) for process in processes]) + 2

    for entry in list_inputdirs:

        year = entry[0]
        inputdir = entry[1]
        print(year)

        for fa in fas:

            filename_out = "inputHistograms_" + year + "_fa" + str(fa) + ".root"
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
                hist_in_bin1 = file_in.Get("cts_mtt250To420")
                hist_in_bin2 = file_in.Get("cts_mtt420To520")
                hist_in_bin3 = file_in.Get("cts_mtt520To620")
                hist_in_bin4 = file_in.Get("cts_mtt620To800")
                hist_in_bin5 = file_in.Get("cts_mtt800To1000")
                hist_in_bin6 = file_in.Get("cts_mtt1000To3500")
                file_out.cd()

                hist_out = hist_in_bin1.Clone()
                hist_out.SetName("cts_" + process)
                if(fa == 520):
                    hist_out.Add(hist_in_bin2)
                elif(fa == 620):
                    hist_out.Add(hist_in_bin2)
                    hist_out.Add(hist_in_bin3)
                elif(fa == 800):
                    hist_out.Add(hist_in_bin2)
                    hist_out.Add(hist_in_bin3)
                    hist_out.Add(hist_in_bin4)
                elif(fa == 1000):
                    hist_out.Add(hist_in_bin2)
                    hist_out.Add(hist_in_bin3)
                    hist_out.Add(hist_in_bin4)
                    hist_out.Add(hist_in_bin5)
                elif(fa == 3500):
                    hist_out.Add(hist_in_bin2)
                    hist_out.Add(hist_in_bin3)
                    hist_out.Add(hist_in_bin4)
                    hist_out.Add(hist_in_bin5)
                    hist_out.Add(hist_in_bin6)
                hist_out.Write()

                if process == "data_obs": continue

                for shape in shapes:
                    if process in shapes[shape]:
                        for var in ["up", "down"]:
                            hist_in_bin1_syst = file_in.Get("cts_mtt250To420_" + shape + "_" + var)
                            hist_in_bin2_syst = file_in.Get("cts_mtt420To520_" + shape + "_" + var)
                            hist_in_bin3_syst = file_in.Get("cts_mtt520To620_" + shape + "_" + var)
                            hist_in_bin4_syst = file_in.Get("cts_mtt620To800_" + shape + "_" + var)
                            hist_in_bin5_syst = file_in.Get("cts_mtt800To1000_" + shape + "_" + var)
                            hist_in_bin6_syst = file_in.Get("cts_mtt1000To3500_" + shape + "_" + var)

                            hist_syst_out = hist_in_bin1_syst.Clone()
                            if(fa == 520):
                                hist_syst_out.Add(hist_in_bin2_syst)
                            elif(fa == 620):
                                hist_syst_out.Add(hist_in_bin2_syst)
                                hist_syst_out.Add(hist_in_bin3_syst)
                            elif(fa == 800):
                                hist_syst_out.Add(hist_in_bin2_syst)
                                hist_syst_out.Add(hist_in_bin3_syst)
                                hist_syst_out.Add(hist_in_bin4_syst)
                            elif(fa == 1000):
                                hist_syst_out.Add(hist_in_bin2_syst)
                                hist_syst_out.Add(hist_in_bin3_syst)
                                hist_syst_out.Add(hist_in_bin4_syst)
                                hist_syst_out.Add(hist_in_bin5_syst)
                            elif(fa == 3500):
                                hist_syst_out.Add(hist_in_bin2_syst)
                                hist_syst_out.Add(hist_in_bin3_syst)
                                hist_syst_out.Add(hist_in_bin4_syst)
                                hist_syst_out.Add(hist_in_bin5_syst)
                                hist_syst_out.Add(hist_in_bin6_syst)

                            if(var == "up"):
                                hist_syst_out.SetName("cts_" + process + "_" + shape + "Up")
                            else:
                                hist_syst_out.SetName("cts_" + process + "_" + shape + "Down")
                            hist_syst_out.Write()

                file_in.Close()

            datacard_name = "datacard_" + year + "_fa" + str(fa) + ".dat"
            with open(datacard_name, 'w') as datacard:
                datacard.write("# PARAMETERS\n")
                datacard.write("imax 1 number of regions\n")
                datacard.write("jmax " + str(len(processes) - 1) + " number of processes -1\n")
                datacard.write("kmax *\n")
                datacard.write("shapes * * " + filename_out + " $CHANNEL_$PROCESS $CHANNEL_$PROCESS_$SYSTEMATIC\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# regions\n")
                datacard.write("bin          " + "".join([pad("cts", N3)]) + "\n")
                datacard.write("observation  " + "".join([pad("-1", N3)]) + "\n")
                datacard.write((N1 + N2 - 2) * "-" + "\n")
                datacard.write("# PROCESSES\n")
                datacard.write(pad("bin", N1 + N2) + "".join([pad("cts", N4) for process in processes]) + "\n")
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
