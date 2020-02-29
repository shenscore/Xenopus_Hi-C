#!/bin/bash
# pipeline to calculate DI index (KR normalized)
# input : hicfile resolusion threads_number
# need exec file straw in your path

hic_file=$1
res=$2
threads=$3
chrList=(Chr01 Chr02 Chr03 Chr04 Chr05 Chr06 Chr07 Chr08 Chr09 Chr10)
block_size=40

dir=/path/to/script

name=$(basename $hic_file .hic)


for chr in ${chrList[*]}
do
  echo "fixedStep chrom=$chr start=1 step="${res}" span="${res} > $name.$chr.DI.wig
  straw VC_SQRT $hic_file $chr $chr BP $res | parallel --pipe -j $threads ${dir}/calc_DI_worker.awk -v block_size=$block_size -v res=$res | ${dir}/calc_DI_merge.awk >> $name.$chr.DI.wig
done

cat $name.*.insulation.wig >$name.all.DI.wig

for chr in ${chrList[*]}
do
    rm $name.$chr.DI.wig
done
