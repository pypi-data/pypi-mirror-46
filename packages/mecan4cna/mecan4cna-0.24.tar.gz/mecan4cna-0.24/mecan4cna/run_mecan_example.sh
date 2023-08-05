#!/bin/sh
## run example Mecan analysis

## run mecan --demo to copy the script file and example files to the current directry

## run Mecan on example files
echo --- running Mecan ---
for fnum in 1 2 3 4 5
do
	echo analyzing: examples/segment_example_$fnum.tsv
	mecan4cna -i examples/segment_example_$fnum.tsv -o example_results/example_$fnum -n -p
done



## The plot of example 3 is ambiguous, 
## try with differnt bins.
echo analyzing: examples/segment_example_3.tsv with 25 bins
mecan4cna -i examples/segment_example_3.tsv -o example_results/example_3_25bins -b 25 -p
echo analyzing: examples/segment_example_3.tsv with 10 bins
mecan4cna -i examples/segment_example_3.tsv -o example_results/example_3_10bins -b 10 -p