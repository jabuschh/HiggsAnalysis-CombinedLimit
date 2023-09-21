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
    'posint'
]

pulls_dir_name = 'pulls/'
if not os.path.exists(pulls_dir_name):
    os.mkdir(pulls_dir_name)

os.chdir(pulls_dir_name)

for scenario in scenarios:
    print(scenario)

    if not os.path.exists(scenario):
        os.mkdir(scenario)
    os.chdir(scenario)

    pulls_log_dir_name = 'log/'
    if not os.path.exists(pulls_log_dir_name):
        os.mkdir(pulls_log_dir_name)

    print('running fit...')
    command_step1 = 'combineTool.py -M FitDiagnostics' # method
    command_step1 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step1 += ' -m 125' # higgs mass
    command_step1 += ' -t -1' # Asimov data
    # command_step1 += ' --expectSignal 0' # --rMin -5 --rMax 5
    command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
    command_step1 += ' -n _' + scenario
    print(command_step1)
    log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
    log_file1 = pulls_log_dir_name + 'fit_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file1, 'w') as file:
        file.write(log_step1.stdout.decode())


    print('plotting...')
    command_step2 = 'python3 ../../../test/diffNuisances.py'
    command_step2 += ' fitDiagnostics_' + scenario + '.root'
    # command_step2 += ' --abs --all'
    command_step2 += ' -g pulls_' + scenario + '.root'
    print(command_step2)
    log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
    log_file2 = pulls_log_dir_name + 'plotting_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file2, 'w') as file:
        file.write(log_step2.stdout.decode())


    os.chdir('..')

os.chdir('..')
