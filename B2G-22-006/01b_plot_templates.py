#!/usr/bin/env python3

import sys
sys.argv.append('-b') # for root in batch mode
import ROOT as root
import os

cwd = os.getcwd() + '/'
templates_dir_name = cwd + 'templates/'
if not os.path.exists(templates_dir_name):
    os.mkdir(templates_dir_name)

processes = [
    'TTbar',
    'ST',
    'WJets',
    'others',
    'ALP_ttbar_signal',
    'ALP_ttbar_interference',
]
regions = [
    'SR_bin1_TopTag',
    'SR_bin1_NoTopTag',
    'SR_bin2_TopTag',
    'SR_bin2_NoTopTag',
    'SR_bin3_TopTag',
    'SR_bin3_NoTopTag',
    'SR_bin4',
    'SR_bin5',
    'SR_bin6',
    'CR1',
    'CR2',
]
systematics = [
    'pdf',
    'mcscale',
    'pu',
    'prefiring',
    'mu_id',
    'mu_iso',
    'mu_reco',
    'mu_trigger',
    'ele_id',
    'ele_reco',
    'ele_trigger',
    'btag_cferr1',
    'btag_cferr2',
    'btag_hf',
    'btag_hfstats1_UL16preVFP',
    'btag_hfstats1_UL16postVFP',
    'btag_hfstats1_UL17',
    'btag_hfstats1_UL18',
    'btag_hfstats2_UL16preVFP',
    'btag_hfstats2_UL16postVFP',
    'btag_hfstats2_UL17',
    'btag_hfstats2_UL18',
    'btag_lf',
    'btag_lfstats1_UL16preVFP',
    'btag_lfstats1_UL16postVFP',
    'btag_lfstats1_UL17',
    'btag_lfstats1_UL18',
    'btag_lfstats2_UL16preVFP',
    'btag_lfstats2_UL16postVFP',
    'btag_lfstats2_UL17',
    'btag_lfstats2_UL18',
    'ttag_corr',
    'ttag_uncorr_UL16preVFP',
    'ttag_uncorr_UL16postVFP',
    'ttag_uncorr_UL17',
    'ttag_uncorr_UL18',
    'tmistag',
    'jec',
    'jer',
]


filename_in = 'rootfiles/inputhists_run2_fa10000.root'
file_in = root.TFile(filename_in)

for systematic in systematics:
    # print(systematic)

    systematic_dir_name = templates_dir_name + systematic + '/'
    if not os.path.exists(systematic_dir_name):
        os.mkdir(systematic_dir_name)


    for process in processes:
        # print(process)

        for region in regions:
            # print(region)

            # standard
            hist_nominal = file_in.Get('M_Zprime_' + region + '_' + process)
            hist_nominal.SetTitle('')
            hist_nominal.SetLineColor(root.kBlack)
            hist_nominal.SetLineWidth(2)
            hist_nominal.SetMarkerSize(0)
            hist_nominal.SetMarkerColor(root.kBlack)
            hist_up = file_in.Get('M_Zprime_' + region + '_' + process + '_' + systematic + 'Up')
            hist_up.SetTitle('')
            hist_up.SetLineColor(root.kRed)
            hist_up.SetLineWidth(2)
            hist_up.SetMarkerSize(0)
            hist_up.SetMarkerColor(root.kRed)
            hist_down = file_in.Get('M_Zprime_' + region + '_' + process + '_' + systematic + 'Down')
            hist_down.SetTitle('')
            hist_down.SetLineColor(root.kBlue)
            hist_down.SetLineWidth(2)
            hist_down.SetMarkerSize(0)
            hist_down.SetMarkerColor(root.kBlue)
            # ratio
            hist_nominal_ratio = hist_nominal.Clone()
            hist_nominal_ratio.Divide(hist_nominal_ratio)
            hist_up_ratio = hist_up.Clone()
            hist_up_ratio.Divide(hist_nominal)
            hist_down_ratio = hist_down.Clone()
            hist_down_ratio.Divide(hist_nominal)

            # settings
            canvas_height = 600
            canvas_width = 600
            canvas_margin_l = 0.15
            canvas_margin_r = 0.05
            canvas_margin_t = 0.08
            canvas_margin_b = 0.12
            border_y = 0.28
            border_width = 0.03
            text_size = 0.035
            tick_length = 0.015
            x_axis_title = 'm(t#bar{t}) [GeV]'
            y_axis_title = 'Events / bin'
            # canvas
            root.gROOT.SetBatch(True)
            # root.gStyle.SetOptTitle(False)
            canvas = root.TCanvas('canvas', 'canvas', canvas_height, canvas_width)
            canvas.cd()
            pad_main = root.TPad('pad_main', 'main pad title', 0, border_y, 1, 1)
            pad_main.SetTopMargin(canvas_margin_t / (1. - border_y))
            pad_main.SetBottomMargin(0.5 * border_width / (1. - border_y))
            pad_main.Draw()
            pad_ratio = root.TPad('pad_ratio', 'ratio pad title', 0, 0, 1, border_y)
            pad_ratio.SetTopMargin(0.5 * border_width / border_y)
            pad_ratio.SetBottomMargin(canvas_margin_b / border_y)
            pad_ratio.Draw()
            for pad in [pad_main, pad_ratio]:
                pad.SetLeftMargin(canvas_margin_l)
                pad.SetRightMargin(canvas_margin_r)
                pad.SetTickx(1)
                pad.SetTicky(1)

            # main pad
            pad_main.cd()
            pad_main.SetLogy()
            hist_nominal.Draw('hist')
            hist_up.Draw('hist same')
            hist_down.Draw('hist same')
            # cosmetics
            hist_nominal.GetYaxis().SetTitle(y_axis_title)
            hist_nominal.GetYaxis().SetTitleSize(text_size / (1. - border_y))
            hist_nominal.GetYaxis().SetLabelSize(text_size / (1. - border_y))
            hist_nominal.GetYaxis().SetLabelOffset(0.01)
            hist_nominal.GetXaxis().SetLabelOffset(999) # hack: let x axis title/labels vanish under pad_ratio
            hist_nominal.GetXaxis().SetTitle('')
            pad_main.Update()
            tickScaleX = (pad_main.GetUxmax() - pad_main.GetUxmin()) / (pad_main.GetX2() - pad_main.GetX1()) * (pad_main.GetWh() * pad_main.GetAbsHNDC())
            tickScaleY = (pad_main.GetUymax() - pad_main.GetUymin()) / (pad_main.GetY2() - pad_main.GetY1()) * (pad_main.GetWw() * pad_main.GetAbsWNDC())
            hist_nominal.GetXaxis().SetTickLength(canvas.GetWh() * tick_length / tickScaleX)
            hist_nominal.GetYaxis().SetTickLength(canvas.GetWw() * tick_length / tickScaleY)
            hist_nominal.SetStats(0)
            root.gPad.Update()
            root.gPad.RedrawAxis()

            # ratio pad
            pad_ratio.cd()
            hist_up_ratio.Draw('hist')
            hist_down_ratio.Draw('hist same')
            # cosmetics
            hist_up_ratio.GetXaxis().SetLabelSize(text_size / border_y)
            # hist_up_ratio.GetXaxis().SetLabelOffset(20. / hist_up_ratio.GetXaxis().GetLabelOffset())
            hist_up_ratio.GetXaxis().SetTitleSize(text_size / border_y)
            hist_up_ratio.GetXaxis().SetTitle(x_axis_title)
            hist_up_ratio.GetXaxis().SetTitleOffset(1.3)
            hist_up_ratio.GetXaxis().SetNdivisions(hist_up_ratio.GetXaxis().GetNdivisions())
            hist_up_ratio.GetYaxis().SetTitle('var. / nom.')
            hist_up_ratio.GetYaxis().SetLabelSize(text_size / border_y)
            hist_up_ratio.GetYaxis().SetLabelOffset(0.01)
            hist_up_ratio.GetYaxis().SetTitleSize(text_size / border_y)
            hist_up_ratio.GetYaxis().SetTitleOffset(0.45)
            hist_up_ratio.GetYaxis().CenterTitle()
            hist_up_ratio.SetMinimum(0.3)
            hist_up_ratio.SetMaximum(1.7)
            hist_up_ratio.GetYaxis().SetNdivisions(503)
            pad_ratio.Update()
            tickScaleX = (pad_ratio.GetUxmax() - pad_ratio.GetUxmin()) / (pad_ratio.GetX2() - pad_ratio.GetX1()) * (pad_ratio.GetWh() * pad_ratio.GetAbsHNDC())
            tickScaleY = (pad_ratio.GetUymax() - pad_ratio.GetUymin()) / (pad_ratio.GetY2() - pad_ratio.GetY1()) * (pad_ratio.GetWw() * pad_ratio.GetAbsWNDC())
            hist_up_ratio.GetXaxis().SetTickLength(canvas.GetWh() * tick_length / tickScaleX)
            hist_up_ratio.GetYaxis().SetTickLength(canvas.GetWw() * tick_length / tickScaleY)
            hist_up_ratio.SetStats(0)
            ratio_line = root.TLine(hist_up_ratio.GetXaxis().GetXmin(), 1., hist_up_ratio.GetXaxis().GetXmax(), 1.)
            ratio_line.SetLineStyle(2)
            ratio_line.Draw()

            # text top left
            canvas.cd()
            tlatex_top_left = root.TLatex(canvas_margin_l, 1. - canvas_margin_t + 0.01, '#bf{' + region + ': ' + process + '}')
            tlatex_top_left.SetTextAlign(11) # left bottom
            tlatex_top_left.SetTextFont(42)
            tlatex_top_left.SetTextSize(0.020)
            tlatex_top_left.SetNDC()
            tlatex_top_left.Draw()
            # text top right
            tlatex_top_right = root.TLatex(1. - canvas_margin_r, 1. - canvas_margin_t + 0.01, '138 fb^{#minus1} (13 TeV)')
            tlatex_top_right.SetTextAlign(31) # right bottom
            tlatex_top_right.SetTextFont(42)
            tlatex_top_right.SetTextSize(text_size)
            tlatex_top_right.SetNDC()
            tlatex_top_right.Draw()
            # legend
            legend = root.TLegend(0.75,0.75,0.95,0.85)
            legend.SetHeader(systematic)
            legend.AddEntry(hist_up, 'up')
            legend.AddEntry(hist_nominal, 'nominal')
            legend.AddEntry(hist_down, 'down')
            legend.SetTextSize(0.025)
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)
            legend.Draw()


            canvas.SaveAs(systematic_dir_name + 'mtt_' + region + '_' + process + '_' + systematic + '.pdf')
            canvas.Close()
