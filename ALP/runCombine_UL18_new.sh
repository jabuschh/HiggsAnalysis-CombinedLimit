#!/usr/bin/env bash

year=UL18

echo "starting..."

echo "removing old files (if possible)..."
rm ${year}_fa.txt
rm limits_exp_${year}_2sigmadown.txt
rm limits_exp_${year}_1sigmadown.txt
rm limits_exp_${year}.txt
rm limits_exp_${year}_1sigmaup.txt
rm limits_exp_${year}_2sigmaup.txt

for fa in 600 800 1000 1200 1400 1600 1800 2000 2200 2400 2600 2800 3000 3200 3400 3600 3800 4000 4400 4800 5200 5600 6000 6100 # 400 -> no events: UL18_el_SRbin2_TopTag, process ST
do
  echo "running fa: ${fa}"
  rm text2workspace_${year}_fa${fa}.log
  rm combine_${year}_fa${fa}.log

  text2workspace.py datacard_ALP_${year}_fa${fa}.dat -P HiggsAnalysis.CombinedLimit.ALPtoTTbar:alpttottbar -m 125 -o workspace_ALP_${year}_fa${fa}.root >> text2workspace_${year}_fa${fa}.log
  combine -M AsymptoticLimits workspace_ALP_${year}_fa${fa}.root --run blind >> combine_${year}_fa${fa}.log

  echo "${fa}" >> ${year}_fa.txt
  sed -n '/Expected  2.5%: r < /p' combine_${year}_fa${fa}.log >> limits_exp_${year}_2sigmadown.txt
  sed -n '/Expected 16.0%: r < /p' combine_${year}_fa${fa}.log >> limits_exp_${year}_1sigmadown.txt
  sed -n '/Expected 50.0%: r < /p' combine_${year}_fa${fa}.log >> limits_exp_${year}.txt
  sed -n '/Expected 84.0%: r < /p' combine_${year}_fa${fa}.log >> limits_exp_${year}_1sigmaup.txt
  sed -n '/Expected 97.5%: r < /p' combine_${year}_fa${fa}.log >> limits_exp_${year}_2sigmaup.txt
done

sed -i 's/Expected  2.5%: r < //g' limits_exp_${year}_2sigmadown.txt
sed -i 's/Expected 16.0%: r < //g' limits_exp_${year}_1sigmadown.txt
sed -i 's/Expected 50.0%: r < //g' limits_exp_${year}.txt
sed -i 's/Expected 84.0%: r < //g' limits_exp_${year}_1sigmaup.txt
sed -i 's/Expected 97.5%: r < //g' limits_exp_${year}_2sigmaup.txt

echo "done!"
