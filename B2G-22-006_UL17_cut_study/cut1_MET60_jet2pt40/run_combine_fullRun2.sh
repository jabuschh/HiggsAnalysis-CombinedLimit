#!/usr/bin/env bash

year=UL17

echo "starting..."
echo "deleting old files (if they exist)..."

for channel in muon # electron
do
  echo "channel: ${channel}"

  for scenario in negint posint
  do
    echo "scenario: ${scenario}"

    rm log/text2workspace_${year}_${channel}_${scenario}.log
    rm log/combine_${year}_${channel}_fa*_${scenario}.log
    rm limits_exp2p5_${year}_${channel}_${scenario}.dat
    rm limits_exp16p0_${year}_${channel}_${scenario}.dat
    rm limits_exp50p0_${year}_${channel}_${scenario}.dat
    rm limits_exp84p0_${year}_${channel}_${scenario}.dat
    rm limits_exp97p5_${year}_${channel}_${scenario}.dat
    rm fa.dat

    # 400: zero events in UL16_el_SRbin2_TopTag, process ST

    for fa in 600 800 1000 1200 1400 1600 1800 2000 2200 2400 2600 2800 3000 3200 3400 3600 3800 4000 4400 4800 5200 5600 6000 6100
    do
      echo "  fa: ${fa}"
      echo "${fa}" >> fa.dat
      echo "    creating workspace..."
      text2workspace.py datacard_${year}_${channel}_fa${fa}.dat -P HiggsAnalysis.CombinedLimit.ALPtoTTbar_${scenario}:alpttottbar_${scenario} -m 125 -o workspace_${year}_${channel}_fa${fa}_${scenario}.root >> log/text2workspace_${year}_${channel}_${scenario}.log
      echo "    running combine..."
      combine -M AsymptoticLimits workspace_${year}_${channel}_fa${fa}_${scenario}.root --run blind >> log/combine_${year}_${channel}_fa${fa}_${scenario}.log
      echo "    extracting limits..."
      sed -n '/Expected  2.5%: /p' log/combine_${year}_${channel}_fa${fa}_${scenario}.log >> limits_exp2p5_${year}_${channel}_${scenario}.dat
      sed -n '/Expected 16.0%: /p' log/combine_${year}_${channel}_fa${fa}_${scenario}.log >> limits_exp16p0_${year}_${channel}_${scenario}.dat
      sed -n '/Expected 50.0%: /p' log/combine_${year}_${channel}_fa${fa}_${scenario}.log >> limits_exp50p0_${year}_${channel}_${scenario}.dat
      sed -n '/Expected 84.0%: /p' log/combine_${year}_${channel}_fa${fa}_${scenario}.log >> limits_exp84p0_${year}_${channel}_${scenario}.dat
      sed -n '/Expected 97.5%: /p' log/combine_${year}_${channel}_fa${fa}_${scenario}.log >> limits_exp97p5_${year}_${channel}_${scenario}.dat
    done

    sed -i 's/Expected  2.5%: r < //g' limits_exp2p5_${year}_${channel}_${scenario}.dat
    sed -i 's/Expected 16.0%: r < //g' limits_exp16p0_${year}_${channel}_${scenario}.dat
    sed -i 's/Expected 50.0%: r < //g' limits_exp50p0_${year}_${channel}_${scenario}.dat
    sed -i 's/Expected 84.0%: r < //g' limits_exp84p0_${year}_${channel}_${scenario}.dat
    sed -i 's/Expected 97.5%: r < //g' limits_exp97p5_${year}_${channel}_${scenario}.dat
  done
done

echo "done!"
