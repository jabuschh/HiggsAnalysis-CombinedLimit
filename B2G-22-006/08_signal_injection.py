#!/usr/bin/env python3

import subprocess
import os

number_of_toys = '250' # default: 250, less for testing purposes : e.g. 50
fa = '10000'
year_to_run = 'run2'
years = [
    'UL16preVFP',
    'UL16postVFP',
    'UL17',
    'UL18',
]
scenarios = [
    'negint',
    'posint'
]
injected_signals_negint = [
    '0',
    '0.4783', # exp. limit - 1 sigma
    '0.6270', # exp. limit
    '0.8044', # exp. limit + 1 sigma
]
injected_signals_posint = [
    '0',
    '0.4057', # exp. limit - 1 sigma
    '0.5293', # exp. limit
    '0.6791', # exp. limit + 1 sigma
]




cwd = os.getcwd() + '/'

signalinjectiontests_dir_name = 'signalinjectiontests/'
if not os.path.exists(signalinjectiontests_dir_name):
    os.mkdir(signalinjectiontests_dir_name)

os.chdir(signalinjectiontests_dir_name)

for scenario in scenarios:
    print(scenario)

    if not os.path.exists(scenario):
        os.mkdir(scenario)
    os.chdir(scenario)

    signalinjectiontests_log_dir_name = 'log/'
    if not os.path.exists(signalinjectiontests_log_dir_name):
        os.mkdir(signalinjectiontests_log_dir_name)

    injected_signals = []
    if scenario == 'negint':
        injected_signals = injected_signals_negint
    else:
        injected_signals = injected_signals_posint

    for injected_signal in injected_signals:

        tag = scenario + '_r' + injected_signal + '_' + number_of_toys + 'toys'

        # from Matteo:
        # combine -M MultiDimFit -d ULCombined/AZH_MA-650_MH-450_2DEllipses_CombinedChannels_SR_AllRegions_ws.root -m 125 -t 500 --setParameters r=1 --cminDefaultMinimizerStrategy 0 --saveWorkspace --algo=singles --floatOtherPOIs 1 --rMin -10 --rMax 10 --cminDefaultMinimizerTolerance 1e-2 --cminDefaultMinimizerPrecision 1e-12 -n _r1_MA-650_MH-450
        print('initial fit...')
        command_step1 = 'combine -M MultiDimFit'
        command_step1 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
        command_step1 += ' -v 1' # print out verbosity level
        command_step1 += ' -m 125' # higgs mass
        command_step1 += ' -t ' + number_of_toys # toys
        command_step1 += ' --setParameters r=' + injected_signal
        command_step1 += ' --rMin -10 --rMax 10'
        # command_step1 += ' --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 1e-2 --cminDefaultMinimizerPrecision 1e-12'
        command_step1 += ' --saveWorkspace'
        command_step1 += ' --algo=singles' # only available for MultiDimFit
        # command_step1 += ' --floatOtherPOIs 1' # why? -> try 0 (default)
        command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
        command_step1 += ' -n _' + tag
        print(command_step1 + '\n')
        log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
        log_file1 = signalinjectiontests_log_dir_name + '1_initialfit_' + tag + '.log'
        with open(log_file1, 'w') as file:
            file.write(log_step1.stdout.decode())


        # combine -M GenerateOnly --saveToys --expectSignal 1 --setParameters r=1  --rMin 0 --rMax 3 -m 125 -d higgsCombine_r1_MA-650_MH-450.MultiDimFit.mH125.123456.root -t 500 --toysFrequentist --bypassFrequentistFit --snapshotName "MultiDimFit" -n _r1_MA-650_MH-450
        print('generate toys...')
        command_step2 = 'combine -M GenerateOnly' # method
        command_step2 += ' -d higgsCombine_' + tag + '.MultiDimFit.mH125.123456.root' # morphed workspace
        command_step2 += ' -m 125' # higgs mass
        command_step2 += ' --expectSignal ' + injected_signal + ' --rMin -10 --rMax 10'
        command_step2 += ' -t ' + number_of_toys + ' --toysFrequentist --bypassFrequentistFit' # toys
        command_step2 += ' --saveToys'
        command_step2 += ' --snapshotName "MultiDimFit"'
        command_step2 += ' -n _' + tag
        print(command_step2 + '\n')
        log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
        log_file2 = signalinjectiontests_log_dir_name + '2_toygeneration_' + tag +  '.log'
        with open(log_file2, 'w') as file:
            file.write(log_step2.stdout.decode())


        print('running fit...')
        command_step3 = 'combine'
        command_step3 += ' higgsCombine_' + tag + '.MultiDimFit.mH125.123456.root' # MultiDimFit
        command_step3 += ' -M FitDiagnostics'
        command_step3 += ' --toysFile higgsCombine_' + tag + '.GenerateOnly.mH125.123456.root' # toys file
        command_step3 += ' -t ' + number_of_toys + ' --toysFrequentist --bypassFrequentistFit' # toys
        command_step3 += ' --setParameters r=' + injected_signal
        command_step3 += ' --rMin -10 --rMax 10'
        command_step3 += ' --saveWorkspace'
        # command_step3 += ' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,Migrad,1:1e-2 --X-rtd MINIMIZER_analytic'
        command_step3 += ' --noErrors --minos none'
        command_step3 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
        command_step3 += ' -n _' + tag
        print(command_step3 + '\n')
        log_step3 = subprocess.run(['bash', '-c', command_step3], capture_output=True)
        log_file3 = signalinjectiontests_log_dir_name + '3_fitdiagnostics_' + tag + '.log'
        with open(log_file3, 'w') as file:
            file.write(log_step3.stdout.decode())


        print('plotting...')
        command_step4 = 'python3 ../../plot_bias_pull.py'
        command_step4 += ' -i fitDiagnostics_' + tag + '.root' # input file
        command_step4 += ' -t ' + number_of_toys # toys
        command_step4 += ' -r ' + injected_signal # injected signal
        command_step4 += ' -o ' + tag
        print(command_step4 + '\n')
        log_step4 = subprocess.run(['bash', '-c', command_step4], capture_output=True)
        log_file4 = signalinjectiontests_log_dir_name + '4_plotting_' + tag + '.log'
        with open(log_file4, 'w') as file:
            file.write(log_step4.stdout.decode())

    os.chdir('..')
