#!/bin/bash
#rm -rf data/subj$1/plots
#mkdir data/subj$1/plots
for f in data/subj$1/*_1.data;
do
  echo "Plotting $f file..."
  python world.py $f f result/subj$1/task1
done
for f in data/subj$1/*_2.data;
do
  echo "Plotting $f file..."
  python world.py $f f result/subj$1/task2
done
for f in data/subj$1/*_3.data;
do
  echo "Plotting $f file..."
  python world.py $f f result/subj$1/task3
done
for f in data/subj$1/*_4.data;
do
  echo "Plotting $f file..."
  python world.py $f f result/subj$1/task4
done
mv data/subj$1/*.png data/subj$1/plots/

