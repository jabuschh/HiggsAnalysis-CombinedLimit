{
  cout << "starting..." << endl;

  vector<TString> v_scenario = {"negint", "posint"};
  vector<TString> v_channel = {"electron", "muon"};

  for(int a=0; a<v_scenario.size(); ++a){ // a=0: negint, a=1: posint
    cout << "scenario: "<< v_scenario.at(a) << endl;

    for(int b=0; b<v_channel.size(); ++b){
      cout << "channel: "<< v_channel.at(b) << endl;

      // input files
      std::fstream input_fa("default_MET50_jet2pt30/fa.dat", std::ios_base::in);
      std::fstream input_limits_cut0("default_MET50_jet2pt30/limits_exp50p0_UL17_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".dat", std::ios_base::in);
      std::fstream input_limits_cut1("cut1_MET60_jet2pt40/limits_exp50p0_UL17_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".dat", std::ios_base::in);
      std::fstream input_limits_cut2("cut2_MET70_jet2pt40/limits_exp50p0_UL17_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".dat", std::ios_base::in);
      std::fstream input_limits_cut3("cut3_MET70_jet2pt50/limits_exp50p0_UL17_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".dat", std::ios_base::in);
      std::fstream input_limits_cut4("cut4_MET80_jet2pt50/limits_exp50p0_UL17_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".dat", std::ios_base::in);

      int n = 24;
      double fa[24];
      double cut0[24];
      double cut1[24];
      double cut2[24];
      double cut3[24];
      double cut4[24];
      double value_in_line = 0.0;
      int counter = 0;

      while(input_fa >> value_in_line){
        fa[counter] = value_in_line;
        counter++;
      }
      value_in_line = 0.0;
      counter = 0;
      while(input_limits_cut0 >> value_in_line){
        cut0[counter] = value_in_line;
        counter++;
      }
      value_in_line = 0.0;
      counter = 0;
      while(input_limits_cut1 >> value_in_line){
        cut1[counter] = value_in_line;
        counter++;
      }
      value_in_line = 0.0;
      counter = 0;
      while(input_limits_cut2 >> value_in_line){
        cut2[counter] = value_in_line;
        counter++;
      }
      value_in_line = 0.0;
      counter = 0;
      while(input_limits_cut3 >> value_in_line){
        cut3[counter] = value_in_line;
        counter++;
      }
      value_in_line = 0.0;
      counter = 0;
      while(input_limits_cut4 >> value_in_line){
        cut4[counter] = value_in_line;
        counter++;
      }

      for(int i=0; i<n; ++i) fa[i] = fa[i] / 1000.;

      for(int c=0; c<2; ++c){ // c=0: limits on poi mu, c=1: limits on product of WCs
        if(c == 1){
          for(int i=0; i<n; ++i){
            cut0[i] = sqrt(cut0[i]) * pow(fa[i], 2);
            cut1[i] = sqrt(cut1[i]) * pow(fa[i], 2);
            cut2[i] = sqrt(cut2[i]) * pow(fa[i], 2);
            cut3[i] = sqrt(cut3[i]) * pow(fa[i], 2);
            cut4[i] = sqrt(cut4[i]) * pow(fa[i], 2);
          }
        }

        // plot limits on mu
        double margin_top = 0.05;
        double margin_left = 0.10;
        double margin_right = 0.05;
        double margin_bottom = 0.10;
        TCanvas *c1 = new TCanvas("c1","c1",0,0,800,800);
        gStyle->SetOptStat(0);
        gStyle->SetOptTitle(kFALSE);
        c1->Draw();
        c1->SetTopMargin(margin_top);
        c1->SetBottomMargin(margin_bottom);
        c1->SetLeftMargin(margin_left);
        c1->SetRightMargin(margin_right);
        c1->SetTicks();
        c1->SetLogy();
        c1->cd();

        auto mg  = new TMultiGraph();
        mg->Draw("aL");

        auto g_cut0 = new TGraph(n, fa, cut0);
        auto g_cut1 = new TGraph(n, fa, cut1);
        auto g_cut2 = new TGraph(n, fa, cut2);
        auto g_cut3 = new TGraph(n, fa, cut3);
        auto g_cut4 = new TGraph(n, fa, cut4);

        g_cut0->SetLineStyle(2);
        g_cut1->SetLineStyle(2);
        g_cut2->SetLineStyle(2);
        g_cut3->SetLineStyle(2);
        g_cut4->SetLineStyle(2);

        g_cut0->SetLineWidth(2);
        g_cut1->SetLineWidth(2);
        g_cut2->SetLineWidth(2);
        g_cut3->SetLineWidth(2);
        g_cut4->SetLineWidth(2);

        g_cut0->SetLineColor(kBlack);
        g_cut1->SetLineColor(kRed);
        g_cut2->SetLineColor(kBlue);
        g_cut3->SetLineColor(kGreen);
        g_cut4->SetLineColor(kOrange);

        mg->Add(g_cut0, "L");
        mg->Add(g_cut1, "SAME L");
        mg->Add(g_cut2, "SAME L");
        mg->Add(g_cut3, "SAME L");
        mg->Add(g_cut4, "SAME L");

        // legend
        double x_pos = 0.15;
        double y_pos = 0.60;
        double x_width = 0.25;
        double y_width = 0.30;
        TLegend *legend;
        legend = new TLegend(x_pos,y_pos,x_pos+x_width,y_pos+y_width);
        legend->SetBorderSize(1);
        legend->SetTextSize(0.025);
        legend->SetLineWidth(0);
        legend->SetFillColor(0);
        legend->SetFillStyle(1001);
        legend->SetNColumns(1);
        if(a == 0) legend->SetHeader("negative ALP-SM interference (c_{#tilde{G}} c_{#tilde{#Phi}} > 0)");
        else legend->SetHeader("positive ALP-SM interference (c_{#tilde{G}} c_{#tilde{#Phi}} < 0)");
        legend->AddEntry(g_cut0, "default: MET > 50 GeV, p_{T}^{2nd AK4 jet} > 30 GeV", "l");
        legend->AddEntry(g_cut1, "cut1: MET > 60 GeV, p_{T}^{2nd AK4 jet} > 40 GeV", "l");
        legend->AddEntry(g_cut2, "cut2: MET > 70 GeV, p_{T}^{2nd AK4 jet} > 40 GeV", "l");
        legend->AddEntry(g_cut3, "cut3: MET > 70 GeV, p_{T}^{2nd AK4 jet} > 50 GeV", "l");
        legend->AddEntry(g_cut4, "cut4: MET > 80 GeV, p_{T}^{2nd AK4 jet} > 50 GeV", "l");

        // CMS tag
        x_pos = 0.1;
        y_pos = 0.957;
        auto *cms_tag = new TLatex(3.5, 24, "Private Work (CMS Simulation)");
        cms_tag->SetNDC();
        cms_tag->SetTextAlign(11);
        cms_tag->SetX(x_pos);
        cms_tag->SetY(y_pos);
        cms_tag->SetTextFont(62);
        cms_tag->SetTextSize(0.032);
        // lumi tag
        x_pos = 0.95;
        y_pos = 0.957;
        auto *lumi_tag = new TLatex(3.5, 24, "41.5 fb^{-1} (13 TeV)");
        lumi_tag->SetNDC();
        lumi_tag->SetTextAlign(31);
        lumi_tag->SetX(x_pos);
        lumi_tag->SetY(y_pos);
        lumi_tag->SetTextFont(42);
        lumi_tag->SetTextSize(0.032);

        // x-axis
        mg->GetXaxis()->SetTitle("f_{a} [TeV]");
        mg->GetXaxis()->SetTitleOffset(1.4);
        mg->GetXaxis()->SetLimits(0.1, 7.0);
        // y-axis
        if(c == 0){
          mg->GetYaxis()->SetTitle("#mu");
        }
        else{
          if(a == 0) mg->GetYaxis()->SetTitle("c_{#tilde{G}} c_{#tilde{#Phi}}");
          else mg->GetYaxis()->SetTitle("- c_{#tilde{G}} c_{#tilde{#Phi}}");
        }
        mg->GetYaxis()->SetRangeUser(0.02, 5000);
        mg->GetYaxis()->SetTitleOffset(1.4);

        legend->Draw();
        cms_tag->Draw();
        lumi_tag->Draw();

        gPad->RedrawAxis();
        c1->Modified();
        if(c == 0) c1->SaveAs("brazilianLimits_mu_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".pdf");
        else c1->SaveAs("brazilianLimits_WCs_" + v_channel.at(b) + "_" + v_scenario.at(a) + ".pdf");
        c1->Close();
      }
    }
  }
  cout << "done!" << endl;
}
