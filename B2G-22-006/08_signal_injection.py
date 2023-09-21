#!/usr/bin/env python3

import subprocess
import os

number_of_toys = '250' # default: 250, for testing purposes: e.g. 50
injected_signals = [ # TODO: think about which values to use: 0.5, 0, 2/3
    '0',
    # '0.5',
    # '1',
]

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

    for injected_signal in injected_signals:
        # from Matteo:
        # combine -M MultiDimFit -d ULCombined/AZH_MA-650_MH-450_2DEllipses_CombinedChannels_SR_AllRegions_ws.root -m 125 -t 500 --setParameters r=1 --cminDefaultMinimizerStrategy 0 --saveWorkspace --algo=singles --floatOtherPOIs 1 --rMin -1 --rMax 3 --cminDefaultMinimizerTolerance 1e-2 --cminDefaultMinimizerPrecision 1e-12 -n _r1_MA-650_MH-450
        print('initial fit...')
        command_step1 = 'combine -M MultiDimFit'
        command_step1 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
        command_step1 += ' -m 125' # higgs mass
        command_step1 += ' -t ' + number_of_toys # toys
        command_step1 += ' --setParameters r=' + injected_signal
        command_step1 += ' --rMin -0.2 --rMax 0.2'
        command_step1 += ' --cminDefaultMinimizerStrategy 0 --cminDefaultMinimizerTolerance 1e-2 --cminDefaultMinimizerPrecision 1e-12'
        command_step1 += ' --saveWorkspace'
        command_step1 += ' --algo=singles' # only available for MultiDimFit
        command_step1 += ' --floatOtherPOIs 1' # only available for MultiDimFit
        # command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
        command_step1 += ' -n _r' + injected_signal + '_' + scenario
        print(command_step1)
        log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
        log_file1 = signalinjectiontests_log_dir_name + 'initial_fit_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
        with open(log_file1, 'w') as file:
            file.write(log_step1.stdout.decode())


        # combine -M GenerateOnly --saveToys --expectSignal 1 --setParameters r=1  --rMin 0 --rMax 3 -m 125 -d higgsCombine_r1_MA-650_MH-450.MultiDimFit.mH125.123456.root -t 500 --toysFrequentist --bypassFrequentistFit --snapshotName "MultiDimFit" -n _r1_MA-650_MH-450
        print('generate toys...')
        command_step2 = 'combine -M GenerateOnly' # method
        command_step2 += ' -d higgsCombine_r' + injected_signal + '_' + scenario + '.MultiDimFit.mH125.123456.root' # morphed workspace
        command_step2 += ' -m 125' # higgs mass
        command_step2 += ' --expectSignal ' + injected_signal + ' --rMin -0.2 --rMax 0.2'
        command_step2 += ' -t ' + number_of_toys + ' --toysFrequentist --bypassFrequentistFit' # toys
        command_step2 += ' --saveToys'
        command_step2 += ' --snapshotName "MultiDimFit"'
        command_step2 += ' -n _r' + injected_signal + '_' + scenario # name tag
        print(command_step2)
        log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
        log_file2 = signalinjectiontests_log_dir_name + 'toy_generation_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
        with open(log_file2, 'w') as file:
            file.write(log_step2.stdout.decode())


        print('running fit...')
        command_step3 = 'combine'
        command_step3 += ' higgsCombine_r' + injected_signal + '_' + scenario + '.MultiDimFit.mH125.123456.root' # MultiDimFit
        command_step3 += ' -M FitDiagnostics'
        command_step3 += ' --toysFile higgsCombine_r' + injected_signal + '_' + scenario + '.GenerateOnly.mH125.123456.root' # toys file
        command_step3 += ' -t ' + number_of_toys + ' --toysFrequentist --bypassFrequentistFit' # toys
        command_step3 += ' --setParameters r=' + injected_signal
        command_step3 += ' --rMin -0.2 --rMax 0.2'
        command_step3 += ' --saveWorkspace'
        command_step3 += ' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,Migrad,1:1e-2 --X-rtd MINIMIZER_analytic'
        command_step3 += ' -n _r' + injected_signal + '_' + scenario # name tag
        print(command_step3)
        log_step3 = subprocess.run(['bash', '-c', command_step3], capture_output=True)
        log_file3 = signalinjectiontests_log_dir_name + 'fit_diagnostics_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
        with open(log_file3, 'w') as file:
            file.write(log_step3.stdout.decode())


        print('plotting...')
        command_step4 = 'python3 ../../plot_bias_pull.py'
        command_step4 += ' -i fitDiagnostics_r' + injected_signal + '_' + scenario + '.root' # input file
        command_step4 += ' -t ' + number_of_toys # toys
        command_step4 += ' -r ' + injected_signal # injected signal
        print(command_step4)
        log_step4 = subprocess.run(['bash', '-c', command_step4], capture_output=True)
        log_file4 = signalinjectiontests_log_dir_name + 'plotting_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
        with open(log_file4, 'w') as file:
            file.write(log_step4.stdout.decode())
