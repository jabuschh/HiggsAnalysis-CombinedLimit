#!/usr/bin/env python3

import subprocess
import os

fa = '10000'
year = 'run2'

scenarios = [
    'negint',
    'posint'
]

dir_name = 'sanitycheckdatacard/'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

print('sanity checking the datacard...')
command_step1 = 'python3 ../test/systematicsAnalyzer.py datacards/datacard_' + year + '_fa' + fa + '.txt > ' + dir_name + 'sanitycheck_' + year + '_fa' + fa + '.html'
log_step1 = subprocess.run(['bash', '-c', command_step1], capture_output=True)
log_file1 = dir_name + 'sanitycheck_' + year + '_fa' + fa + '.log'
with open(log_file1, 'w') as file:
    file.write(log_step1.stdout.decode())

for scenario in scenarios:
    print('writing workspace normalizations: ' + scenario + '...')
    command_step2 = 'python3 ../test/printWorkspaceNormalisations.py asymptoticlimits/workspace_' + year + '_fa' + fa + '_' + scenario + '.root'
    log_step2 = subprocess.run(['bash', '-c', command_step2], capture_output=True)
    log_file2 = dir_name + 'workspacenormalization_' + year + '_fa' + fa + '_' + scenario + '.log'
    with open(log_file2, 'w') as file:
        file.write(log_step2.stdout.decode())
