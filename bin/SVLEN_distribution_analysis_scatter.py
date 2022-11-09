import re
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def plot_svlen_distribution(caller_vcf_dict,intervals_label,save_dir,svtypes=['DEL','INS']):

    N=5
    width=0.25
    caller_types = list(caller_vcf_dict.keys()) #should be length 2
    ind=np.arange(N)+width*2
    for svtype in svtypes:
        color_cycle = plt.rcParams['axes.prop_cycle']()
        caller_name = dict()
        caller_data = dict()
        type_svcaller_pairs = list()
        for caller_type in caller_vcf_dict.keys():
            caller_name[caller_type] = list()
            caller_data[caller_type] = list()
            for sv_caller in caller_vcf_dict[caller_type].keys():
                caller_name[caller_type].append(sv_caller)
                caller_data[caller_type].append(caller_vcf_dict[caller_type][sv_caller][svtype])

                type_svcaller_pairs.append([caller_type,sv_caller])
            caller_data[caller_type] = np.array(caller_data[caller_type])

        fig, axes = plt.subplots(2,1,figsize=(10,8))
        axes[0].bar(ind-width/2,caller_data[caller_types[0]].mean(axis=0)[:N],width,color="gray",zorder=0)
        axes[1].bar(ind-width/2,caller_data[caller_types[0]].mean(axis=0)[N:],width,color="gray",label=caller_types[0]+'-based mean',zorder=0)
        axes[0].bar(ind+width/2,caller_data[caller_types[1]].mean(axis=0)[:N],width,color="silver",zorder=0)
        axes[1].bar(ind+width/2,caller_data[caller_types[1]].mean(axis=0)[N:],width,color="silver",label=caller_types[1]+'-based mean',zorder=0)

        for caller_type, sv_caller in type_svcaller_pairs:
            if caller_type == caller_types[0]:
                temp_ind = ind-width/2
            elif caller_type == caller_types[1]:
                temp_ind = ind+width/2
            color = next(color_cycle)['color']
            if color == "#7f7f7f":
                color = next(color_cycle)['color']
            axes[0].scatter(temp_ind,caller_data[caller_type][caller_name[caller_type].index(sv_caller)][:N],color=color)
            axes[1].scatter(temp_ind,caller_data[caller_type][caller_name[caller_type].index(sv_caller)][N:],color=color,label=sv_caller)

        for i in [0,1]:
            axes[i].set_ylabel("number of SVs")
            axes[i].set_xlabel("SV size")
            axes[i].set_xticks(ind)
        axes[0].set_xticklabels(intervals_label[:N])
        axes[1].set_xticklabels(intervals_label[N:])
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        axes[1].legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
        plt.savefig(save_dir+'/'+svtype+'_SVLEN_distribution.pdf',bbox_inches='tight')
        plt.close(fig)


def svlen_distribution_analysis(vlf,out_dir):

    caller_vcf_dict = dict()

    with open(vlf,'r') as vlf_file:
        for line in vlf_file:
            if line[0] != '#':
                sv_caller, vcf_dir,caller_type = line.rstrip('\n').split('\t')
                if caller_type not in caller_vcf_dict:
                    caller_vcf_dict[caller_type] = dict()
                caller_vcf_dict[caller_type][sv_caller] = vcf_dir

    # svlen50_1k = dict()
    # svlen1k_10k= dict()

    Intervals = [(50,200),(200,400),(400,600),(600,800),(800,1000),(1000,2500),(2500,5000),(5000,7500),(7500,10000),(10000,np.inf)]
    intervals_label = ['[50,200)','[200,400)','[400,600)','[600,800)','[800,1k)','[1k,2.5k)','[2.5k,5k)','[5k,7.5k)','[7.5k,10k)','[10k,inf)']

    for caller_type in caller_vcf_dict.keys():
        for sv_caller, vcf_file in caller_vcf_dict[caller_type].items():
            temp_store = dict()
            with open(vcf_file,'r') as vf:
                for line in vf:
                    if line[0] != '#':
                        try:
                            svtype = re.findall("SVTYPE=(\w+)",line)[0]
                            svlen = float(re.findall("SVLEN=-?(\d+)",line)[0])
                        except:
                            fields = line.rstrip('\n').split('\t')
                            if len(fields[3])-len(fields[4]) > 0:
                                svtype = 'DEL'
                            elif len(fields[3])-len(fields[4]) < 0:
                                svtype = 'INS'
                            svlen = abs(len(fields[3])-len(fields[4]))
                            svlen = float(svlen)

                        if svtype not in temp_store:
                            temp_store[svtype] = [0]*len(Intervals)

                        for i in range(len(Intervals)):
                            if Intervals[i][0] <= svlen < Intervals[i][1]:
                                temp_store[svtype][i] += 1
                                break

            caller_vcf_dict[caller_type][sv_caller] = temp_store

    plot_svlen_distribution(caller_vcf_dict,intervals_label,out_dir,svtypes=['DEL','INS'])




if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--vcf_list_file','-vlf',help='a file which has three columns seperated by tab, one for caller name, one for the location of corresponding vcf file, one for caller type, each line corresponds to one SV caller. Example line: cuteSV  path/to/cuteSV/vcf alignment')
    parser.add_argument('--out_dir','-o_dir')

    args = parser.parse_args()

    vlf = args.vcf_list_file
    out_dir = args.out_dir

    svlen_distribution_analysis(vlf,out_dir)
