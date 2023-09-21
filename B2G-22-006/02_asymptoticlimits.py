#!/usr/bin/env python3

import subprocess
import os
from collections import OrderedDict

year = 'run2'

fas = [
    '750',
    '1000',
    '1250',
    '1500',
    '1750',
    '2000',
    '2500',
    '3000',
    '10000',
]

scenarios = [
    'negint',
    'posint',
]

cwd = os.getcwd() + '/'

asymptoticlimits_dir_name = 'asymptoticlimits/'
if not os.path.exists(asymptoticlimits_dir_name):
    os.mkdir(asymptoticlimits_dir_name)

asymptoticlimits_log_dir_name = asymptoticlimits_dir_name + 'log/'
if not os.path.exists(asymptoticlimits_log_dir_name):
    os.mkdir(asymptoticlimits_log_dir_name)


print(year)

for scenario in scenarios:
    print(scenario)

    observed = ''
    expected2p5 = ''
    expected16p0 = ''
    expected50p0 = ''
    expected84p0 = ''
    expected97p5 = ''
    for fa in fas:
        print(fa)

        # write fas (x-axis)
        fa_file_name = asymptoticlimits_dir_name + '/fa_' + year + '.txt'
        if fa == fas[0]:
            if os.path.exists(fa_file_name):
                os.remove(fa_file_name)
        mode = 'a' if os.path.exists(fa_file_name) else 'w'
        with open(fa_file_name, mode) as fa_file:
            fa_file.write(fa + '\n')

        # step 1: text2workspace
        command_step1 = 'python3 ../scripts/text2workspace.py ' # text2workspace command
        command_step1 += 'datacards/datacard_' + year + '_fa' + fa + '.txt' # datacard
        command_step1 += ' -P HiggsAnalysis.CombinedLimit.ALPtoTTbar_' + scenario + ':alptottbar_' + scenario # physics model
        command_step1 += ' -m 125' # higgs mass
        command_step1 += ' -o ' + asymptoticlimits_dir_name + 'workspace_' + year + '_fa' + fa + '_' + scenario + '.root' # workspace
        command_step1 += ' --channel-masks' # to mask channels
        # print(command_step1)
        log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
        with open(asymptoticlimits_log_dir_name + '/text2workspace_' + year + '_fa' + fa + '_' + scenario + '.log', 'w') as log_file:
            log_file.write(log_step1.stdout.decode())

        # step 2: AsymptoticLimits
        command_step2 = 'combine -v3 -M AsymptoticLimits ' # method
        command_step2 += asymptoticlimits_dir_name + 'workspace_' + year + '_fa' + fa + '_' + scenario + '.root' # workspace
        command_step2 += ' --setParameterRanges ttag_corr=-5,5:ttag_uncorr_' + year + '=-5,5' # set parameter ranges for shapeU NPs: 1 (too small, at boundary)
        command_step2 += ' --run blind' # option to run blinded
        # print(command_step2)
        log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
        with open(asymptoticlimits_log_dir_name + '/asymptoticlimits_' + year + '_fa' + fa + '_' + scenario + '.log', 'w') as log_file:
            log_file.write(log_step2.stdout.decode())

        # extract limits
        with open(asymptoticlimits_log_dir_name + '/asymptoticlimits_' + year + '_fa' + fa + '_' + scenario + '.log', 'r') as log_file:
            for line in log_file:
                if line.startswith('Observed Limit: r < '):
                    value = line.replace('Observed Limit: r < ', '')
                    observed += value
                elif line.startswith('Expected  2.5%: r < '):
                    value = line.replace('Expected  2.5%: r < ', '')
                    expected2p5 += value
                elif line.startswith('Expected 16.0%: r < '):
                    value = line.replace('Expected 16.0%: r < ', '')
                    expected16p0 += value
                elif line.startswith('Expected 50.0%: r < '):
                    value = line.replace('Expected 50.0%: r < ', '')
                    expected50p0 += value
                elif line.startswith('Expected 84.0%: r < '):
                    value = line.replace('Expected 84.0%: r < ', '')
                    expected84p0 += value
                elif line.startswith('Expected 97.5%: r < '):
                    value = line.replace('Expected 97.5%: r < ', '')
                    expected97p5 += value

    with open(asymptoticlimits_dir_name + 'limit_observed_' + year + '_' + scenario + '.txt', 'w') as observed_file: observed_file.write(observed)
    with open(asymptoticlimits_dir_name + 'limit_expected2p5_' + year + '_' + scenario + '.txt', 'w') as expected2p5_file: expected2p5_file.write(expected2p5)
    with open(asymptoticlimits_dir_name + 'limit_expected16p0_' + year + '_' + scenario + '.txt', 'w') as expected16p0_file: expected16p0_file.write(expected16p0)
    with open(asymptoticlimits_dir_name + 'limit_expected50p0_' + year + '_' + scenario + '.txt', 'w') as expected50p0_file: expected50p0_file.write(expected50p0)
    with open(asymptoticlimits_dir_name + 'limit_expected84p0_' + year + '_' + scenario + '.txt', 'w') as expected84p0_file: expected84p0_file.write(expected84p0)
    with open(asymptoticlimits_dir_name + 'limit_expected97p5_' + year + '_' + scenario + '.txt', 'w') as expected97p5_file: expected97p5_file.write(expected97p5)
