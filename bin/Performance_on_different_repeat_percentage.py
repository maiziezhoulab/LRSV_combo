import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def plot_perf_on_diff_rep_percent(result_df,tpfpfn_dict,sv_caller,save_dir):
    fig, ax = plt.subplots(figsize=(8,6))
    result_df.plot.bar(ax=ax,)
    ax.tick_params(axis='x',          # changes apply to the x-axis
                   which='both',      # both major and minor ticks are affected
                   bottom=False,      # ticks along the bottom edge are off
                   top=False,         # ticks along the top edge are off
                   labelbottom=False) # labels along the bottom edge are off
    cell_text = list()
    row_labels = list()
    for key,value in tpfpfn_dict.items():
        cell_text.append([str(int(i)) for i in value])
        row_labels.append(key)
    ax.table(cellText=cell_text, colLabels=result_df.index, rowLabels=row_labels, loc='bottom')

    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    plt.savefig(save_dir+'/'+sv_caller+'_performance_on_different_repeat_percentage.pdf',bbox_inches='tight')
    plt.close(fig)

def perf_on_diff_rep_percent(tp,fp,fn,sv_caller,save_dir):
    #0% 1~25% 25~50% 50~75% 75~100%
    intervals = [(0,25), (25,50), (50,75), (75,100)]
    index = ['0%', '1~25%', '25~50%', '50~75%', '75~100%']
    tpfpfn_dict = dict()
    for key in ['TP','FP','FN']:
        tpfpfn_dict[key] = np.zeros(len(index))
    for label,file_name in [('TP',tp),('FP',fp),('FN',fn)]:
        with open(file_name,'r') as f:
            for line in f:
                if line[0]!='#':
                    rep_perc = float(line.split('\t')[2].rstrip('%'))
                    if rep_perc == 0:
                        tpfpfn_dict[label][0]+=1
                    else:
                        for i in range(len(intervals)):
                            if intervals[i][0] < rep_perc <= intervals[i][1]:
                                tpfpfn_dict[label][i+1]+=1

    result_dict = dict()
    result_dict['precision'] = tpfpfn_dict['TP']/(tpfpfn_dict['TP']+tpfpfn_dict['FP'])
    result_dict['recall'] = tpfpfn_dict['TP']/(tpfpfn_dict['TP']+tpfpfn_dict['FN'])
    result_dict['F1'] = 2*(result_dict['precision']*result_dict['recall'])/(result_dict['precision']+result_dict['recall'])

    result_df = pd.DataFrame(result_dict, index=index,)

    plot_perf_on_diff_rep_percent(result_df,tpfpfn_dict,sv_caller,save_dir)




perf_on_diff_rep_percent('Sniffles_NA24385_CCS_NGMLR_TP_repeat_persentage_info.txt',
'Sniffles_NA24385_CCS_NGMLR_FP_repeat_persentage_info.txt',
'Sniffles_NA24385_CCS_NGMLR_FN_repeat_persentage_info.txt',
'Sniffles','.')