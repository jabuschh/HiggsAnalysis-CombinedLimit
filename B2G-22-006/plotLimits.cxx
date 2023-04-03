{
  cout << "starting..." << endl;

  TString inputdir_TOP20001_mtt = "/nfs/dust/cms/user/jabuschh/combine/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/TOP-20-001/mtt/";
  TString inputdir_TOP20001_ctsmtt = "/nfs/dust/cms/user/jabuschh/combine/CMSSW_10_2_13/src/HiggsAnalysis/CombinedLimit/TOP-20-001/cts_mtt_separateHists/";

  vector<TString> v_scenario = {
    "negint",
    "posint"
  };

  for(int a=0; a<2; ++a){ // a=0: negint, a=1: posint
    cout << "  scenario: "<< v_scenario.at(a) << endl;

    // input files
    std::fstream input_fa("fa.dat", std::ios_base::in);
    std::fstream input_limits_exp2p5("limits_exp2p5_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream input_limits_exp16p0("limits_exp16p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream input_limits_exp50p0("limits_exp50p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream input_limits_exp84p0("limits_exp84p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream input_limits_exp97p5("limits_exp97p5_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_fa(inputdir_TOP20001_mtt + "fa.dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_limits_exp2p5(inputdir_TOP20001_mtt + "limits_exp2p5_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_limits_exp16p0(inputdir_TOP20001_mtt + "limits_exp16p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_limits_exp50p0(inputdir_TOP20001_mtt + "limits_exp50p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_limits_exp84p0(inputdir_TOP20001_mtt + "limits_exp84p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_limits_exp97p5(inputdir_TOP20001_mtt + "limits_exp97p5_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_mtt_input_limits_obs(inputdir_TOP20001_mtt + "limits_obs_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_fa(inputdir_TOP20001_ctsmtt + "fa.dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_limits_exp2p5(inputdir_TOP20001_ctsmtt + "limits_exp2p5_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_limits_exp16p0(inputdir_TOP20001_ctsmtt + "limits_exp16p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_limits_exp50p0(inputdir_TOP20001_ctsmtt + "limits_exp50p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_limits_exp84p0(inputdir_TOP20001_ctsmtt + "limits_exp84p0_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_limits_exp97p5(inputdir_TOP20001_ctsmtt + "limits_exp97p5_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);
    std::fstream TOP20001_ctsmtt_input_limits_obs(inputdir_TOP20001_ctsmtt + "limits_obs_fullRun2_" + v_scenario.at(a) + ".dat", std::ios_base::in);

    int n = 24;
    double fa[24];
    double exp2p5[24];
    double exp16p0[24];
    double exp50p0[24];
    double exp84p0[24];
    double exp97p5[24];
    double value_in_line = 0.0;
    int counter = 0;
    while(input_fa >> value_in_line){
      fa[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(input_limits_exp2p5 >> value_in_line){
      exp2p5[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(input_limits_exp16p0 >> value_in_line){
      exp16p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(input_limits_exp50p0 >> value_in_line){
      exp50p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(input_limits_exp84p0 >> value_in_line){
      exp84p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(input_limits_exp97p5 >> value_in_line){
      exp97p5[counter] = value_in_line;
      counter++;
    }

    for(int i=0; i<n; ++i){
      fa[i] = fa[i] / 1000.;
      exp2p5[i] = exp50p0[i] - exp2p5[i];
      exp16p0[i] = exp50p0[i] - exp16p0[i];
      exp84p0[i] = exp84p0[i] - exp50p0[i];
      exp97p5[i] = exp97p5[i] - exp50p0[i];
    }

    int TOP20001_mtt_n = 15;
    double TOP20001_mtt_fa[15];
    double TOP20001_mtt_exp2p5[15];
    double TOP20001_mtt_exp16p0[15];
    double TOP20001_mtt_exp50p0[15];
    double TOP20001_mtt_exp84p0[15];
    double TOP20001_mtt_exp97p5[15];
    double TOP20001_mtt_obs[15];
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_fa >> value_in_line){
      TOP20001_mtt_fa[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_limits_exp2p5 >> value_in_line){
      TOP20001_mtt_exp2p5[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_limits_exp16p0 >> value_in_line){
      TOP20001_mtt_exp16p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_limits_exp50p0 >> value_in_line){
      TOP20001_mtt_exp50p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_limits_exp84p0 >> value_in_line){
      TOP20001_mtt_exp84p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_limits_exp97p5 >> value_in_line){
      TOP20001_mtt_exp97p5[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_mtt_input_limits_obs >> value_in_line){
      TOP20001_mtt_obs[counter] = value_in_line;
      counter++;
    }

    for(int i=0; i<TOP20001_mtt_n; ++i){
      TOP20001_mtt_fa[i] = TOP20001_mtt_fa[i] / 1000.;
      TOP20001_mtt_exp2p5[i] = TOP20001_mtt_exp50p0[i] - TOP20001_mtt_exp2p5[i];
      TOP20001_mtt_exp16p0[i] = TOP20001_mtt_exp50p0[i] - TOP20001_mtt_exp16p0[i];
      TOP20001_mtt_exp84p0[i] = TOP20001_mtt_exp84p0[i] - TOP20001_mtt_exp50p0[i];
      TOP20001_mtt_exp97p5[i] = TOP20001_mtt_exp97p5[i] - TOP20001_mtt_exp50p0[i];
    }




    int TOP20001_ctsmtt_n = 6;
    double TOP20001_ctsmtt_fa[6];
    double TOP20001_ctsmtt_exp2p5[6];
    double TOP20001_ctsmtt_exp16p0[6];
    double TOP20001_ctsmtt_exp50p0[6];
    double TOP20001_ctsmtt_exp84p0[6];
    double TOP20001_ctsmtt_exp97p5[6];
    double TOP20001_ctsmtt_obs[6];
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_fa >> value_in_line){
      TOP20001_ctsmtt_fa[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_limits_exp2p5 >> value_in_line){
      TOP20001_ctsmtt_exp2p5[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_limits_exp16p0 >> value_in_line){
      TOP20001_ctsmtt_exp16p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_limits_exp50p0 >> value_in_line){
      TOP20001_ctsmtt_exp50p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_limits_exp84p0 >> value_in_line){
      TOP20001_ctsmtt_exp84p0[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_limits_exp97p5 >> value_in_line){
      TOP20001_ctsmtt_exp97p5[counter] = value_in_line;
      counter++;
    }
    value_in_line = 0.0;
    counter = 0;
    while(TOP20001_ctsmtt_input_limits_obs >> value_in_line){
      TOP20001_ctsmtt_obs[counter] = value_in_line;
      counter++;
    }

    for(int i=0; i<TOP20001_ctsmtt_n; ++i){
      TOP20001_ctsmtt_fa[i] = TOP20001_ctsmtt_fa[i] / 1000.;
      TOP20001_ctsmtt_exp2p5[i] = TOP20001_ctsmtt_exp50p0[i] - TOP20001_ctsmtt_exp2p5[i];
      TOP20001_ctsmtt_exp16p0[i] = TOP20001_ctsmtt_exp50p0[i] - TOP20001_ctsmtt_exp16p0[i];
      TOP20001_ctsmtt_exp84p0[i] = TOP20001_ctsmtt_exp84p0[i] - TOP20001_ctsmtt_exp50p0[i];
      TOP20001_ctsmtt_exp97p5[i] = TOP20001_ctsmtt_exp97p5[i] - TOP20001_ctsmtt_exp50p0[i];
    }



    for(int b=0; b<2; ++b){ // b=0: limits on poi mu, b=1: limits on product of WCs
      if(b == 1){
        for(int i=0; i<n; ++i){ // scale to WCs
          exp2p5[i] = sqrt(exp2p5[i]) * pow(fa[i], 2);
          exp16p0[i] = sqrt(exp16p0[i]) * pow(fa[i], 2);
          exp50p0[i] = sqrt(exp50p0[i]) * pow(fa[i], 2);
          exp84p0[i] = sqrt(exp84p0[i]) * pow(fa[i], 2);
          exp97p5[i] = sqrt(exp97p5[i]) * pow(fa[i], 2);
        }
        for(int i=0; i<TOP20001_mtt_n; ++i){ // scale to WCs
          TOP20001_mtt_exp2p5[i] *= pow(TOP20001_mtt_fa[i], 2);
          TOP20001_mtt_exp16p0[i] *= pow(TOP20001_mtt_fa[i], 2);
          TOP20001_mtt_exp50p0[i] *= pow(TOP20001_mtt_fa[i], 2);
          TOP20001_mtt_exp84p0[i] *= pow(TOP20001_mtt_fa[i], 2);
          TOP20001_mtt_exp97p5[i] *= pow(TOP20001_mtt_fa[i], 2);
          TOP20001_mtt_obs[i] *= pow(TOP20001_mtt_fa[i], 2);
        }
        for(int i=0; i<TOP20001_ctsmtt_n; ++i){ // scale to WCs
          TOP20001_ctsmtt_exp2p5[i] *= pow(TOP20001_ctsmtt_fa[i], 2);
          TOP20001_ctsmtt_exp16p0[i] *= pow(TOP20001_ctsmtt_fa[i], 2);
          TOP20001_ctsmtt_exp50p0[i] *= pow(TOP20001_ctsmtt_fa[i], 2);
          TOP20001_ctsmtt_exp84p0[i] *= pow(TOP20001_ctsmtt_fa[i], 2);
          TOP20001_ctsmtt_exp97p5[i] *= pow(TOP20001_ctsmtt_fa[i], 2);
          TOP20001_ctsmtt_obs[i] *= pow(TOP20001_ctsmtt_fa[i], 2);
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

      auto tgae_2s = new TGraphAsymmErrors(n, fa, exp50p0, nullptr, nullptr, exp2p5, exp97p5);
      tgae_2s->SetFillColor(kOrange);
      tgae_2s->SetLineColor(kOrange);
      auto tgae_1s = new TGraphAsymmErrors(n, fa, exp50p0, nullptr, nullptr, exp16p0, exp84p0);
      tgae_1s->SetFillColor(kGreen+1);
      tgae_1s->SetLineColor(kGreen+1);
      auto g_exp = new TGraph(n, fa, exp50p0);
      g_exp->SetLineStyle(2);
      g_exp->SetLineWidth(2);

      auto TOP20001_mtt_tgae_2s = new TGraphAsymmErrors(TOP20001_mtt_n, TOP20001_mtt_fa, TOP20001_mtt_exp50p0, nullptr, nullptr, TOP20001_mtt_exp2p5, TOP20001_mtt_exp97p5);
      TOP20001_mtt_tgae_2s->SetFillColorAlpha(kBlue, 0.1);
      TOP20001_mtt_tgae_2s->SetLineColorAlpha(kBlue, 0.1);
      auto TOP20001_mtt_tgae_1s = new TGraphAsymmErrors(TOP20001_mtt_n, TOP20001_mtt_fa, TOP20001_mtt_exp50p0, nullptr, nullptr, TOP20001_mtt_exp16p0, TOP20001_mtt_exp84p0);
      TOP20001_mtt_tgae_1s->SetFillColorAlpha(kBlue, 0.1);
      TOP20001_mtt_tgae_1s->SetLineColorAlpha(kBlue, 0.1);
      auto TOP20001_mtt_g_exp = new TGraph(TOP20001_mtt_n, TOP20001_mtt_fa, TOP20001_mtt_exp50p0);
      TOP20001_mtt_g_exp->SetLineStyle(2);
      TOP20001_mtt_g_exp->SetLineWidth(2);
      TOP20001_mtt_g_exp->SetLineColor(kBlue);
      auto TOP20001_mtt_g_obs = new TGraph(TOP20001_mtt_n, TOP20001_mtt_fa, TOP20001_mtt_obs);
      TOP20001_mtt_g_obs->SetLineWidth(2);
      TOP20001_mtt_g_obs->SetLineColor(kBlue);
      TOP20001_mtt_g_obs->SetMarkerStyle(8);
      TOP20001_mtt_g_obs->SetMarkerColor(kBlue);

      auto TOP20001_ctsmtt_tgae_2s = new TGraphAsymmErrors(TOP20001_ctsmtt_n, TOP20001_ctsmtt_fa, TOP20001_ctsmtt_exp50p0, nullptr, nullptr, TOP20001_ctsmtt_exp2p5, TOP20001_ctsmtt_exp97p5);
      TOP20001_ctsmtt_tgae_2s->SetFillColorAlpha(kRed, 0.1);
      TOP20001_ctsmtt_tgae_2s->SetLineColorAlpha(kRed, 0.1);
      auto TOP20001_ctsmtt_tgae_1s = new TGraphAsymmErrors(TOP20001_ctsmtt_n, TOP20001_ctsmtt_fa, TOP20001_ctsmtt_exp50p0, nullptr, nullptr, TOP20001_ctsmtt_exp16p0, TOP20001_ctsmtt_exp84p0);
      TOP20001_ctsmtt_tgae_1s->SetFillColorAlpha(kRed, 0.1);
      TOP20001_ctsmtt_tgae_1s->SetLineColorAlpha(kRed, 0.1);
      auto TOP20001_ctsmtt_g_exp = new TGraph(TOP20001_ctsmtt_n, TOP20001_ctsmtt_fa, TOP20001_ctsmtt_exp50p0);
      TOP20001_ctsmtt_g_exp->SetLineStyle(2);
      TOP20001_ctsmtt_g_exp->SetLineWidth(2);
      TOP20001_ctsmtt_g_exp->SetLineColor(kRed);
      auto TOP20001_ctsmtt_g_obs = new TGraph(TOP20001_ctsmtt_n, TOP20001_ctsmtt_fa, TOP20001_ctsmtt_obs);
      TOP20001_ctsmtt_g_obs->SetLineWidth(2);
      TOP20001_ctsmtt_g_obs->SetLineColor(kRed);
      TOP20001_ctsmtt_g_obs->SetMarkerStyle(8);
      TOP20001_ctsmtt_g_obs->SetMarkerColor(kRed);

      mg->Add(tgae_2s, "3l AL");
      mg->Add(tgae_1s, "SAME 3l AL");
      // mg->Add(TOP20001_mtt_tgae_2s, "SAME 3l AL");
      // mg->Add(TOP20001_mtt_tgae_1s, "SAME 3l AL");
      // mg->Add(TOP20001_ctsmtt_tgae_2s, "SAME 3l AL");
      // mg->Add(TOP20001_ctsmtt_tgae_1s, "SAME 3l AL");
      mg->Add(g_exp, "SAME L");
      // mg->Add(TOP20001_mtt_g_exp, "SAME L");
      // mg->Add(TOP20001_mtt_g_obs, "SAME LP");
      mg->Add(TOP20001_ctsmtt_g_exp, "SAME L");
      // mg->Add(TOP20001_ctsmtt_g_obs, "SAME LP");



      // legend
      double x_pos = 0.15;
      double y_pos = 0.67;
      double x_width = 0.25;
      double y_width = 0.25;
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
      legend->AddEntry(g_exp, "Expected 95% CL upper limit", "l");
      legend->AddEntry(tgae_1s, "Expected #pm 1#sigma", "f");
      legend->AddEntry(tgae_2s, "Expected #pm 2#sigma", "f");
      // legend->AddEntry(TOP20001_mtt_g_exp, "Expected 95% CL upper limit [PRD 104, 092013: m(t#bar{t})]", "l");
      // legend->AddEntry(TOP20001_mtt_g_obs, "Observed 95% CL upper limit [PRD 104, 092013: m(t#bar{t})]", "l");
      legend->AddEntry(TOP20001_ctsmtt_g_exp, "Expected 95% CL upper limit [PRD 104, 092013: cos(#theta*) #otimes m(t#bar{t})]", "l");
      // legend->AddEntry(TOP20001_ctsmtt_g_obs, "Observed 95% CL upper limit [PRD 104, 092013: cos(#theta*) #otimes m(t#bar{t})]", "l");
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
      auto *lumi_tag = new TLatex(3.5, 24, "138 fb^{-1} (13 TeV)");
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
      if(b == 0){
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
      if(b == 0) c1->SaveAs("brazilianLimits_mu_" + v_scenario.at(a) + ".pdf");
      else c1->SaveAs("brazilianLimits_WCs_" + v_scenario.at(a) + ".pdf");
      c1->Close();
    }
  }
  cout << "done!" << endl;
}
