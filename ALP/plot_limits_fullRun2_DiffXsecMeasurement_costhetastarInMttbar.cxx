{
  // TOP-20-001: mttbar only
  vector<double> fa_mttbar = {0.48,0.56,0.64,0.72,0.8,0.9,1.0,1.3,1.15,1.5,1.7,2.0,2.3,3.5};
  vector<vector<double>> v_mttbar = readIn_expected(
    "../ALP_TOP20001_converted_mttbar/limits_exp_fullRun2.txt",
    fa_mttbar,
    true
  );
  //
  // // TOP-20-001: cos(theta*) only
  // vector<double> fa_costhetastar = {3.5};
  // vector<vector<double>> v_costhetastar = readIn_expected(
  //   "database/ALPtoTTbar_DiffXsecMeasurement_fullRun2_costhetastar/limits_exp.txt",
  //   fa_costhetastar,
  //   true
  // );

  // TOP-20-001: cos(theta*) in 6 bins of mttbar
  vector<double> fa_costhetastarInMttbar = {0.42,0.52,0.62,0.8,1.0,3.5};
  vector<vector<double>> v_costhetastarInMttbar = readIn_expected(
    "../ALP_TOP20001_converted_costhetastarMttbar/limits_exp_fullRun2.txt",
    // "database/ALPtoTTbar_DiffXsecMeasurement_fullRun2_costhetastarInMttbar/limits_exp.txt",
    fa_costhetastarInMttbar,
    true
  );

  // our search: mttbar in 4 bins of cos(theta*) after DNN
  // vector<double> fa_mttbarInCosthetastar = {0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.4,4.8,5.2,5.6,6.0,6.1};
  vector<double> fa_mttbarInCosthetastar = {0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0,3.2,3.4,3.6,3.8,4.0,4.4,4.8,5.2,5.6,6.0,6.1};
  vector<vector<double>> v_mttbarInCosthetastar = readIn_expected(
    "limits_exp_fullRun2.txt",
    // "limits_exp_fullRun2_modified.txt",
    fa_mttbarInCosthetastar,
    true
  );


  // // our search: mttbar after full selection
  // vector<double> fa_afterFullSel_mttbar = {0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.5,3.0,3.5,4.0,5.0};
  // vector<vector<double>> v_afterFullSel_mttbar = readIn_expected(
  //   "database/ALPtoTTbar_fullRun2_afterFullSel_mttbar/limits_exp.txt",
  //   fa_afterFullSel_mttbar,
  //   true
  // );


  // // our search: UL18 muon + systematics
  // vector<double> fa_UL18_muon_withSyst = {1.0,2.0,3.0,4.0,6.0};
  // vector<vector<double>> v_UL18_muon_withSyst = readIn_expected(
  //   "database/ALP_UL18_muon_withSyst/limits_ALP_UL18_muon_withSyst.txt",
  //   fa_UL18_muon_withSyst,
  //   true
  // );
  //
  // // our search: UL18 muon without any systematics
  // vector<double> fa_UL18_muon_noSyst = {1.0,2.0,3.0,4.0,6.0};
  // vector<vector<double>> v_UL18_muon_noSyst = readIn_expected(
  //   "database/ALP_UL18_muon_noSyst/limits_ALP_UL18_muon_noSyst.txt",
  //   fa_UL18_muon_noSyst,
  //   true
  // );




  // plotting
  cout << "plotting..." << endl;
  TCanvas *c1 = new TCanvas("c1","c1",0,0,800,800);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(kFALSE);
  gPad->SetTopMargin(0.05);
  gPad->SetBottomMargin(0.10);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.05);
  gPad->SetLogy();
  gPad->SetTicks();

  auto multigraph = new TMultiGraph();
  multigraph->Draw("AL");


  auto gr_exp_mttbar = new TGraph(fa_mttbar.size(), &(fa_mttbar[0]), &(v_mttbar.at(2)[0]));
  gr_exp_mttbar->SetLineColor(kRed);
  gr_exp_mttbar->SetLineStyle(2);
  gr_exp_mttbar->SetLineWidth(2);
  gr_exp_mttbar->SetMarkerStyle(8);
  gr_exp_mttbar->SetMarkerColor(kRed);
  multigraph->Add(gr_exp_mttbar, "same lp");
  //
  // auto gr_exp_costhetastar = new TGraph(fa_costhetastar.size(), &(fa_costhetastar[0]), &(v_costhetastar.at(2)[0]));
  // gr_exp_costhetastar->SetLineColor(kBlue);
  // gr_exp_costhetastar->SetLineStyle(2);
  // gr_exp_costhetastar->SetLineWidth(2);
  // gr_exp_costhetastar->SetMarkerStyle(8);
  // gr_exp_costhetastar->SetMarkerColor(kBlue);
  // multigraph->Add(gr_exp_costhetastar, "same lp");

  auto gr_exp_costhetastarInMttbar = new TGraph(fa_costhetastarInMttbar.size(), &(fa_costhetastarInMttbar[0]), &(v_costhetastarInMttbar.at(2)[0]));
  gr_exp_costhetastarInMttbar->SetLineColor(kBlue);
  gr_exp_costhetastarInMttbar->SetLineStyle(2);
  gr_exp_costhetastarInMttbar->SetLineWidth(2);
  gr_exp_costhetastarInMttbar->SetMarkerStyle(8);
  gr_exp_costhetastarInMttbar->SetMarkerColor(kBlue);
  multigraph->Add(gr_exp_costhetastarInMttbar, "same lp");

  auto gr_exp_mttbarInCosthetastar = new TGraph(fa_mttbarInCosthetastar.size(), &(fa_mttbarInCosthetastar[0]), &(v_mttbarInCosthetastar.at(2)[0]));
  gr_exp_mttbarInCosthetastar->SetLineColor(kBlack);
  gr_exp_mttbarInCosthetastar->SetLineStyle(2);
  gr_exp_mttbarInCosthetastar->SetLineWidth(2);
  gr_exp_mttbarInCosthetastar->SetMarkerStyle(8);
  gr_exp_mttbarInCosthetastar->SetMarkerColor(kBlack);
  multigraph->Add(gr_exp_mttbarInCosthetastar, "same lp");

  // vector<double> Zero = fa_mttbarInCosthetastar = {0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0};
  // auto sigmaband1 = new TGraphAsymmErrors(fa_mttbarInCosthetastar.size(), &(fa_mttbarInCosthetastar[0]), &(v_mttbarInCosthetastar.at(2)[0]), &(v_mttbarInCosthetastar.at(0)[0]), &(v_mttbarInCosthetastar.at(4)[0]));
  // sigmaband1->SetFillColor(kOrange);
  // sigmaband1->Draw("a3");
  // multigraph->Add(sigmaband1,"3l ALP");

  // auto ge = new TGraphAsymmErrors(22, X, exp, Zero, Zero,oneD,oneU);
  // ge->SetFillColor(kGreen+1);
  // multigraph->Add(ge,"SAME 3l ALP");




  //
  // auto gr_exp_afterFullSel_mttbar = new TGraph(fa_afterFullSel_mttbar.size(), &(fa_afterFullSel_mttbar[0]), &(v_afterFullSel_mttbar.at(2)[0]));
  // gr_exp_afterFullSel_mttbar->SetLineColor(kGray);
  // gr_exp_afterFullSel_mttbar->SetLineStyle(2);
  // gr_exp_afterFullSel_mttbar->SetLineWidth(2);
  // gr_exp_afterFullSel_mttbar->SetMarkerStyle(8);
  // gr_exp_afterFullSel_mttbar->SetMarkerColor(kGray);
  // multigraph->Add(gr_exp_afterFullSel_mttbar, "same lp");

  // auto gr_exp_UL18_muon_withSyst = new TGraph(fa_UL18_muon_withSyst.size(), &(fa_UL18_muon_withSyst[0]), &(v_UL18_muon_withSyst.at(2)[0]));
  // gr_exp_UL18_muon_withSyst->SetLineColor(kBlack);
  // gr_exp_UL18_muon_withSyst->SetLineStyle(2);
  // gr_exp_UL18_muon_withSyst->SetLineWidth(2);
  // gr_exp_UL18_muon_withSyst->SetMarkerStyle(8);
  // gr_exp_UL18_muon_withSyst->SetMarkerColor(kBlack);
  // multigraph->Add(gr_exp_UL18_muon_withSyst, "same lp");
  //
  // auto gr_exp_UL18_muon_noSyst = new TGraph(fa_UL18_muon_noSyst.size(), &(fa_UL18_muon_noSyst[0]), &(v_UL18_muon_noSyst.at(2)[0]));
  // gr_exp_UL18_muon_noSyst->SetLineColor(kGray);
  // gr_exp_UL18_muon_noSyst->SetLineStyle(2);
  // gr_exp_UL18_muon_noSyst->SetLineWidth(2);
  // gr_exp_UL18_muon_noSyst->SetMarkerStyle(8);
  // gr_exp_UL18_muon_noSyst->SetMarkerColor(kGray);
  // multigraph->Add(gr_exp_UL18_muon_noSyst, "same lp");




  // x-axis
  double x_axis_lowerLimit = 0.3;
  double x_axis_upperLimit = 6.1;
  multigraph->GetXaxis()->SetTitle("f_{a} [TeV]");
  multigraph->GetXaxis()->SetTitleOffset(1.3);
  multigraph->GetXaxis()->SetLimits(x_axis_lowerLimit,x_axis_upperLimit);
  // y-axis
  double y_axis_lowerLimit = 0.01;
  double y_axis_upperLimit = 1000.;
  multigraph->GetYaxis()->SetTitle("|c_{#tilde{G}} c_{#tilde{#Phi}}|");
  // multigraph->GetYaxis()->SetTitle("#mu");
  multigraph->GetYaxis()->SetTitleOffset(1.5);
  multigraph->GetYaxis()->SetRangeUser(y_axis_lowerLimit,y_axis_upperLimit);

  // theoretical limit (red)
  TLine *theo_line;
  theo_line = new TLine (x_axis_lowerLimit,1.0,x_axis_upperLimit,1.0);
  theo_line->SetLineColor(kRed);
  theo_line->SetLineWidth(2);
  theo_line->Draw();


  plot_CMSTag();
  plot_subtext1("simulation");
  plot_subtext2("work in progress");
  plot_lumiTag("138 fb^{-1} (13 TeV)");
  // plot_channelTag("expected limits");
  // plot_lumiTag("36.3 fb^{-1} (13 TeV)");
  // plot_channelTag("UL18 muon channel");

  // legend
  x_pos = 0.9;
  y_pos = 0.90;
  double x_width = 0.3;
  double y_width = 0.1;
  TLegend *legend = new TLegend(x_pos-x_width, y_pos-y_width, x_pos, y_pos);
  legend->SetBorderSize(0);
  legend->SetFillStyle(0);
  // legend->SetHeader("expected limits (full Run2, no systematics)");
  legend->AddEntry(gr_exp_mttbar, "CMS-TOP-20-001: m(t#bar{t}) only","l");
  // legend->AddEntry(gr_exp_costhetastar, "CMS-TOP-20-001: cos(#theta*) only","l");
  legend->AddEntry(gr_exp_costhetastarInMttbar, "CMS-TOP-20-001: cos(#theta*) in bins of m(t#bar{t})","l");
  // legend->AddEntry(gr_exp_mttbarInCosthetastar, "our search: m_{t#bar{t}} in 4 cos(#theta*) bins (after DNN)","l");
  legend->AddEntry(gr_exp_mttbarInCosthetastar, "our search","l");
  // legend->AddEntry(gr_exp_afterFullSel_mttbar, "our search: m_{t#bar{t}} only (after full selection)","l");
  // legend->AddEntry(gr_exp_UL18_muon_withSyst, "with systematics","l");
  // legend->AddEntry(gr_exp_UL18_muon_noSyst, "no systematics","l");
  legend->Draw();

  gPad->RedrawAxis();

  c1->Print("Limits_fullRun2.pdf");
  // c1->Print("../plots/BrazilianLimits_cGcPhi_ALPtoTTbar_UL18_muon.pdf");
  // c1->Print("../plots/BrazilianLimits_mu_ALPtoTTbar_UL18_muon.pdf");
}




vector<vector<double>> readIn_expected(string input_file_str, vector<double> fa, bool limitsOnCGCPhi){
  cout << "reading in file: " << input_file_str << endl;
  std::fstream input_file(input_file_str,std::ios_base::in);

  int counter_lines = 0;
  double value_inCurrentLine;
  vector<double> v_2sigma_down, v_1sigma_down, v_expected, v_1sigma_up, v_2sigma_up;

  while(input_file >> value_inCurrentLine){
    counter_lines++;
    if(counter_lines % 5 == 1){v_2sigma_down.push_back(value_inCurrentLine);}
    if(counter_lines % 5 == 2){v_1sigma_down.push_back(value_inCurrentLine);}
    if(counter_lines % 5 == 3){v_expected.push_back(value_inCurrentLine);}
    if(counter_lines % 5 == 4){v_1sigma_up.push_back(value_inCurrentLine);}
    if(counter_lines % 5 == 0){v_2sigma_up.push_back(value_inCurrentLine);}
  }

  int N_fa = fa.size();
  int N_fa_fromInputFile = counter_lines / 5;
  if(N_fa != N_fa_fromInputFile) throw runtime_error("Number of values for fa does not match");

  if(limitsOnCGCPhi){
    for(int i=0; i<N_fa; i++){
      v_2sigma_down.at(i) = sqrt(v_2sigma_down.at(i)) * pow(fa.at(i),2);
      v_1sigma_down.at(i) = sqrt(v_1sigma_down.at(i)) * pow(fa.at(i),2);
      v_expected.at(i)    = sqrt(v_expected.at(i))    * pow(fa.at(i),2);
      v_1sigma_up.at(i)   = sqrt(v_1sigma_up.at(i))   * pow(fa.at(i),2);
      v_2sigma_up.at(i)   = sqrt(v_2sigma_up.at(i))   * pow(fa.at(i),2);
    }
  }

  vector<vector<double>> v;
  v.push_back(v_2sigma_down);
  v.push_back(v_1sigma_down);
  v.push_back(v_expected);
  v.push_back(v_1sigma_up);
  v.push_back(v_2sigma_up);

  return v;
}

void plot_CMSTag(){
  double x_pos = 0.15;
  double y_pos = 0.915;
  TString cmslogo_text = "CMS";
  TLatex *cmslogo = new TLatex(3.5, 24, cmslogo_text);
  cmslogo->SetX(x_pos);
  cmslogo->SetY(y_pos);
  cmslogo->SetNDC();
  cmslogo->SetTextAlign(13);
  cmslogo->SetTextFont(62);
  cmslogo->SetTextSize(0.05);
  cmslogo->Draw();
}

void plot_subtext1(TString text){
  double x_pos = 0.15;
  double y_pos = 0.87;
  TLatex *subtext1 = new TLatex(3.5, 24, text);
  subtext1->SetX(x_pos);
  subtext1->SetY(y_pos);
  subtext1->SetNDC();
  subtext1->SetTextAlign(13);
  subtext1->SetTextFont(52);
  subtext1->SetTextSize(0.03);
  subtext1->Draw();
}

void plot_subtext2(TString text){
  double x_pos = 0.15;
  double y_pos = 0.84;
  TLatex *subtext2 = new TLatex(3.5, 24, text);
  subtext2->SetX(x_pos);
  subtext2->SetY(y_pos);
  subtext2->SetNDC();
  subtext2->SetTextAlign(13);
  subtext2->SetTextFont(52);
  subtext2->SetTextSize(0.03);
  subtext2->Draw();
}

void plot_lumiTag(TString text){
  double x_pos = 0.95;
  double y_pos = 0.96;
  TLatex *lumi = new TLatex(3.5, 24, text);
  lumi->SetX(x_pos);
  lumi->SetY(y_pos);
  lumi->SetNDC();
  lumi->SetTextAlign(31);
  lumi->SetTextFont(42);
  lumi->SetTextSize(0.03);
  lumi->Draw();
}

void plot_channelTag(TString text){
  double x_pos = 0.125;
  double y_pos = 0.96;
  TLatex *channel = new TLatex(3.5, 24, text);
  channel->SetX(x_pos);
  channel->SetY(y_pos);
  channel->SetNDC();
  channel->SetTextAlign(11);
  channel->SetTextFont(42);
  channel->SetTextSize(0.03);
  channel->Draw();
}
