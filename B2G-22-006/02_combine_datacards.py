#!/usr/bin/env python3

import subprocess
import os

cwd = os.getcwd() + '/'

script_path = "python3 ../scripts/combineCards.py"

years = [
    'UL16preVFP',
    'UL16postVFP',
    'UL17',
    'UL18',
]

fas = [
    # '500',
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


print('combining datacards for...')
# individual years
for year in years:
    print(year)
    for fa in fas:
        cards = year + '_el=datacards/datacard_' + year + '_electron_fa' + fa + '.txt ' # electron channel
        cards += year + '_mu=datacards/datacard_' + year + '_muon_fa' + fa + '.txt ' # muon channel
        cards += '> datacards/datacard_' + year + '_fa' + fa + '.txt' # combined datacard
        command = script_path + ' ' + cards
        # print(command)
        result = subprocess.run(['bash', '-c', command], capture_output=True)
        # print(result.stdout.decode())

# full run2
print('run2')
for fa in fas:
    cards = ''
    for year in years:
        cards += year + '_el=datacards/datacard_' + year + '_electron_fa' + fa + '.txt ' # electron channel
        cards += year + '_mu=datacards/datacard_' + year + '_muon_fa' + fa + '.txt ' # muon channel

    cards += '> '
    cards += 'datacards/datacard_run2_fa' + fa + '.txt' # combined datacard
    command = script_path + ' ' + cards
    # print(command)
    result = subprocess.run(['bash', '-c', command], capture_output=True)
    # print(result.stdout.decode())

print('...done!')
