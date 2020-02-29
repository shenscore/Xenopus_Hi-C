import numpy as np
import matplotlib.pyplot as plt


def get_obs_from_hic(hic_file,chr1,chr2,res=25e3,norm="KR"):
    juicer_tool_path = "/path/to/juicer_tools.jar"
    tmp_dir = "./hic_tmp/"
    out_file = tmp_dir + os.path.split(hic_file)[1] + ".tmp.obs." + chr1 + '_' + chr2 + "." + norm + "." + str(int(res))
    if os.path.exists(out_file):
        print("file tmp exists!\n use this file directly!\n")
    else:
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        os.system("java -jar " + juicer_tool_path + " dump observed " + norm +" " + hic_file + " " + chr1 + " " + chr2 + " BP " + str(int(res)) + " " + out_file)
    if chr1 == chr2:
        obs_mat = read_trip_mat(out_file,res)
    else:
        obs_mat = read_trip_mat_2(out_file,res)
    return obs_mat


def aggregate_TAD(hic_file,domain_file,res=5000,norm = 'KR'):
    
    
    domain = np.loadtxt(domain_file,dtype={'names':('chrom','start','end'),'formats':('<U5',np.int,np.int)})
    domain['start'] = domain['start']/res
    domain['end'] = domain['end']/res
    #chr_list = np.unique(domain['chrom'])
    
    sub_mat = np.zeros((100,100))
    for chr_ in np.nditer(np.unique(domain['chrom'])):
        chrom = str(chr_)
        print(chrom)
        obs = get_obs_from_hic(hic_file, chrom,chrom, res=res, norm=norm)
        obs.data[np.isnan(obs.data)] = 0
        domain_ = domain[domain['chrom'] == chr_]
        domain_len = domain_['end'] - domain_['start']
        # extract and resize image
        for i in range(domain_.shape[0]):
            start = domain_['start'][i]
            end   = domain_['end'][i]
            len_  = domain_len[i]
            #expand submatrix
            if(start - len_ > 0 and end + len_ < obs.shape[0]):
                start = start - len_
                end   = end + len_
            else:
                print("skip " + chrom + ' ' + str(start) + ' ' + str(end))
                next
            index = np.ix_(np.arange(start,end),np.arange(start,end))
            sub_mat_  = obs[index]
            sub_mat  += transform.resize(sub_mat_.toarray(), (100,100)) 
    
    # normlized by mean value
    sub_mat = sub_mat/np.mean(sub_mat)
    return sub_mat
    
def plot_aggregate_TAD(sub_mat,vmax=None,vmin=None,cmap_ = cm_custom_2,title=None):
    
    left, width    = 0.05, 0.8
    bottom, height = 0.1, 0.8
    size_heatmap   = [left, bottom, width, height]
    size_colorbar  = [left + width + 0.04, bottom + height/2 - height/6, width/25, height/3]
    lenth          = sub_mat.shape[0]
    
    fig = plt.figure(figsize=(8,8))
    ax     = fig.add_axes(size_heatmap)
    if vmax is None:
        vmax = np.percentile(sub_mat,90)
    if vmin is None:
        vmin = 0
    sc = ax.imshow(sub_mat, cmap = cmap_, vmin=vmin, vmax=vmax, interpolation = 'none',
               origin = 'upper',extent = (0, lenth, lenth, 0))
    ax.set_yticks([])
    ax.set_xticks([33,67])
    ax.set_xticklabels(["5'border","3'border"])
    ax.set_xlabel(title)
    ax = fig.add_axes(size_colorbar)
    fig.colorbar(sc,cax = ax, orientation = "vertical")
    return fig
    
    
def read_trip_mat(mat_file,res):
    """
    read in trip-format oe matrix output from juicer_tools
    """
    trip = np.loadtxt(mat_file)
    row_1 = trip[:,0]/res
    col_1 = trip[:,1]/res
    index = np.where(row_1 != col_1)[0]
    row_2 = col_1[index]
    col_2 = row_1[index]
    row = np.concatenate((row_1,row_2)).astype(int)
    col = np.concatenate((col_1,col_2)).astype(int)
    # value = np.log2(np.concatenate((trip[:,2],trip[:,2])))
    value = np.concatenate((trip[:,2],trip[:,2][index]))
    mat = csr_matrix((value,(row,col)))
    return mat

def read_trip_mat_2(mat_file,res):
    """
    read in trip-format oe matrix output from juicer_tools
    """
    trip = np.loadtxt(mat_file)
    row  = trip[:,0]/res
    col  = trip[:,1]/res
    
    value = trip[:,2]
    mat = csr_matrix((value,(row.astype(int),col.astype(int))))
    return mat    
