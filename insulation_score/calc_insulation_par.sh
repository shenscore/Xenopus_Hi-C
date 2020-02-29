#!/bin/bash
# pipeline to calculate insulation score (KR normalized)
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
  echo "fixedStep chrom=$chr start=1 step="${res}" span="${res} > $name.$chr.insulation.wig
#  straw KR $hic_file $chr $chr BP $res | ${dir}/calc_DI.awk -v block_size=$block_size -v res=$res >> $name.$chr.DI
  straw VC_SQRT $hic_file $chr $chr BP $res | parallel --pipe -j $threads ${dir}/calc_insulation_worker.awk -v block_size=$block_size -v res=$res | ${dir}/calc_insulation_merge.awk >> $name.$chr.insulation.wig
done

cat $name.*.insulation.wig >$name.all.insulation.wig

for chr in ${chrList[*]}
do
    rm $name.$chr.insulation.wig
done

