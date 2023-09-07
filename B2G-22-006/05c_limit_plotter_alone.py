#!/usr/bin/env python3

import sys
sys.argv.append('-b') # for root in batch mode
import ROOT as root
import numpy as np
import matplotlib.pyplot as plt
import os
from constants import _YEARS


year = 'run2'
scenarios = [
    'negint',
    'posint'
]

dir_name = 'limits/'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)


for scenario in scenarios:

    # x-axis: f_a
    fas = np.loadtxt('asymptoticlimits/fa_' + year + '.txt', delimiter='\n')
    fas /= 1000. # scale fa from GeV to TeV

    # y-axis: limits on poi
    limit_exp2p5 = np.loadtxt('asymptoticlimits/limit_expected2p5_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp16p0 = np.loadtxt('asymptoticlimits/limit_expected16p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp50p0 = np.loadtxt('asymptoticlimits/limit_expected50p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp84p0 = np.loadtxt('asymptoticlimits/limit_expected84p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp97p5 = np.loadtxt('asymptoticlimits/limit_expected97p5_' + year + '_' + scenario + '.txt', delimiter='\n')
    # limit_obs = np.loadtxt('asymptoticlimits/limit_observed_' + year + '_' + scenario + '.txt', delimiter='\n')

    # scale from poi to WC
    for limit in [limit_exp2p5, limit_exp16p0, limit_exp50p0, limit_exp84p0, limit_exp97p5]: # limit_obs
        limit *= np.square(fas)

    # settings
    canvas_height = 600
    canvas_width = 600
    canvas_margin_l = 0.15
    canvas_margin_r = 0.05
    canvas_margin_t = 0.08
    canvas_margin_b = 0.12

    # canvas
    root.gROOT.SetBatch(True)
    canvas = root.TCanvas(scenario, scenario, canvas_height, canvas_width)
    canvas.Draw()
    canvas.SetLeftMargin(canvas_margin_l)
    canvas.SetRightMargin(canvas_margin_r)
    canvas.SetTopMargin(canvas_margin_t)
    canvas.SetBottomMargin(canvas_margin_b)
    canvas.SetTicks()
    canvas.SetLogy()
    canvas.cd()


    # recast
    graph_exp = root.TGraph(len(fas), fas, limit_exp50p0)
    graph_exp.SetLineColor(root.kBlack)
    graph_exp.SetLineStyle(2)
    graph_exp.SetLineWidth(2)

    # graph_obs = root.TGraph(len(fas), fas, limit_obs)
    # graph_obs.SetLineColor(root.kBlack)
    # graph_obs.SetLineStyle(1)
    # graph_obs.SetLineWidth(2)

    graph_2s = root.TGraphAsymmErrors(len(fas), fas, limit_exp50p0, np.zeros(len(fas)), np.zeros(len(fas)), limit_exp50p0-limit_exp2p5, limit_exp97p5-limit_exp50p0)
    graph_2s.SetFillColor(root.kOrange)
    graph_2s.SetLineWidth(0)
    graph_1s = root.TGraphAsymmErrors(len(fas), fas, limit_exp50p0, np.zeros(len(fas)), np.zeros(len(fas)), limit_exp50p0-limit_exp16p0, limit_exp84p0-limit_exp50p0)
    graph_1s.SetFillColor(root.kGreen+1)
    graph_1s.SetLineWidth(0)


    # cms logo
    tlatex_cms = root.TLatex(canvas_margin_l + 0.04, 1. - canvas_margin_t - 0.04, 'CMS')
    tlatex_cms.SetTextAlign(13) # left top
    tlatex_cms.SetTextFont(62)
    tlatex_cms.SetTextSize(0.05)
    tlatex_cms.SetNDC()
    # top left text
    tlatex_top_left = root.TLatex(canvas_margin_l, 1. - canvas_margin_t + 0.01, 'Run2')
    tlatex_top_left.SetTextAlign(11) # left bottom
    tlatex_top_left.SetTextFont(42)
    tlatex_top_left.SetTextSize(0.035)
    tlatex_top_left.SetNDC()
    # top right text
    tlatex_top_right = root.TLatex(1. - canvas_margin_r, 1. - canvas_margin_t + 0.01, _YEARS.get('Run2').get('lumi_fb_display') + ' fb^{#minus1} (13 TeV)',)
    tlatex_top_right.SetTextAlign(31) # right bottom
    tlatex_top_right.SetTextFont(42)
    tlatex_top_right.SetTextSize(0.035)
    tlatex_top_right.SetNDC()
    # prelim text
    tlatex_prelim = root.TLatex(canvas_margin_l + 0.04, 1. - canvas_margin_t - 0.1, 'Private Work')
    tlatex_prelim.SetTextAlign(13)
    tlatex_prelim.SetTextFont(52)
    tlatex_prelim.SetTextSize(0.035)
    tlatex_prelim.SetNDC()
    # legend
    legend = root.TLegend(canvas_margin_l + 0.04, canvas_margin_b + 0.40, 1. - canvas_margin_r - 0.49, 1. - canvas_margin_t - 0.17)
    if scenario == 'negint':
        legend.SetHeader('#bf{negative ALP-SM interference}')
    else:
        legend.SetHeader('#bf{positive ALP-SM interference}')
    legend.AddEntry(graph_exp, 'Expected 95% CL upper limit (PRD 104, 092013)', 'l')
    legend.AddEntry(graph_1s, 'Expected #pm 1#sigma (PRD 104, 092013)', 'fl')
    legend.AddEntry(graph_2s, 'Expected #pm 2#sigma (PRD 104, 092013)', 'fl')
    # legend.AddEntry(graph_obs, 'Observed (PRD 104, 092013)', 'l')
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    # multigraph
    multigraph = root.TMultiGraph()
    multigraph.Draw('AL')
    multigraph.Add(graph_2s, 'SAME 3A')
    multigraph.Add(graph_1s, 'SAME 3A')
    multigraph.Add(graph_exp, 'SAME AL')
    # multigraph.Add(graph_obs, 'SAME AL')
    tlatex_cms.Draw()
    tlatex_top_left.Draw()
    tlatex_top_right.Draw()
    tlatex_prelim.Draw()
    legend.Draw()

    x_axis = multigraph.GetXaxis()
    y_axis = multigraph.GetYaxis()
    x_axis.SetTitle('f_{a} [TeV]')
    if scenario == 'negint':
        y_axis.SetTitle('c_{#tilde{G}} c_{#tilde{#Phi}}')
    else:
        y_axis.SetTitle('#minus c_{#tilde{G}} c_{#tilde{#Phi}}')
    x_axis.SetTitleOffset(1.3)
    y_axis.SetTitleOffset(1.6)
    x_axis.SetLimits(0.1, 10.5)
    y_axis.SetRangeUser(0.2, 9000.)

    canvas.RedrawAxis()
    canvas.Update()
    canvas.SaveAs(dir_name + 'limits_' + year + '_' + scenario + '_alone.pdf')
    # canvas.Delete()
