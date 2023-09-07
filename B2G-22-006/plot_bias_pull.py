#!/usr/bin/env python3

import ROOT, argparse
import numpy as np

ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest='input', type=str)
parser.add_argument("-o", dest='output', type=str)
parser.add_argument("-t", dest='n_toys', type=int)
parser.add_argument("-r", dest='r_inj', type=float)
args = parser.parse_args()

print(args)

input = args.input
output = args.output
n_toys = args.n_toys
r_inj = args.r_inj

# Open file with fits
f = ROOT.TFile(input)
t_limit = f.Get("limit")
t_fit_sb = f.Get("tree_fit_sb")

if t_limit==None and t_fit_sb==None:
    raise ValueError('None of the methods works')
if t_limit!=None and t_fit_sb!=None:
    raise ValueError('Both methods worked. Undefined behaviour')

hist_pull = ROOT.TH1F("pull", "Pull distribution", 40, -4, 4)
hist_pull.GetXaxis().SetTitle("(r_{fit}-r_{inj})/#sigma_{fit}")
hist_pull.GetYaxis().SetTitle("Toys")

sigma_values = np.array([])

if t_fit_sb!=None:
    for entry in t_fit_sb:
        if entry.fit_status!=0: continue

        r_fit = entry.r
        # if r_fit<-4: continue
        sigma = entry.rErr
        diff = r_fit-r_inj
        if sigma != 0:
            sigma_values = np.append(sigma_values, sigma )
        else:
            sigma = sigma_values.mean()
        if sigma != 0:
            hist_pull.Fill( diff/sigma )
        # else:
        #     hist_pull.Fill(-0.1)

if t_limit!=None:
    for i_toy in range( n_toys ):
        # Best-fit value
        t_limit.GetEntry(i_toy*3)
        r_fit = getattr(t_limit, "r")
        print('r_fit: ' + str(r_fit))

        # -1 sigma value
        t_limit.GetEntry(i_toy*3+1)
        r_lo = getattr(t_limit, "r")
        print('r_lo: ' + str(r_lo))

        # +1 sigma value
        t_limit.GetEntry(i_toy*3+2)
        r_hi = getattr(t_limit, "r")
        print('r_hi: ' + str(r_hi))

        diff = r_inj-r_fit

        # Use uncertainty depending on where mu_truth is relative to mu_fit
        if diff > 0: sigma = abs(r_hi-r_fit)
        else: sigma = abs(r_lo-r_fit)

        if sigma != 0:
            sigma_values = np.append( sigma_values , sigma )
        else:
            sigma = sigma_values.mean()

        hist_pull.Fill( diff/sigma if sigma != 0 else -10)

canv = ROOT.TCanvas()
hist_pull.Draw()

# Fit Gaussian to pull distribution
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(111)
fit_result = hist_pull.Fit("gaus", "QMS+", "", -3, 3)

canv.SaveAs(f'pull_{output}.pdf')

with open(f'pull_{output}.txt', 'w') as f_:
    f_.write( f'mean={str(round(fit_result.Parameter(1),3))}+-{str(round(fit_result.Error(1),3))}\n')
    f_.write(f'sigma={str(round(fit_result.Parameter(2),3))}+-{str(round(fit_result.Error(2),3))}\n')
