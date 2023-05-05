import re
# import numpy as np
# import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# <ID=MatchId,Number=1,Type=Integer,Description="Truvari uid to help tie tp-base.vcf and tp-call.vcf entries together">


def plot_sequence_similarity_distribution(seqsim,save_dir,xlowerlimit=0.5,xupperlimit=1.0):

    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    fig, axes = plt.subplots(2,1,figsize=(8,16))
    axes[0].hist(seqsim['DEL'], bins=200, range=None, histtype='bar',log=False, color='blue',label='DEL')
    axes[1].hist(seqsim['INS'], bins=200, range=None, histtype='bar',log=False, color='red',label='INS')

    for i in range(2):
        axes[i].set_xlim(xmin=xlowerlimit, xmax=xupperlimit)
        
    axes[0].legend()
    axes[1].legend()
    plt.savefig(save_dir+'/sequence_similarity_distribution.pdf',bbox_inches='tight')
    plt.close(fig)


def sequence_similarity_analysis(truv_rslt_dir):

    #tp_base_vcf = truv_rslt_dir+'/tp-base.vcf'
    tp_call_vcf = truv_rslt_dir+'/tp-call.vcf'

    seqsim_dict = dict()

    with open(tp_call_vcf,'r') as vf:
        for line in vf:
            if line[0]!='#':
                #matchid = re.findall("MatchId=(\d+)",line)[0]
                #print(re.findall("PctSeqSimilarity=(\d*\.?\d*)",line))
                seqsim = float(re.findall("PctSeqSimilarity=(\d*\.?\d*)",line)[0])
                fields = line.rstrip('\n').split('\t')
                try:
                    svtype = re.findall("SVTYPE=(\w+)",line)[0]
                    #svlen = float(re.findall("SVLEN=-?(\d+)",line)[0])
                except:
                    if len(fields[3])-len(fields[4]) > 0:
                        svtype = 'DEL'
                    elif len(fields[3])-len(fields[4]) < 0:
                        svtype = 'INS'
                    #svlen = abs(len(fields[3])-len(fields[4]))
                    #svlen = float(svlen)

                if svtype not in seqsim_dict:
                    seqsim_dict[svtype] = [seqsim,]
                else:
                    seqsim_dict[svtype].append(seqsim)

    plot_sequence_similarity_distribution(seqsim_dict,truv_rslt_dir)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--truv_rslt_dir','-trd',)

    args = parser.parse_args()

    truv_rslt_dir = args.truv_rslt_dir

    sequence_similarity_analysis(truv_rslt_dir)
