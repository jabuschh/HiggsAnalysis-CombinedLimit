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
    fas_recast = np.loadtxt('../TOP-20-001/cts_mtt/asymptoticlimits/fa_' + year + '.txt', delimiter='\n')
    fas_recast /= 1000. # scale fa from GeV to TeV

    # y-axis: limits on poi
    limit_exp2p5 = np.loadtxt('asymptoticlimits/limit_expected2p5_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp16p0 = np.loadtxt('asymptoticlimits/limit_expected16p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp50p0 = np.loadtxt('asymptoticlimits/limit_expected50p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp84p0 = np.loadtxt('asymptoticlimits/limit_expected84p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp97p5 = np.loadtxt('asymptoticlimits/limit_expected97p5_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_exp_recast = np.loadtxt('../TOP-20-001/cts_mtt/asymptoticlimits/limit_expected50p0_' + year + '_' + scenario + '.txt', delimiter='\n')
    limit_obs_recast = np.loadtxt('../TOP-20-001/cts_mtt/asymptoticlimits/limit_observed_' + year + '_' + scenario + '.txt', delimiter='\n')

    # scale from poi to WC
    for limit in [limit_exp2p5, limit_exp16p0, limit_exp50p0, limit_exp84p0, limit_exp97p5]:
        limit *= np.square(fas)
    for limit in [limit_exp_recast, limit_obs_recast]:
        limit *= np.square(fas_recast)


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


    # analysis
    graph_search_exp = root.TGraph(len(fas), fas, limit_exp50p0)
    graph_search_exp.SetLineColor(root.kBlack)
    graph_search_exp.SetLineStyle(2)
    graph_search_exp.SetLineWidth(2)
    # graph_search_exp.SetMarkerStyle(8)
    # graph_search_exp.SetMarkerColor(root.kBlack)

    graph_2s = root.TGraphAsymmErrors(len(fas), fas, limit_exp50p0, np.zeros(len(fas)), np.zeros(len(fas)), limit_exp50p0-limit_exp2p5, limit_exp97p5-limit_exp50p0)
    graph_2s.SetFillColor(root.kOrange)
    graph_2s.SetLineColor(root.kOrange)
    graph_1s = root.TGraphAsymmErrors(len(fas), fas, limit_exp50p0, np.zeros(len(fas)), np.zeros(len(fas)), limit_exp50p0-limit_exp16p0, limit_exp84p0-limit_exp50p0)
    graph_1s.SetFillColor(root.kGreen+1)
    graph_1s.SetLineColor(root.kGreen+1)

    # recast
    graph_recast_exp = root.TGraph(len(fas_recast), fas_recast, limit_exp_recast)
    graph_recast_exp.SetLineColor(root.kBlue)
    graph_recast_exp.SetLineStyle(2)
    graph_recast_exp.SetLineWidth(2)
    # graph_recast_exp.SetMarkerStyle(8)
    # graph_recast_exp.SetMarkerColor(root.kBlue)

    graph_recast_obs = root.TGraphAsymmErrors(len(fas_recast), fas_recast, limit_obs_recast, np.zeros(len(fas_recast)), np.zeros(len(fas_recast)), np.zeros(len(fas_recast)), np.full(len(fas_recast), 10000.))
    graph_recast_obs.SetLineColorAlpha(root.kBlue, 1.)
    graph_recast_obs.SetFillColorAlpha(root.kBlue, 0.5)
    graph_recast_obs.SetLineStyle(1)
    graph_recast_obs.SetLineWidth(2)
    # graph_recast_obs.SetMarkerStyle(8)
    # graph_recast_obs.SetMarkerColor(root.kBlue)



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
    legend = root.TLegend(canvas_margin_l + 0.38, canvas_margin_l + 0.55, 1. - canvas_margin_r - 0.05, 1. - canvas_margin_t - 0.04)
    if scenario == 'negint':
        legend.SetHeader('#bf{negative ALP-SM interference}', 'C')
    else:
        legend.SetHeader('#bf{positive ALP-SM interference}', 'C')
    legend.AddEntry(graph_search_exp, 'Expected 95% CL upper limit', 'l')
    legend.AddEntry(graph_1s, 'Expected #pm 1#sigma', 'fl')
    legend.AddEntry(graph_2s, 'Expected #pm 2#sigma', 'fl')
    legend.AddEntry(graph_recast_exp, 'Expected (PRD 104, 092013)', 'l')
    legend.AddEntry(graph_recast_obs, 'Observed (PRD 104, 092013)', 'fl')
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    # multigraph
    multigraph = root.TMultiGraph()
    multigraph.Draw('AL')
    multigraph.Add(graph_2s, '3AL')
    multigraph.Add(graph_1s, 'SAME 3AL')
    multigraph.Add(graph_search_exp, 'SAME AL')
    multigraph.Add(graph_recast_exp, 'SAME AL')
    multigraph.Add(graph_recast_obs, 'SAME 3AL')
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
    y_axis.SetRangeUser(0.2, 900.)

    canvas.RedrawAxis()
    canvas.Update()
    canvas.SaveAs(dir_name + 'limits_' + year + '_' + scenario + '_region.pdf')
    # canvas.Delete()
