#!/usr/bin/env bash

echo "starting..."

combineCards.py bin1=datacard_ALP_fullRun2_bin1.dat > datacard_ALP_fullRun2_fa420.dat
combineCards.py bin1=datacard_ALP_fullRun2_bin1.dat bin2=datacard_ALP_fullRun2_bin2.dat > datacard_ALP_fullRun2_fa520.dat
combineCards.py bin1=datacard_ALP_fullRun2_bin1.dat bin2=datacard_ALP_fullRun2_bin2.dat bin3=datacard_ALP_fullRun2_bin3.dat > datacard_ALP_fullRun2_fa620.dat
combineCards.py bin1=datacard_ALP_fullRun2_bin1.dat bin2=datacard_ALP_fullRun2_bin2.dat bin3=datacard_ALP_fullRun2_bin3.dat bin4=datacard_ALP_fullRun2_bin4.dat > datacard_ALP_fullRun2_fa800.dat
combineCards.py bin1=datacard_ALP_fullRun2_bin1.dat bin2=datacard_ALP_fullRun2_bin2.dat bin3=datacard_ALP_fullRun2_bin3.dat bin4=datacard_ALP_fullRun2_bin4.dat bin5=datacard_ALP_fullRun2_bin5.dat > datacard_ALP_fullRun2_fa1000.dat
combineCards.py bin1=datacard_ALP_fullRun2_bin1.dat bin2=datacard_ALP_fullRun2_bin2.dat bin3=datacard_ALP_fullRun2_bin3.dat bin4=datacard_ALP_fullRun2_bin4.dat bin5=datacard_ALP_fullRun2_bin5.dat bin6=datacard_ALP_fullRun2_bin6.dat > datacard_ALP_fullRun2_fa3500.dat

echo "done!"
