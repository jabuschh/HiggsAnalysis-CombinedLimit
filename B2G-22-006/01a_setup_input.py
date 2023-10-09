#!/usr/bin/env python3

import ROOT
import collections
import os
import shutil
import array
import math
from collections import OrderedDict, Mapping

inputdirs = {
    'UL16preVFP': {
        'electron': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL16preVFP/electron/',
        'muon': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL16preVFP/muon/'
    },
    'UL16postVFP': {
        'electron': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL16postVFP/electron/',
        'muon': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL16postVFP/muon/'
    },
    'UL17': {
        'electron': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL17/electron/',
        'muon': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL17/muon/'
    },
    'UL18': {
        'electron': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL18/electron/',
        'muon': '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_UL18/muon/'
    }
}

inputbasedir_pdf = '/nfs/dust/cms/user/jabuschh/uhh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/macros/src/PDF_hists/'
inputbasedir_mcscale = '/nfs/dust/cms/user/jabuschh/uhh2-106X_v2/CMSSW_10_6_28/src/UHH2/ZprimeSemiLeptonic/macros/src/Scale_hists/'

signals = [
    'ALP_ttbar_signal',
    'ALP_ttbar_interference'
]

# binning: input histogram has 400 bins of 25 GeV width
# in GeV
binning = array.array('d', [
    0,
    # 500,
    750,
    1000,
    1250,
    1500,
    1750,
    2000,
    2500,
    3000,
    10000,
])

fas = [
    # 500,
    750,
    1000,
    1250,
    1500,
    1750,
    2000,
    2500,
    3000,
    10000,
]

backgrounds = [
    'TTbar',
    'ST',
    'WJets',
    'others', # DY + Diboson + QCD
]

data = [
    'DATA', # real data -> renamed to 'data_obs'
    'data_obs', # Asimov data -> renamed to 'data_asimov'
]

processes = signals + backgrounds

regions = OrderedDict()
regions['SR_bin1_TopTag']   = 'Zprime_SystVariations_DNN_output0_TopTag_thetastar_bin1'
regions['SR_bin1_NoTopTag'] = 'Zprime_SystVariations_DNN_output0_NoTopTag_thetastar_bin1'
regions['SR_bin2_TopTag']   = 'Zprime_SystVariations_DNN_output0_TopTag_thetastar_bin2'
regions['SR_bin2_NoTopTag'] = 'Zprime_SystVariations_DNN_output0_NoTopTag_thetastar_bin2'
regions['SR_bin3_TopTag']   = 'Zprime_SystVariations_DNN_output0_TopTag_thetastar_bin3'
regions['SR_bin3_NoTopTag'] = 'Zprime_SystVariations_DNN_output0_NoTopTag_thetastar_bin3'
regions['SR_bin4']          = 'Zprime_SystVariations_DNN_output0_thetastar_bin4'
regions['SR_bin5']          = 'Zprime_SystVariations_DNN_output0_thetastar_bin5'
regions['SR_bin6']          = 'Zprime_SystVariations_DNN_output0_thetastar_bin6'
regions['CR1']              = 'Zprime_SystVariations_DNN_output1'
regions['CR2']              = 'Zprime_SystVariations_DNN_output2'

var = 'M_Zprime'

# normalization systematics
rates = OrderedDict()
rates['ttbar_rate'] = 1.2
rates['st_rate'] = 1.3
rates['wjets_rate'] = 1.5
rates['others_rate'] = 1.5
rates['lumi_13TeV'] = 1.016
# rates['lumi_13TeV_uncorrelated_UL16'] = 1.010
# rates['lumi_13TeV_uncorrelated_UL17'] = 1.020
# rates['lumi_13TeV_uncorrelated_UL18'] = 1.015
# rates['lumi_13TeV_correlated_UL16_UL17_UL18'] = {'UL16': 1.006, 'UL17': 1.009, 'UL18': 1.02}
# rates['lumi_13TeV_correlated_UL17_UL18'] = {'UL16': '-', 'UL17': 1.006, 'UL18': 1.002}

# shape systematics: up/down variations
shapes = OrderedDict()
shapes['pdf']           = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # pdf uncertainty # TODO: comment in once ST is fixed
shapes['mcscale']       = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # mcscale uncertainty: envelope of muR and muF up/down combinations
shapes['pu']            = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # pileup
shapes['prefiring']     = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # prefiring
shapes['mu_id']         = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # muon id
shapes['mu_iso']        = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # muon isolation
shapes['mu_reco']       = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # muon reconstruction
shapes['mu_trigger']    = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # muon trigger
shapes['ele_id']        = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # electron id
shapes['ele_reco']      = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # electron reconstruction
shapes['ele_trigger']   = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # electron trigger
shapes['btag_cferr1']   = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # charm jet uncertainty 1 (correlated)
shapes['btag_cferr2']   = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # charm jet uncertainty 2 (correlated)
shapes['btag_hf']       = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # heavy flavor purity uncertainty (correlated)
shapes['btag_hfstats1'] = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # heavy flavor statistical uncertainty (uncorrelated)
shapes['btag_hfstats2'] = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # heavy flavor statistical uncertainty (uncorrelated)
shapes['btag_lf']       = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # light flavor purity uncertainty (correlated)
shapes['btag_lfstats1'] = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # light flavor statistical uncertainty (uncorrelated)
shapes['btag_lfstats2'] = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # light flavor statistical uncertainty (uncorrelated)
shapes['ttag_corr']     = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # top tag uncertainty (correlated)
shapes['ttag_uncorr']   = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # top tag uncertainty (uncorrelated)
shapes['tmistag']       = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # top mistag uncertainty
shapes['jec']           = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # jet energy corrections
shapes['jer']           = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # jet energy resolution
# currently not used:
# shapes['isr'] = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # initial state radiation
# shapes['fsr'] = ['TTbar','ST','WJets','others','ALP_ttbar_signal','ALP_ttbar_interference'] # final state radiation

uncorrelated_shapes = ['btag_hfstats1','btag_hfstats2','btag_lfstats1','btag_lfstats2','ttag_uncorr']


# characters per column
N1 = max([len(rate) for rate in rates] + [len(shape) for shape in shapes] + [1]) + 15
N2 = 8
N3 = max([len(region) for region in regions]) + 2
N4 = max([len(process) for process in processes] + [len(region) for region in regions]) + 2

def nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, Mapping):
            for inner_key, inner_value in nested_dict_iter(value):
                yield key, inner_key, inner_value
        else:
            yield key, value

def check_file(file_path):
    if not os.path.isfile(file_path):
        raise ValueError('file does not exist: ' + str(file_path))

def pad(s, n_pad):
    s = str(s)
    n_pad = n_pad - len(s)
    return s + n_pad * ' '


def createCombineInput():

    cwd = os.getcwd() + '/'

    rootfiles_dir_name = cwd
    rootfiles_dir_name += 'rootfiles/'
    if not os.path.exists(rootfiles_dir_name):
        os.mkdir(rootfiles_dir_name)

    datacards_dir_name = cwd
    datacards_dir_name += 'datacards/'
    if not os.path.exists(datacards_dir_name):
        os.mkdir(datacards_dir_name)


    print('creating input files...')
    list_inputdirs = list(nested_dict_iter(inputdirs))

    for entry in list_inputdirs:
        year = entry[0]
        channel = entry[1]
        inputdir = entry[2]
        print((year + ' ' + channel + ' channel'))

        for fa in fas:
            # print(fa)
            filename_out = rootfiles_dir_name + 'inputhists_' + year + '_' + channel + '_fa' + str(fa) + '.root'
            file_out = ROOT.TFile(filename_out, 'RECREATE')

            for region in regions:
                # print(region)
                for process in data + processes:
                    # print(process)

                    process_prefix = 'uhh2.AnalysisModuleRunner.'
                    if process == 'DATA':
                        process_prefix += 'DATA.'
                    else:
                        process_prefix += 'MC.'

                    filename_in = inputdir + process_prefix + process + '.root'
                    check_file(filename_in)
                    file_in = ROOT.TFile(filename_in)
                    if process in processes:
                        filename_in_pdf = inputbasedir_pdf + year + '/' + channel + '/' + process_prefix + process + '.root'
                        check_file(filename_in_pdf)
                        file_in_pdf = ROOT.TFile(filename_in_pdf)

                        filename_in_mcscale = inputbasedir_mcscale + year + '/' + channel + '/' + process_prefix + process + '.root'
                        check_file(filename_in_mcscale)
                        file_in_mcscale = ROOT.TFile(filename_in_mcscale)

                        filename_in_jec_up = '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_' + year + '/JEC_up/' + channel + '/' + process_prefix + process + '.root'
                        check_file(filename_in_jec_up)
                        file_in_jec_up = ROOT.TFile(filename_in_jec_up)
                        filename_in_jec_down = '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_' + year + '/JEC_down/' + channel + '/' + process_prefix + process + '.root'
                        check_file(filename_in_jec_down)
                        file_in_jec_down = ROOT.TFile(filename_in_jec_down)

                        filename_in_jer_up = '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_' + year + '/JER_up/' + channel + '/' + process_prefix + process + '.root'
                        check_file(filename_in_jer_up)
                        file_in_jer_up = ROOT.TFile(filename_in_jer_up)
                        filename_in_jer_down = '/nfs/dust/cms/group/zprime-uhh/AnalysisDNN_' + year + '/JER_down/' + channel + '/' + process_prefix + process + '.root'
                        check_file(filename_in_jer_down)
                        file_in_jer_down = ROOT.TFile(filename_in_jer_down)

                    if process == 'DATA':
                        hist_in = file_in.Get(regions[region][22:] + '_General' + '/' + var) # different syntax for real data
                    else:
                        hist_in = file_in.Get(regions[region] + '/' + var)
                    hist_in_rebinned = hist_in.Rebin(len(binning)-1, "rebinned", binning) #rebinning

                    # add overflow bin content to highest bin
                    overflow_bin = hist_in_rebinned.GetNbinsX()+1
                    overflow_bin_content = hist_in_rebinned.GetBinContent(overflow_bin)
                    overflow_bin_error = hist_in_rebinned.GetBinError(overflow_bin)

                    if fa == fas[-1] and overflow_bin_content > 0:
                        highest_bin = hist_in_rebinned.GetNbinsX()
                        highest_bin_content = hist_in_rebinned.GetBinContent(highest_bin)
                        highest_bin_errror = hist_in_rebinned.GetBinError(highest_bin)
                        hist_in_rebinned.SetBinContent(highest_bin, highest_bin_content + overflow_bin_content)
                        hist_in_rebinned.SetBinError(highest_bin, math.sqrt(highest_bin_content**2 + overflow_bin_content**2))

                    # print out bin contents for rebinning
                    # if fa == 10000 and process == 'DATA':
                    #     for bin in range(1, hist_in_rebinned.GetNbinsX()+1):
                    #         bin_content = hist_in_rebinned.GetBinContent(bin)
                    #         # if bin_content < 1.:
                    #         print('bin ' + str(bin) + ': ' + str(bin_content))

                    file_out.cd()
                    hist_out = hist_in_rebinned.Clone()
                    if process == 'ALP_ttbar_interference':
                        hist_out.Scale(-1)

                    # restrict events to EFT validity region: mttbar <= fa
                    Nbins = hist_out.GetNbinsX() + 2 # add underflow and overflow bin
                    if 'M_Zprime' in var:
                        for bin in range(Nbins):
                            # print('bin ' + str(bin) + ', low edge: ' + str(hist_out.GetBinLowEdge(bin)) +  ', content: ' + str(hist_out.GetBinContent(bin)))
                            if hist_out.GetBinLowEdge(bin) >= fa:
                                hist_out.SetBinContent(bin, 0.)
                                hist_out.SetBinError(bin, 0.) # needed for combine to ignore this bin

                    if process == 'DATA':
                        hist_out.Write(var + '_' + region + '_data_obs')
                    elif process == 'data_obs':
                        hist_out.Write(var + '_' + region + '_data_asimov')
                    else:
                        hist_out.Write(var + '_' + region + '_' + process)

                    if process in data: continue

                    for shape in shapes:
                        # print(shape)
                        if process in shapes[shape]:
                            if shape == 'pdf':
                                # print(regions[region] + '/' + var + '_' + shape + '_up')
                                hist_syst_up_in = file_in_pdf.Get(regions[region] + '/' + var + '_' + shape + '_up')
                                hist_syst_down_in = file_in_pdf.Get(regions[region] + '/' + var + '_' + shape + '_down')
                            elif shape == 'mcscale':
                                hist_syst_up_in = file_in_mcscale.Get(regions[region] + '/' + var + '_' + shape + '_up')
                                hist_syst_down_in = file_in_mcscale.Get(regions[region] + '/' + var + '_' + shape + '_down')
                            elif shape == 'jec':
                                hist_syst_up_in = file_in_jec_up.Get(regions[region] + '/' + var)
                                hist_syst_down_in = file_in_jec_down.Get(regions[region] + '/' + var)
                            elif shape == 'jer':
                                hist_syst_up_in = file_in_jer_up.Get(regions[region] + '/' + var)
                                hist_syst_down_in = file_in_jer_down.Get(regions[region] + '/' + var)
                            else:
                                hist_syst_up_in = file_in.Get(regions[region] + '/' + var + '_' + shape + '_up')
                                hist_syst_down_in = file_in.Get(regions[region] + '/' + var + '_' + shape + '_down')
                            hist_syst_up_in_rebinned = hist_syst_up_in.Rebin(len(binning)-1, "rebinned", binning)
                            hist_syst_down_in_rebinned = hist_syst_down_in.Rebin(len(binning)-1, "rebinned", binning)

                            hist_syst_up_out_rebinned = hist_syst_up_in_rebinned.Clone()
                            hist_syst_down_out_rebinned = hist_syst_down_in_rebinned.Clone()
                            if process == 'ALP_ttbar_interference':
                                hist_syst_up_out_rebinned.Scale(-1)
                                hist_syst_down_out_rebinned.Scale(-1)

                            if 'M_Zprime' in var:
                                for bin in range(Nbins):
                                    # if hist_syst_up_out_rebinned.GetBinContent(bin) < 0: # negative variations are not properly handled by combine -> set them to basically zero (has to be >0 for bogus norm computation)
                                        # hist_syst_up_out_rebinned.SetBinContent(bin, 1E-9)
                                        # hist_syst_up_out_rebinned.SetBinError(bin, 0.)
                                    # if hist_syst_down_out_rebinned.GetBinContent(bin) < 0: # negative variations are not properly handled by combine -> set them to basically zero (has to be >0 for bogus norm computation)
                                        # hist_syst_down_out_rebinned.SetBinContent(bin, 1E-9)
                                        # hist_syst_down_out_rebinned.SetBinError(bin, 0.)

                                    if hist_syst_up_out_rebinned.GetBinLowEdge(bin) >= fa:
                                        hist_syst_up_out_rebinned.SetBinContent(bin, 0.)
                                        hist_syst_up_out_rebinned.SetBinError(bin, 0.) # needed for combine to ignore this bin
                                    if hist_syst_down_out_rebinned.GetBinLowEdge(bin) >= fa:
                                        hist_syst_down_out_rebinned.SetBinContent(bin, 0.)
                                        hist_syst_down_out_rebinned.SetBinError(bin, 0.) # needed for combine to ignore this bin

                            if shape in uncorrelated_shapes:
                                hist_syst_up_out_rebinned.Write(var + '_' + region + '_' + process + '_' + shape + '_' + year + 'Up')
                                hist_syst_down_out_rebinned.Write(var + '_' + region + '_' + process + '_' + shape + '_' + year + 'Down')
                                other_years = ['UL16preVFP', 'UL16postVFP', 'UL17', 'UL18']
                                other_years.remove(year)
                                for other_year in other_years: # nominal hist for other years
                                    hist_out.Write(var + '_' + region + '_' + process + '_' + shape + '_' + other_year + 'Up')
                                    hist_out.Write(var + '_' + region + '_' + process + '_' + shape + '_' + other_year + 'Down')
                            else:
                                hist_syst_up_out_rebinned.Write(var + '_' + region + '_' + process + '_' + shape + 'Up')
                                hist_syst_down_out_rebinned.Write(var + '_' + region + '_' + process + '_' + shape + 'Down')
                    file_in.Close()
            file_out.Close()


    # hadding for full Run2
    print('hadding...')
    for fa in fas:
        os.system('hadd -f ' + rootfiles_dir_name + 'inputhists_run2_fa' + str(fa) + '.root ' + rootfiles_dir_name + 'inputhists_UL1*_fa' + str(fa) + '.root')


    # write datacards for combined Run2 only
    print('writing datacards...')
    for fa in fas:

        datacard_name = 'datacard_run2_fa' + str(fa) + '.txt'
        with open(datacards_dir_name + datacard_name, 'w') as datacard:
            datacard.write('# PARAMETERS\n')
            datacard.write('imax ' + str(len(regions)) + ' number of regions\n')
            datacard.write('jmax ' + str(len(processes) - 1) + ' number of processes -1\n')
            datacard.write('kmax *\n')
            datacard.write('shapes * * ' + rootfiles_dir_name + 'inputhists_run2_fa' + str(fa) + '.root' + ' ' + var + '_$CHANNEL_$PROCESS ' + var + '_$CHANNEL_$PROCESS_$SYSTEMATIC\n')
            datacard.write((N1 + N2 - 2) * '-' + '\n')
            datacard.write('# regions\n')
            datacard.write('bin          ' + ''.join([pad(region, N3) for region in regions]) + '\n')
            datacard.write('observation  ' + ''.join([pad('-1', N3) for region in regions]) + '\n')
            datacard.write((N1 + N2 - 2) * '-' + '\n')
            datacard.write('# PROCESSES\n')
            datacard.write(pad('bin', N1 + N2) + ''.join([pad(region, N4) for region in regions for process in processes]) + '\n') # exclude signal from CRs: "for region in regions for process in processes if not (process in signals and 'CR' in region)"
            datacard.write(pad('process', N1 + N2) + ''.join([pad(process, N4) for region in regions for process in processes]) + '\n')
            datacard.write(pad('process', N1 + N2) + (''.join([pad(str(-s), N4) for s in range(len(signals))][::-1] + [pad(str(b+1), N4) for b in range(len(backgrounds))])) * len(regions) + '\n')
            datacard.write(pad('rate', N1 + N2) + ''.join([pad('-1', N4) for region in regions for process in processes]) + '\n')
            datacard.write((N1 + N2 - 2) * '-' + '\n')
            datacard.write('# SYSTEMATICS\n')

            # normalization systematics
            for rate in rates:
                datacard.write(pad(rate, N1) + pad('lnN', N2))
                for region in regions:
                    for process in processes:
                        if rate == 'lumi_13TeV':
                            datacard.write(pad('1.016', N4))
                        elif process.lower() + '_rate' == rate: # cross sections
                            datacard.write(pad(rates[rate], N4))
                        else: # other
                            datacard.write(pad('-', N4))
                datacard.write('\n')

            # shape systematics
            for shape in shapes:
                # print(shape)
                if shape not in uncorrelated_shapes:
                    if 'ttag' in shape:
                        datacard.write(pad(shape, N1) + pad('shapeU', N2))
                    else:
                        datacard.write(pad(shape, N1) + pad('shape', N2))
                    for region in regions:
                        for process in processes:
                            if process in shapes[shape]:
                                datacard.write(pad('1.0', N4))
                            else:
                                datacard.write(pad('-', N4))
                    datacard.write('\n')
                else:
                    for year in ['UL16preVFP','UL16postVFP','UL17','UL18']:
                        if 'ttag' in shape:
                            datacard.write(pad(shape + '_' + year, N1) + pad('shapeU', N2))
                        else:
                            datacard.write(pad(shape + '_' + year, N1) + pad('shape', N2))
                        for region in regions:
                            for process in processes:
                                if process in shapes[shape]:
                                    datacard.write(pad('1.0', N4))
                                else:
                                    datacard.write(pad('-', N4))
                        datacard.write('\n')

            datacard.write((N1 + N2 - 2) * '-' + '\n')
            datacard.write('* autoMCStats 0 0 1')

    print('...done!')


if __name__ == '__main__':
    createCombineInput()
