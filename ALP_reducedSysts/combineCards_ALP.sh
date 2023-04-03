#!/usr/bin/env bash

echo "starting..."

echo "combining channels for each year..."
for year in UL16 UL17 UL18
do
  echo "----- ${year} -----"
  for fa in 400 600 800 1000 1200 1400 1600 1800 2000 2200 2400 2600 2800 3000 3200 3400 3600 3800 4000 4400 4800 5200 5600 6000 6100
  do
    echo "fa: ${fa}"
    combineCards.py ${year}_el=datacard_ALP_${year}_electron_fa${fa}.dat ${year}_mu=datacard_ALP_${year}_muon_fa${fa}.dat > datacard_ALP_${year}_fa${fa}.dat
  done
done

echo "combining channels and years (full Run 2) ..."
for fa in 400 600 800 1000 1200 1400 1600 1800 2000 2200 2400 2600 2800 3000 3200 3400 3600 3800 4000 4400 4800 5200 5600 6000 6100
do
  echo "fa: ${fa}"
  combineCards.py UL16_el=datacard_ALP_UL16_electron_fa${fa}.dat UL16_mu=datacard_ALP_UL16_muon_fa${fa}.dat UL17_el=datacard_ALP_UL17_electron_fa${fa}.dat UL17_mu=datacard_ALP_UL17_muon_fa${fa}.dat UL18_el=datacard_ALP_UL18_electron_fa${fa}.dat UL18_mu=datacard_ALP_UL18_muon_fa${fa}.dat > datacard_ALP_fullRun2_fa${fa}.dat
done

echo "done!"
