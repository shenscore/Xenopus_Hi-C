#!/usr/bin/awk -f
# input  : all calc_insulation_worker output of one chromosome
# output : insulation value of each bin


{
  C[$1] += $2
}

max_bin < $1 {
  max_bin = $1
}

END{
  for(i=1;i<=max_bin;i++){
    if(!(i in C)){C[i] = 0}
    print C[i]
  }
}

