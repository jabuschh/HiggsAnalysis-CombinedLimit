#!/usr/bin/env bash

year=fullRun2

echo "starting..."

echo "deleting old files (if they exist)..."

for scenario in negint posint
do
  echo "scenario: ${scenario}"

  rm log/text2workspace_${year}_${scenario}.log
  rm log/combine_${year}_fa*_${scenario}.log
  rm limits_exp2p5_${year}_${scenario}.dat
  rm limits_exp16p0_${year}_${scenario}.dat
  rm limits_exp50p0_${year}_${scenario}.dat
  rm limits_exp84p0_${year}_${scenario}.dat
  rm limits_exp97p5_${year}_${scenario}.dat
  rm limits_obs_${year}_${scenario}.dat
  rm fa.dat

  for fa in 400 480 560 640 720 800 900 1000 1150 1300 1500 1700 2000 2300 3500
  do
    echo "  fa: ${fa}"
    echo "${fa}" >> fa.dat
    echo "    creating workspace..."
    text2workspace.py datacard_${year}_fa${fa}.dat -P HiggsAnalysis.CombinedLimit.ALPtoTTbar_${scenario}:alpttottbar_${scenario} -m 125 -o workspace_${year}_fa${fa}_${scenario}.root >> log/text2workspace_${year}_${scenario}.log
    echo "    running combine..."
    combine -v2 -M AsymptoticLimits workspace_${year}_fa${fa}_${scenario}.root >> log/combine_${year}_fa${fa}_${scenario}.log # add "--run blind" for blinding data
    echo "    extracting limits..."
    sed -n '/Expected  2.5%: /p' log/combine_${year}_fa${fa}_${scenario}.log >> limits_exp2p5_${year}_${scenario}.dat
    sed -n '/Expected 16.0%: /p' log/combine_${year}_fa${fa}_${scenario}.log >> limits_exp16p0_${year}_${scenario}.dat
    sed -n '/Expected 50.0%: /p' log/combine_${year}_fa${fa}_${scenario}.log >> limits_exp50p0_${year}_${scenario}.dat
    sed -n '/Expected 84.0%: /p' log/combine_${year}_fa${fa}_${scenario}.log >> limits_exp84p0_${year}_${scenario}.dat
    sed -n '/Expected 97.5%: /p' log/combine_${year}_fa${fa}_${scenario}.log >> limits_exp97p5_${year}_${scenario}.dat
    sed -n '/Observed Limit: /p' log/combine_${year}_fa${fa}_${scenario}.log >> limits_obs_${year}_${scenario}.dat
  done

  sed -i 's/Expected  2.5%: r < //g' limits_exp2p5_${year}_${scenario}.dat
  sed -i 's/Expected 16.0%: r < //g' limits_exp16p0_${year}_${scenario}.dat
  sed -i 's/Expected 50.0%: r < //g' limits_exp50p0_${year}_${scenario}.dat
  sed -i 's/Expected 84.0%: r < //g' limits_exp84p0_${year}_${scenario}.dat
  sed -i 's/Expected 97.5%: r < //g' limits_exp97p5_${year}_${scenario}.dat
  sed -i 's/Observed Limit: r < //g' limits_obs_${year}_${scenario}.dat
done

echo "done!"
