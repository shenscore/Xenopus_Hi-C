#!/usr/bin/awk -f
# input  : straw output of a chromosome
# output : DI value of each bin

function abs(v) {return v < 0 ? -v : v} #get absolute value

#BEGIN{
#  block_size = 40
#  res = 50000
#  max_bin = 0
#}

$2/res + 1 > max_bin{
  max_bin = $2/res + 1
}


$3 != "NaN" && ($2 - $1)/res <= block_size {
  A[$2/res] += $3
  B[$1/res] += $3
}
END{
  for(i=1;i<=max_bin;i++){
    if(!(i in A)){a = 0}else{a = A[i]}
    if(!(i in B)){b = 0}else{b = B[i]}
    if(!(a == 0 && b== 0)){
      print i,a,b
    }
  }
}

