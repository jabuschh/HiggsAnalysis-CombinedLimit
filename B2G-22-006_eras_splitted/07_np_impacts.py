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

impacts_dir_name = 'impacts/'
if not os.path.exists(impacts_dir_name):
    os.mkdir(impacts_dir_name)

os.chdir(impacts_dir_name)

for scenario in scenarios:
    print(scenario)

    if not os.path.exists(scenario):
        os.mkdir(scenario)
    os.chdir(scenario)

    impacts_log_dir_name = 'log/'
    if not os.path.exists(impacts_log_dir_name):
        os.mkdir(impacts_log_dir_name)

    print('initial fits...')
    command_step1 = 'combineTool.py -M Impacts' # method
    command_step1 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step1 += ' -m 125' # higgs mass
    command_step1 += ' --rMin -5 --rMax 5' # set r boundaries (unphysical bounds okay in order to produce symmetric impacts)
    command_step1 += ' --doInitialFit --robustFit 1' # initial fit
    command_step1 += ' -t -1' # Asimov data
    command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
    # further options: --cminDefaultMinimizerStrategy 0 # --rmin -1 --rmax 1 # --expect signal 0
    # print(command_step1)
    log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
    log_file1 = impacts_log_dir_name + 'initial_fit_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file1, 'w') as file:
        file.write(log_step1.stdout.decode())
    with open(log_file1, "r") as file:
        for line in file:
            print(line.rstrip())

    print('do fits...')
    command_step2 = 'combineTool.py -M Impacts' # method
    command_step2 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step2 += ' -m 125' # higgs mass
    command_step2 += ' --rMin -5 --rMax 5' # set r boundaries (unphysical bounds okay in order to produce symmetric impacts)
    command_step2 += ' --doFits --robustFit 1' # do fits
    command_step2 += ' -t -1' # Asimov data
    command_step2 += ' --parallel 8' # multi threading
    command_step2 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
    # print(command_step2)
    log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
    log_file2 = impacts_log_dir_name + 'do_fits_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file2, 'w') as file:
        file.write(log_step2.stdout.decode())
    with open(log_file2, "r") as file:
        for line in file:
            print(line.rstrip())

    print('collect impacts...')
    command_step3 = 'combineTool.py -M Impacts' # method
    command_step3 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step3 += ' -m 125' # higgs mass
    command_step3 += ' --rMin -5 --rMax 5' # set r boundaries (unphysical bounds okay in order to produce symmetric impacts)
    command_step3 += ' -t -1' # Asimov data
    command_step3 += ' -o impacts_' + year_to_run + '_' + scenario + '.json' # output file
    # print(command_step3)
    log_step3 = subprocess.run(['bash', '-c', command_step3], capture_output=True)
    log_file3 = impacts_log_dir_name + 'collect_impacts_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file3, 'w') as file:
        file.write(log_step3.stdout.decode())
    with open(log_file3, "r") as file:
        for line in file:
            print(line.rstrip())

    print('plot impacts...')
    command_step4 = 'plotImpacts.py' # plotter
    command_step4 += ' -i impacts_' + year_to_run + '_' + scenario + '.json' # input
    command_step4 += ' -o impacts_' + year_to_run + '_' + scenario # output
    # print(command_step4)
    log_step4 = subprocess.run(['bash', '-c', command_step4], capture_output=True)
    log_file4 = impacts_log_dir_name + 'plot_impacts_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file4, 'w') as file:
        file.write(log_step4.stdout.decode())
    with open(log_file4, "r") as file:
        for line in file:
            print(line.rstrip())

    os.chdir('..')

os.chdir('..')
