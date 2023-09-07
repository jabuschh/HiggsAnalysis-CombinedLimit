#!/usr/bin/env python3

import subprocess
import os

number_of_toys = '50' # default: 250, for testing purposes: e.g. 50
injected_signals = [ # TODO: think about which values to use: 0.5, 0, 2/3
    # '0',
    # '0.5',
    '1',
]

fa = '10000'

year_to_run = 'run2'
years = [
    'UL16preVFP',
    'UL16postVFP',
    'UL17',
    'UL18',
]

# channel_tags = [
#     'el',
#     'mu',
# ]

# regions = [
#     'SR_bin1_TopTag',
#     'SR_bin1_NoTopTag',
#     'SR_bin2_TopTag',
#     'SR_bin2_NoTopTag',
#     'SR_bin3_TopTag',
#     'SR_bin3_NoTopTag',
#     # 'SR_bin4_TopTag',
#     # 'SR_bin4_NoTopTag',
#     'SR_bin4',
#     'SR_bin5',
#     'SR_bin6',
#     'CR1',
#     'CR2',
# ]

# # set masks
# masks = []
# for year in years:
#     for channel_tag in channel_tags:
#         for region in regions:
#             masks.append('mask_' + year + '_' + channel_tag + '_' + region)
# # print(masks)
# # print(len(masks))

scenarios = [
    'negint',
    # 'posint'
]

cwd = os.getcwd() + '/'

biastest_dir_name = 'biastests/'
if not os.path.exists(biastest_dir_name):
    os.mkdir(biastest_dir_name)

os.chdir(biastest_dir_name)

for scenario in scenarios:
    print(scenario)

    if not os.path.exists(scenario):
        os.mkdir(scenario)
    os.chdir(scenario)

    biastest_log_dir_name = 'log/'
    if not os.path.exists(biastest_log_dir_name):
        os.mkdir(biastest_log_dir_name)

    for injected_signal in injected_signals:
        # from Matteo:
        # combine -M MultiDimFit -d ULCombined/AZH_MA-650_MH-450_2DEllipses_CombinedChannels_SR_AllRegions_ws.root -m 125 -t 500 --setParameters r=1 --cminDefaultMinimizerStrategy 0 --saveWorkspace --algo=singles --floatOtherPOIs 1 --rMin -1 --rMax 3 --cminDefaultMinimizerTolerance 1e-2 --cminDefaultMinimizerPrecision 1e-12 -n _r1_MA-650_MH-450
        print('initial fit...')
        command_step1 = 'combine -M MultiDimFit'
        command_step1 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
        command_step1 += ' -m 125' # higgs mass
        command_step1 += ' -t ' + number_of_toys # toys (50 for testing purposes)
        command_step1 += ' --setParameters r=' + injected_signal
        command_step1 += ' --rMin -5 --rMax 5'
        command_step1 += ' --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 1e-2 --cminDefaultMinimizerPrecision 1e-12'
        command_step1 += ' --saveWorkspace'
        command_step1 += ' --algo=singles' # only available for MultiDimFit
        command_step1 += ' --floatOtherPOIs 1' # only available for MultiDimFit
        # command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
        command_step1 += ' -n _r' + injected_signal + '_' + scenario
        print(command_step1)

        # print('create morphed workspace...')
        # command_step2 = 'python ../../importPars.py'
        # command_step2 += ' ../../datacards/datacard_' + year_to_run + '_fa' + fa + '.txt' # input datacard
        # command_step2 += ' fitDiagnostics_' + scenario + '.root' # output from step 1
        # print(command_step2)

        # combine -M GenerateOnly --saveToys --expectSignal 1 --setParameters r=1  --rMin -1 --rMax 13 -m 125 -d higgsCombine_r1_MA-650_MH-450.MultiDimFit.mH125.123456.root -t 500 --toysFrequentist --bypassFrequentistFit --snapshotName "MultiDimFit" -n _r1_MA-650_MH-450
        print('generate toys...')
        command_step3 = 'combine -M GenerateOnly' # method
        command_step3 += ' -d higgsCombine_r' + injected_signal + '_' + scenario + '.MultiDimFit.mH125.123456.root' # morphed workspace
        command_step3 += ' -m 125' # higgs mass
        command_step3 += ' --expectSignal ' + injected_signal + ' --rMin -5 --rMax 5'
        command_step3 += ' -t ' + number_of_toys + ' --toysFrequentist --bypassFrequentistFit' # toys
        command_step3 += ' --saveToys'
        command_step3 += ' --snapshotName "MultiDimFit"'
        command_step3 += ' -n _r' + injected_signal + '_' + scenario # name tag
        print(command_step3)

        print('running fit...')
        command_step4 = 'combine'
        command_step4 += ' higgsCombine_r' + injected_signal + '_' + scenario + '.MultiDimFit.mH125.123456.root' # MultiDimFit
        command_step4 += ' -M FitDiagnostics'
        command_step4 += ' --toysFile higgsCombine_r' + injected_signal + '_' + scenario + '.GenerateOnly.mH125.123456.root' # toys file
        command_step4 += ' -t ' + number_of_toys + ' --toysFrequentist --bypassFrequentistFit' # toys
        command_step4 += ' --setParameters r=' + injected_signal
        command_step4 += ' --rMin -5 --rMax 5'
        command_step4 += ' --saveWorkspace'
        command_step4 += ' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,Migrad,1:1e-2 --X-rtd MINIMIZER_analytic'
        command_step4 += ' -n _r' + injected_signal + '_' + scenario # name tag
        print(command_step4)

        print('plotting...')
        command_step5 = 'python3 ../../plot_bias_pull.py'
        command_step5 += ' -i fitDiagnostics_r' + injected_signal + '_' + scenario + '.root' # input file
        command_step5 += ' -t 50' # toys
        command_step5 += ' -r ' + injected_signal # injected signal
        # command_step5 += ' -i ' + cwd + biastest_dir_name + scenario + '/fitDiagnosticsTest.root'
        print(command_step5)
