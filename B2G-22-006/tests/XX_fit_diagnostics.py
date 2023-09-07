#!/usr/bin/env python3

import subprocess
import os

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
    # 'posint'
]

dir_name = 'fitdiagnostics/'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)

for scenario in scenarios:
    print(scenario)

    if not os.path.exists(scenario):
        os.mkdir(scenario)
    os.chdir(scenario)

    print('background only...')
    command_step1 = 'combine -M FitDiagnostics' # method
    command_step1 += ' ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step1 += ' -t -1' # use Asimov data
    command_step1 += ' --expectSignal 0' # no signal
    command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year_to_run + '=-5,5' for year in years)
    print(command_step1)
    # log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
    # log_file1 = 'fitdiagnostics_backgroundonly_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    # with open(log_file1, 'w') as file:
    #     file.write(log_step1.stdout.decode())

    print('plotting...')
    command_step2 = 'python3 ../../../test/diffNuisances.py' # method
    command_step2 += ' -a fitDiagnosticsTest.root' # input # TODO: add output name tag!!!
    command_step2 += ' -g plots_backgroundonly_' + scenario + '.root' # output
    print(command_step2)
    # log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
    # log_file2 = 'diffnuisances_backgroundonly_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    # with open(log_file2, 'w') as file:
    #     file.write(log_step2.stdout.decode())

    print('signal + background...')
    command_step3 = 'combine -M FitDiagnostics'
    command_step3 += ' ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root'
    command_step3 += ' -t -1' # use Asimov data
    command_step3 += ' --expectSignal 1' # with signal
    command_step3 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year_to_run + '=-5,5' for year in years)
    print(command_step3)
    # log_step3 = subprocess.run(['bash', '-c', command_step3], capture_output=True)
    # log_file3 = 'fitdiagnostics_signalbackground_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    # with open(log_file3, 'w') as file:
    #     file.write(log_step3.stdout.decode())

    print('plotting...')
    command_step4 = 'python3 ../../../test/diffNuisances.py' # method
    command_step4 += ' -a fitDiagnosticsTest.root' # input # TODO: add output name tag!!!
    command_step4 += ' -g plots_signalbackground_' + scenario + '.root' # output
    print(command_step4)
    # log_step4 = subprocess.run(['bash', '-c', command_step4], capture_output=True)
    # log_file4 = 'diffnuisances_signalbackground_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    # with open(log_file4, 'w') as file:
    #     file.write(log_step4.stdout.decode())

    os.chdir('..')
