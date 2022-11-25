{

  std::fstream file_fa("UL18_fa.txt", std::ios_base::in);
  std::fstream file_twoSigmaDown("limits_exp_UL18_2sigmadown.txt", std::ios_base::in);
  std::fstream file_oneSigmaDown("limits_exp_UL18_1sigmadown.txt", std::ios_base::in);
  std::fstream file_expected("limits_exp_UL18.txt", std::ios_base::in);
  std::fstream file_oneSigmaUp("limits_exp_UL18_1sigmaup.txt", std::ios_base::in);
  std::fstream file_twoSigmaUp("limits_exp_UL18_2sigmaup.txt", std::ios_base::in);

  Double_t fa[24];
  Double_t twoSigmaDown[24];
  Double_t oneSigmaDown[24];
  Double_t expected[24];
  Double_t oneSigmaUp[24];
  Double_t twoSigmaUp[24];

  Double_t value_inCurrentLine;
  Int_t counter = 0;

  while(file_fa >> value_inCurrentLine){
    fa[counter] = value_inCurrentLine;
    counter++;
  }

  counter = 0;
  while(file_twoSigmaDown >> value_inCurrentLine)
  {
    twoSigmaDown[counter] = value_inCurrentLine;
    counter++;
  }

  counter = 0;
  while(file_oneSigmaDown >> value_inCurrentLine){
    oneSigmaDown[counter] = value_inCurrentLine;
    counter++;
  }

  counter = 0;
  while(file_expected >> value_inCurrentLine){
    expected[counter] = value_inCurrentLine;
    counter++;
  }

  counter = 0;
  while(file_oneSigmaUp >> value_inCurrentLine){
    oneSigmaUp[counter] = value_inCurrentLine;
    counter++;
  }

  counter = 0;
  while(file_twoSigmaUp >> value_inCurrentLine){
    twoSigmaUp[counter] = value_inCurrentLine;
    counter++;
  }


  Double_t err_2sigmaDown[24];
  Double_t err_1sigmaDown[24];
  Double_t err_1sigmaUp[24];
  Double_t err_2sigmaUp[24];

  // scale limits from mu to cG x cPhi
  for(int i=0; i<24; i++){
    twoSigmaDown[i] = sqrt(twoSigmaDown[i]) * pow(fa[i]/1000, 2);
    oneSigmaDown[i] = sqrt(oneSigmaDown[i]) * pow(fa[i]/1000, 2);
    expected[i] = sqrt(expected[i]) * pow(fa[i]/1000, 2);
    oneSigmaUp[i] = sqrt(oneSigmaUp[i]) * pow(fa[i]/1000, 2);
    twoSigmaUp[i] = sqrt(twoSigmaUp[i]) * pow(fa[i]/1000, 2);

    err_2sigmaDown[i] = expected[i] - twoSigmaDown[i];
    err_1sigmaDown[i] = expected[i] - oneSigmaDown[i];
    err_1sigmaUp[i] = oneSigmaUp[i] - expected[i];
    err_2sigmaUp[i] = twoSigmaUp[i] - expected[i];
  }

  // no error in fa
  Double_t err_fa[24];
  for(int i=0; i<24; i++){
    err_fa[i] = 0.0;
  }

  // plotting
  cout << "plotting..." << endl;
  TCanvas *c1 = new TCanvas("c1", "c1", 0, 0, 800, 800);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(kFALSE);
  gPad->SetTopMargin(0.05);
  gPad->SetBottomMargin(0.10);
  gPad->SetLeftMargin(0.12);
  gPad->SetRightMargin(0.05);
  gPad->SetLogy();
  gPad->SetTicks();

  auto multigraph = new TMultiGraph();
  // multigraph->Draw("AL");

  auto gr_2sigma = new TGraphAsymmErrors(24, fa, expected, err_fa, err_fa, err_2sigmaDown, err_2sigmaUp);
  gr_2sigma->SetFillColor(kOrange);
  gr_2sigma->Draw("AP");
  multigraph->Add(gr_2sigma,"SAME 3l ALP");

  auto gr_1sigma = new TGraphAsymmErrors(24, fa, expected, err_fa, err_fa, err_1sigmaDown, err_1sigmaUp);
  gr_1sigma->SetFillColor(kGreen+1);
  // gr_1sigma->Draw("AP");
  multigraph->Add(gr_1sigma,"SAME 3l ALP");

  auto gr_exp = new TGraph(24, fa, expected);
  gr_exp->SetLineColor(kBlack);
  gr_exp->SetLineStyle(2);
  gr_exp->SetLineWidth(2);
  gr_exp->SetMarkerStyle(8);
  gr_exp->SetMarkerColor(kBlack);
  multigraph->Add(gr_exp, "SAME LP");

  multigraph->Draw("aL");

  // x-axis
  multigraph->GetXaxis()->SetTitle("f_{a} [TeV]");
  multigraph->GetXaxis()->SetTitleOffset(1.3);
  // multigraph->GetXaxis()->SetLimits(0.3,6.1);
  // y-axis
  multigraph->GetYaxis()->SetTitle("|c_{#tilde{G}} c_{#tilde{#Phi}}|");
  multigraph->GetYaxis()->SetTitleOffset(1.5);
  // multigraph->GetYaxis()->SetRangeUser(0.1,1000);

  // c1->Modified();
  // multigraph->Draw("aL");

  // gPad->RedrawAxis();
  // multigraph->Draw();

  // c1->Modified();






}
