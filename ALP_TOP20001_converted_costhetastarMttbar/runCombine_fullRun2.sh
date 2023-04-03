#!/usr/bin/env bash

year=fullRun2

echo "starting..."
echo "removing old log files (if possible)..."
rm text2workspace_${year}.log
rm combine_${year}.log
rm limits_exp_${year}.txt

echo "entering fa loop..."
for fa in 420 520 620 800 1000 3500
do
  echo "running fa: ${fa}"
  echo "----- ${fa} -----" >> text2workspace_${year}.log
  text2workspace.py datacard_ALP_${year}_fa${fa}.dat -P HiggsAnalysis.CombinedLimit.ALPtoTTbar_int_neg:alpttottbarintneg -m 125 -o workspace_ALP_${year}_fa${fa}.root >> text2workspace_${year}.log
  echo "----- ${fa} -----" >> combine_${year}.log
  combine -v3 -M AsymptoticLimits workspace_ALP_${year}_fa${fa}.root --run blind >> combine_${year}.log
done

echo "extracting expected limits..."
sed -n '/Expected /p' combine_${year}.log >> limits_exp_${year}.txt
sed -i 's/Expected  2.5%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 16.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 50.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 84.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 97.5%: r < //g' limits_exp_${year}.txt
echo "done!"
