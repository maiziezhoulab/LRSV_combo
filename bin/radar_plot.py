# basic packages #
import os
import numpy as np
#plot
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt

def read_truvari_summary(summary_file):
    with open(summary_file,"r") as sumryf:
        summary_dict=eval(sumryf.read())
    return summary_dict

def radar_plot(sv_caller, perf_on_aligners, save_dir):
    mpl.rcParams['pdf.fonttype'] = 42
    fig,axis = plt.subplots(figsize=(10,10),subplot_kw={'projection': 'polar'})
    axis.set_theta_zero_location('N')
    axis.set_theta_direction(-1)
        
    axis.set_yticks([])
    axis.set_xticks(['DEL-Recall','DEL-Precision','INS-Recall','INS-Precision'])
    axis.set_rlim(0,1)

    theta = np.arange(0, 2 * np.pi + 0.00000001, np.pi / 2)

    for aligner_perf in perf_on_aligners:
        axis.plot(theta,aligner_perf[1],label=aligner_perf[0])

    title = sv_caller
    plt.suptitle(title)
    plt.legend()

    plt.savefig(save_dir+'/'+sv_caller+'.pdf',transparent=False)

    plt.close()

def truvari_result_parser(perf_on_aligners_list, save_dir):

    with open(perf_on_aligners_list,'r') as plf:
        for line in plf:
            if line[0]!='#':
                line = line.rstrip('\n').split('\t')
                sv_caller = line[0]
                perf_on_aligners = []
                for i in range(1,len(line),2):
                    summary_dict_DEL = read_truvari_summary(line[i+1]+'/DEL_50_/summary.txt')
                    summary_dict_INS = read_truvari_summary(line[i+1]+'/INS_50_/summary.txt')

                    perf_on_aligners.append(
                        [line[i],[summary_dict_DEL['recall'],summary_dict_DEL['precision'],summary_dict_INS['recall'],summary_dict_INS['precision']]])
    
                radar_plot(sv_caller, perf_on_aligners, save_dir)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--perf_on_aligners_list','-i', type=str,)
    parser.add_argument('--save_dir', type=str,default=".")
    args = parser.parse_args()

    perf_on_aligners_list = args.perf_on_aligners_list
    save_dir = args.save_dir

    truvari_result_parser(perf_on_aligners_list, save_dir)     