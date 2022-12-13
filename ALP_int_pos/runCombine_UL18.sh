#!/usr/bin/env bash

year=UL18

echo "starting..."
echo "removing old log files (if possible)..."
rm text2workspace_${year}.log
rm combine_${year}.log
rm limits_exp_${year}.txt

echo "entering fa loop..."
for fa in 600 800 1000 1200 1400 1600 1800 2000 2200 2400 2600 2800 3000 3200 3400 3600 3800 4000 4400 4800 5200 5600 6000 6100 # 400 -> no events: UL18_el_SRbin2_TopTag, process ST
do
  echo "running fa: ${fa}"
  echo "----- ${fa} -----" >> text2workspace_${year}.log
  text2workspace.py datacard_ALP_${year}_fa${fa}.dat -P HiggsAnalysis.CombinedLimit.ALPtoTTbar_int_pos:alpttottbarintpos -m 125 -o workspace_ALP_${year}_fa${fa}.root >> text2workspace_${year}.log
  echo "----- ${fa} -----" >> combine_${year}.log
  combine -M AsymptoticLimits workspace_ALP_${year}_fa${fa}.root --run blind >> combine_${year}.log
done

echo "extracting expected limits..."
sed -n '/Expected/p' combine_${year}.log >> limits_exp_${year}.txt
sed -i 's/Expected  2.5%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 16.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 50.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 84.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 97.5%: r < //g' limits_exp_${year}.txt
echo "done!"
