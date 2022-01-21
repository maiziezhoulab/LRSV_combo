import re
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def plot_svlen_distribution(svlen50_1k,svlen1k_10k,sv_callers,save_dir,svtypes=['DEL','INS']):

    for svtype in svtypes:
        fig, axes = plt.subplots(2,1,figsize=(10,8))
        svlen50_1k_df = pd.DataFrame(svlen50_1k[svtype])
        svlen1k_10k_df = pd.DataFrame(svlen1k_10k[svtype])
        svlen50_1k_df.plot(x='Intervals', y=[sv_caller for sv_caller in sv_callers], ax=axes[0],kind="bar")
        axes[0].tick_params(axis='x', rotation=0)
        svlen1k_10k_df.plot(x='Intervals', y=[sv_caller for sv_caller in sv_callers], ax=axes[1], kind="bar")
        axes[1].tick_params(axis='x', rotation=0)
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.savefig(save_dir+'/'+svtype+'_SVLEN_distribution.pdf',bbox_inches='tight')
        plt.close(fig)


def svlen_distribution_analysis(vlf,out_dir):

    caller_vcf_dict = dict()

    with open(vlf,'r') as vlf_file:
        for line in vlf_file:
            if line[0] != '#':
                sv_caller, vcf_dir = line.rstrip('\n').split('\t')[:2]
                caller_vcf_dict[sv_caller] = vcf_dir

    svlen50_1k = dict()
    svlen1k_10k= dict()

    Intervals = [(50,200),(200,400),(400,600),(600,800),(800,1000),(1000,2500),(2500,5000),(5000,7500),(7500,10000),(10000,np.inf)]

    for sv_caller, vcf_file in caller_vcf_dict.items():
        temp_store = dict()
        with open(vcf_file,'r') as vf:
            for line in vf:
                if line[0] != '#':
                    svtype = re.findall("SVTYPE=(\w+)",line)[0]
                    svlen = float(re.findall("SVLEN=-?(\d+)",line)[0])

                    if svtype not in temp_store:
                        temp_store[svtype] = [0]*len(Intervals)

                    for i in range(len(Intervals)):
                        if Intervals[i][0] <= svlen < Intervals[i][1]:
                            temp_store[svtype][i] += 1
                            break

        for key,value in temp_store.items():
            if key not in svlen50_1k:
                svlen50_1k[key]=dict()
                svlen50_1k[key]['Intervals'] = ['[50,200)','[200,400)','[400,600)','[600,800)','[800,1k)']
            if key not in svlen1k_10k:
                svlen1k_10k[key]=dict()
                svlen1k_10k[key]['Intervals'] = ['[1k,2.5k)','[2.5k,5k)','[5k,7.5k)','[7.5k,10k)','[10k,inf)']
            svlen50_1k[key][sv_caller] = value[:len(svlen50_1k[key]['Intervals'])]
            svlen1k_10k[key][sv_caller] = value[len(svlen50_1k[key]['Intervals']):]


    plot_svlen_distribution(svlen50_1k,svlen1k_10k,list(caller_vcf_dict.keys()),out_dir,svtypes=['DEL','INS'])




if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--vcf_list_file','-vlf',help='a file which has two columns seperated by tab, one for caller name, one for the location of corresponding vcf file, each line corresponds to one SV caller. Example line: cuteSV  path/to/cuteSV/vcf')
    parser.add_argument('--out_dir','-o_dir')

    args = parser.parse_args()

    vlf = args.vcf_list_file
    out_dir = args.out_dir

    svlen_distribution_analysis(vlf,out_dir)
