#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TLatex.h>
#include <TGraphAsymmErrors.h>
#include "RooRealVar.h"
#include "TLegend.h"
#include "RooDataSet.h"
#include "RooDataHist.h"
#include "RooGaussian.h"
#include "TCanvas.h"

#include "RooPlot.h"
#include "TTree.h"
#include "TH1D.h"
#include "TRandom.h"
using namespace RooFit ;
using namespace std;

void plot_limit_ZPrime_W1()
{

  // DeepAK8 selection, using Mtt distribution binned in cos theta star
  std::fstream myfile("ZPrime_W1_limits_combined_exp.txt", std::ios_base::in);
  Float_t twosd[22];
  Float_t onesd[22];
  Float_t exp[22];
  Float_t onesu[22];
  Float_t twosu[22];



  Float_t a;
  Int_t c1 = 0;
  Int_t c2 = 0;
  Int_t c3 = 0;
  Int_t c4 = 0;
  Int_t c5 = 0;

  Int_t c = 0;
  while (myfile >> a)
  {
    c = c + 1;


    if (c % 5 == 1){
      twosd[c1] = a;
      c1 = c1 + 1;
    }

    if (c % 5 == 2){
      onesd[c2] = a;
      c2 = c2 + 1;
    }

    if (c % 5 == 3){
      exp[c3] = a;
      c3 = c3 + 1;
    }

    if (c % 5 == 4){
      onesu[c4] = a;
      c4 = c4 + 1;
    }

    if (c % 5 == 0){
      twosu[c5] = a;
      c5 = c5 + 1;
    }

  }


  Float_t X[]    = {0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2.0,2.5,3.0,3.5,4.0,4.5,5.0,6.0,7.0,8.0,9.0};
  Float_t Zero[] = {0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0};

  Float_t oneD[22];
  Float_t oneU[22];
  Float_t twoD[22];
  Float_t twoU[22];

  int i;
  for(i=0;i<22;i++){
    oneD[i]=exp[i]-onesd[i];
    oneU[i]=onesu[i]-exp[i];
    twoD[i]=exp[i]-twosd[i];
    twoU[i]=twosu[i]-exp[i];
  }

  // Theory limit Z' 1%
  Float_t th[27] = {5.83131e+01, 1.36051e+01, 4.50540e+00, 1.80866e+00, 8.13716e-01, 3.97420e-01, 2.05510e-01, 1.10890e-01, 6.17038e-02, 3.52336e-02, 2.05665e-02, 1.21935e-02, 7.34662e-03, 4.46826e-03, 2.75870e-03, 1.72335e-03, 1.09115e-03, 6.99838e-04, 4.58135e-04, 3.04742e-04, 2.07506e-04, 1.44911e-04, 1.03407e-04, 7.60116e-05, 5.71530e-05, 4.42244e-05, 3.49246e-05};

  Float_t X_th[27] = {0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4,4.25,4.5,4.75,5,5.25,5.5,5.75,6,6.25,6.5,6.75,7};

  TCanvas* cc = new TCanvas("Scatter","Scatter",1200,800) ;
  cc->Divide(1,1) ;
  cc->cd(1) ;
  gPad->SetTopMargin(0.07);
  gPad->SetBottomMargin(0.17);
  gPad->SetLeftMargin(0.2);
  gPad->SetRightMargin(0.1);
  gPad->SetLogy();
  gPad->SetTicks();

  auto mg  = new TMultiGraph();

  auto ge2 = new TGraphAsymmErrors(22, X, exp, Zero, Zero,twoD,twoU);
  ge2->SetFillColor(kOrange);
  ge2->GetXaxis()->SetTitle("Mttbar [TeV]");
  ge2->Draw("AP");
  mg->Add(ge2,"3l ALP");

  auto ge = new TGraphAsymmErrors(22, X, exp, Zero, Zero,oneD,oneU);
  ge->SetFillColor(kGreen+1);
  mg->Add(ge,"SAME 3l ALP");

  auto ge3 = new TGraph(22,X,exp);
  ge3->SetLineStyle(7);
  ge3->SetLineWidth(2);
  ge3->SetLineColor(kBlack);
  mg->Add(ge3,"SAME L");

  auto ge4 = new TGraph(27,X_th,th);
  ge4->SetLineStyle(1);
  ge4->SetLineWidth(2);
  ge4->SetLineColor(kRed);
  mg->Add(ge4,"SAME L");

  mg->Draw("aL");
  mg->GetXaxis()->SetTitle("M_{Z'} [TeV]");
  mg->GetXaxis()->SetTitleSize(0.055);
  mg->GetXaxis()->SetLabelSize(0.05);
  mg->GetYaxis()->SetTitle("#sigma_{Z'} x B(Z' #rightarrow t#bar{t}) [pb]");
  mg->GetYaxis()->SetRangeUser(0.0001,10000);
  //mg->GetYaxis()->SetRangeUser(0.01,1);
  mg->GetYaxis()->SetTitleSize(0.055);
  mg->GetYaxis()->SetLabelSize(0.05);

  auto legend = new TLegend(0.6,0.75,0.88,0.9);
  legend->SetBorderSize(0);
  legend->AddEntry(ge3,"Expected","l");
  legend->AddEntry(ge,"#pm 1#sigma Expected","f");
  legend->AddEntry(ge2,"#pm 2#sigma Expected","f");
  legend->AddEntry(ge4,"Z' 10% width","l");
  legend->Draw("same");
  //cc->BuildLegend();

  TString cmstext = "CMS";
  TLatex *text2 = new TLatex(3.5, 24, cmstext);
  text2->SetNDC();
  text2->SetTextAlign(13);
  text2->SetX(0.24);
  text2->SetTextFont(62);
  text2->SetTextSize(0.06825);
  text2->SetY(0.895);
  text2->Draw();


  TString supptext = "#splitline{Simulation}{Work in progress}";
  TLatex *text4 = new TLatex(3.5, 24, supptext);
  text4->SetNDC();
  text4->SetTextAlign(13);
  text4->SetX(0.24);
  text4->SetTextFont(52);
  text4->SetTextSize(0.55*0.06825);
  text4->SetY(0.8312);
  text4->Draw();

  TString infotext = "138 fb^{-1} (13 TeV)";
  //TString infotext = "41.5 fb^{-1} (13 TeV)";
  TLatex *text1 = new TLatex(3.5, 24, infotext);
  text1->SetNDC();
  text1->SetTextAlign(31);
  text1->SetX(1.-0.1);
  text1->SetTextFont(42);
  text1->SetTextSize(0.07*0.7);
  text1->SetY(1.-0.07+0.2*0.07);
  text1->Draw();

  TString extratext = "l+jets";
  TLatex *text3 = new TLatex(3.5, 24, extratext);
  text3->SetNDC();
  text3->SetTextAlign(31);
  text3->SetX(0.72);
  text3->SetTextFont(42);
  text3->SetTextSize(0.07*0.5);
  text3->SetY(0.7);
  text3->Draw();


  //TString extratext2 = "0 t tag";
  //TLatex *text5 = new TLatex(3.5, 24, extratext2);
  //text5->SetNDC();
  //text5->SetTextAlign(31);
  //text5->SetX(0.7);
  //text5->SetTextFont(42);
  //text5->SetTextSize(0.07*0.5);
  //text5->SetY(0.6);
  //text5->Draw();

  cc->Print("Brazil_ZPrime_W1_combination.pdf");
}
