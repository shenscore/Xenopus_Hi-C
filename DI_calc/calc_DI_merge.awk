#!/usr/bin/awk -f
# input  : all calc_DI_worker output of one chromosome
# output : DI value of each bin

function abs(v) {return v < 0 ? -v : v} #get absolute value


{
  A[$1] += $2
  B[$1] += $3
}

max_bin < $1 {
  max_bin = $1
}

END{
  for(i=1;i<=max_bin;i++){
    if(!(i in A)){a = 0}else{a = A[i]}
    if(!(i in B)){b = 0}else{b = B[i]}
    if(a == 0 && b== 0 || a == b){DI = 0} # avoid divide by 0 error
    else{
    e = (a+b)/2
    DI = ((b-a)/abs(b-a))*((a-e)^2/e + (b-e)^2/e)  # compute DI
    }
    print DI
  }
}

