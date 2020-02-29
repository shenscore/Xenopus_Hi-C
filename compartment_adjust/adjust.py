import numpy as np
import pyBigWig as pb

chr_list = ['Chr01','Chr02','Chr03','Chr04','Chr05','Chr06','Chr07','Chr08','Chr09','Chr10']


chip = ""
print('use file' + chip)
chip_bw = pb.open(chip)
bin_size  = 1e5
file_path = ""
out_      = ""
for chrom in chr_list:
	chr_eigen = np.loadtxt(file_path)
	nBin      = len(chr_eigen) - 1 # debug out of bound
	vals      = chip_bw.stats(chrom,0,int(bin_size*nBin),nBins=nBin)
	vals      = np.array([0.0 if x is None else x for x in vals])

# compare average signal enrichment
	pos_site  = np.where(chr_eigen[:-1] > 0)[0]
	neg_site  = np.where(chr_eigen[:-1] < 0)[0]
	pos_mean_signal = np.mean(vals[pos_site])
	neg_mean_signal = np.mean(vals[neg_site])

	if(neg_mean_signal > pos_mean_signal):
		chr_eigen = -chr_eigen
	out_file  = out_ + '_' + chrom + '_adjusted_eigen_100k'
	np.savetxt(out_file,chr_eigen)
