#!/usr/bin/env python3

import subprocess
import os

year_to_run = 'run2'
years = [
    'UL16preVFP',
    'UL16postVFP',
    'UL17',
    'UL18',
]

channel_tags = [
    'el',
    'mu',
]

regions = [
    'SR_bin1_TopTag',
    'SR_bin1_NoTopTag',
    'SR_bin2_TopTag',
    'SR_bin2_NoTopTag',
    'SR_bin3_TopTag',
    'SR_bin3_NoTopTag',
    # 'SR_bin4_TopTag',
    # 'SR_bin4_NoTopTag',
    'SR_bin4',
    'SR_bin5',
    'SR_bin6',
    'CR1',
    'CR2',
]

# set masks
masks = []
for region in regions:
    masks.append('mask_' + region)
print(masks)
print(len(masks))

fa = '10000'

scenarios = [
    'negint',
    'posint',
]

dir_name = 'goodnessoffittests/'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
os.chdir(dir_name)

for scenario in scenarios:
    print(scenario)

    if not os.path.exists(scenario):
        os.mkdir(scenario)
    os.chdir(scenario)

    print('fit on data (SRs masked)...')
    command_step1 = 'combine -M GoodnessOfFit' # method
    command_step1 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step1 += ' -n _' + scenario + '_maskSRs' # name tag
    command_step1 += ' -m 125' # Higgs mass
    command_step1 += ' -v 1' # level of verbosity for output
    command_step1 += ' --algo=saturated' # algorithm
    command_step1 += ' --freezeParameters r --setParameters r=0' # freeze and set signal strength modifier to 0
    command_step1 += ' --toysFrequentist --bypassFrequentistFit' # use Frequentist toys
    command_step1 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
    command_step1 += ' --setParametersForFit '
    for mask in masks:
        if 'SR' in mask:
            command_step1 += mask + '=1,' # mask SRs
        # else:
        #     command_step1 += mask + '=0,'
    command_step1 = command_step1[:-1] # remove last comma
    command_step1 += ' --setParametersForEval '
    for mask in masks:
        command_step1 += mask + '=0,' # but evaluate everywhere
    command_step1 = command_step1[:-1] # remove last comma
    print(command_step1)
    log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
    log_file1 = 'goodnessoffit_data_SRmasked_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file1, 'w') as file:
        file.write(log_step1.stdout.decode())

    print('fit on toys...')
    command_step2 = 'combine -M GoodnessOfFit' # method
    command_step2 += ' -d ../../asymptoticlimits/workspace_' + year_to_run + '_fa' + fa + '_' + scenario + '.root' # workspace
    command_step2 += ' -n _' + scenario + '_maskSRs' # name tag
    command_step2 += ' -m 125' # Higgs mass
    command_step2 += ' -v 1' # level of verbosity for output
    command_step2 += ' --algo=saturated' # algorithm
    command_step2 += ' -t 250 -s 12345' # set number of toys and seed
    command_step2 += ' --freezeParameters r --setParameters r=0' # freeze and set signal strength modifier to 0
    command_step2 += ' --toysFrequentist --bypassFrequentistFit' # use Frequentist toys
    command_step2 += ' --setParameterRanges ttag_corr=-5,5' + ''.join(':ttag_uncorr_' + year + '=-5,5' for year in years)
    command_step2 += ' --setParametersForFit '
    for mask in masks:
        if 'SR' in mask:
            command_step2 += mask + '=1,' # mask SRs
    command_step2 = command_step2[:-1] # remove last comma
    command_step2 += ' --setParametersForEval '
    for mask in masks:
        command_step2 += mask + '=0,' # but evaluate everywhere
    command_step2 = command_step2[:-1] # remove last comma
    print(command_step2)
    log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
    log_file2 = 'goodnessoffit_toys_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file2, 'w') as file:
        file.write(log_step2.stdout.decode())

    print('collecting results...')
    command_step3 = 'combineTool.py -M CollectGoodnessOfFit' # method
    command_step3 += ' --input higgsCombine_' + scenario + '_maskSRs.GoodnessOfFit.mH125.root higgsCombine_' + scenario + '_maskSRs.GoodnessOfFit.mH125.12345.root' # inputs: data, toys
    command_step3 += ' -m 125.0' # Higgs mass
    command_step3 += ' -o gof_' + scenario + '.json'
    print(command_step3)
    log_step3 = subprocess.run(['bash', '-c', command_step3], capture_output=True)
    log_file3 = 'collect_gof_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file3, 'w') as file:
        file.write(log_step3.stdout.decode())

    print('plotting...')
    command_step4 = 'plotGof.py' # method
    command_step4 += ' gof_' + scenario + '.json'
    command_step4 += ' --statistic saturated' # algorithm
    command_step4 += ' --mass 125.0' # Higgs mass
    command_step4 += ' -o gof_plot_' + scenario
    command_step4 += ' --title-right="' + scenario + '"'
    print(command_step4)
    log_step4 = subprocess.run(['bash', '-c', command_step4], capture_output=True)
    log_file4 = 'plot_gof_' + year_to_run + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file4, 'w') as file:
        file.write(log_step4.stdout.decode())

    os.chdir('..')
