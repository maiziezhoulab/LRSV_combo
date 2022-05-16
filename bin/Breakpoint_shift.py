import re
# import numpy as np
# import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# <ID=MatchId,Number=1,Type=Integer,Description="Truvari uid to help tie tp-base.vcf and tp-call.vcf entries together">


def plot_breakpoint_shift_distribution(breakpoint_shift,save_dir):

    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    fig, axes = plt.subplots(2,1,figsize=(8,16))
    #del_max = abs(max(breakpoint_shift['DEL'], key=abs))
    axes[0].hist(breakpoint_shift['DEL'], bins=200, range=None, histtype='bar',log=False, color='blue',label='DEL')
    #axes[0].set_xlim(xmin=-500, xmax=500)
    axes[1].hist(breakpoint_shift['INS'], bins=200, range=None, histtype='bar',log=False, color='red',label='INS')
    #center at zero
    for i in range(2):
        # xabs_max = abs(max(axes[i].get_xlim(), key=abs))
        # axes[i].set_xlim(xmin=-xabs_max, xmax=xabs_max)
        axes[i].set_xlim(xmin=-210, xmax=210)
        
    axes[0].legend()
    axes[1].legend()
    plt.savefig(save_dir+'/breakpoint_shift_distribution.pdf',bbox_inches='tight')
    plt.close(fig)

def group_by_matchid(vcf):

    brkpt_dict = dict()

    with open(vcf,'r') as vf:
        for line in vf:
            if line[0]!='#':
                matchid = re.findall("MatchId=(\d+)",line)[0]
                fields = line.rstrip('\n').split('\t')

                try:
                    svtype = re.findall("SVTYPE=(\w+)",line)[0]
                    svlen = float(re.findall("SVLEN=-?(\d+)",line)[0])
                except:
                    if len(fields[3])-len(fields[4]) > 0:
                        svtype = 'DEL'
                    elif len(fields[3])-len(fields[4]) < 0:
                        svtype = 'INS'
                    svlen = abs(len(fields[3])-len(fields[4]))
                    svlen = float(svlen)

                start = float(fields[1])
                if svtype == 'DEL':
                    end = start+svlen
                elif svtype == 'INS':
                    end = start

                brkpt_dict[matchid] = [svtype, start, end]

    return brkpt_dict


def breakpoint_shift_analysis(truv_rslt_dir):

    tp_base_vcf = truv_rslt_dir+'/tp-base.vcf'
    tp_call_vcf = truv_rslt_dir+'/tp-call.vcf'

    base_brkpt = group_by_matchid(tp_base_vcf)
    call_brkpt = group_by_matchid(tp_call_vcf)

    breakpoint_shift = dict()
    for svtype in ['DEL','INS']:
        breakpoint_shift[svtype] = list()

    for matchid in base_brkpt.keys():
        base_bp = base_brkpt[matchid]
        call_bp = call_brkpt[matchid]

        svtype = base_bp[0]

        bp_shift = max([call_bp[1]-base_bp[1],call_bp[2]-base_bp[2]], key=abs)
        #clip
        if bp_shift<=-201:
            bp_shift = -201
        if bp_shift>=201:
            bp_shift = 201

        breakpoint_shift[svtype].append(bp_shift)

    plot_breakpoint_shift_distribution(breakpoint_shift,truv_rslt_dir)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--truv_rslt_dir','-trd',)

    args = parser.parse_args()

    truv_rslt_dir = args.truv_rslt_dir

    breakpoint_shift_analysis(truv_rslt_dir)