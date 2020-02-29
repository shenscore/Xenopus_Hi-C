#!/usr/bin/awk -f
# input  : straw output of a chromosome
# output : insulation score value of each bin

#BEGIN{
#  block_size = 40
#  res = 50000
#  max_bin = 0
#}

$2/res + 1 > max_bin{
  max_bin = $2/res + 1
}


$3 != "NaN" && ($2 - $1)/res <= 2*block_size && ($2 -$1)/res > 1 {
    dis = ($2 -$1)/res
    if(dis <= block_size + 1){
	left = $1/res + 1
	right = $1/res + dis -1
    }else{
        left = $1/res + dis - block_size
	right = $1/res + block_size
    }
    for(i=left;i<=right;i++){
        C[i] += $3
    }
}
END{
  for(i=1;i<=max_bin;i++){
    if(i in C){
      print i,C[i]
    }
  }
}

