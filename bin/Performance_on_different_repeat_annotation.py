import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def plot_perf_on_diff_rep_anno(result_df,tpfpfn_dict,lenth_distrb_dict,sv_caller,save_dir,topk):

    fig = plt.figure(figsize=(topk*3,10))

    ax = plt.subplot2grid((3, topk), (1, 0), colspan=topk,rowspan=2)
    result_df.plot.bar(ax=ax,)
    ax.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
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
    #ax.set_title('ax1_title')

    len_axes = list()
    for i in range(topk):
        len_axes.append(plt.subplot2grid((3, topk), (0, i),))
        plt.xticks(fontsize=7)
        plt.yticks(fontsize=7)
    
    for i,index in enumerate(result_df.index):
        len_axes[i].hist(lenth_distrb_dict[index],histtype='bar',) #n_bins,log=True


    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    plt.savefig(save_dir+'/'+sv_caller+'_performance_on_different_repeat_annotation.pdf',bbox_inches='tight')
    plt.close(fig)

def perf_on_diff_rep_anno(tp,fp,fn,sv_caller,save_dir,include_None_anno=False,topk=12):
    temp_annot_dict = dict()
    for file_name in [tp,fp,fn]:
        with open(file_name,'r') as f:
            for line in f:
                if line[0]!='#':
                    anno = line.split('\t')[-1].rstrip('\n')
                    svlen = int(line.split('\t')[1].split('_')[-1])
                    if anno in temp_annot_dict:
                        temp_annot_dict[anno][0] += 1
                        temp_annot_dict[anno][1].append(svlen)
                    else:
                        temp_annot_dict[anno]=[1,[svlen,]]

    anno_list = list()
    for key,value in temp_annot_dict.items():
        if not include_None_anno:
            if key=='None':
                continue
            else:
                anno_list.append([key,value[0],value[1]])
        else:
            anno_list.append([key,value[0],value[1]])
    anno_list = sorted(anno_list,key=lambda x: x[1],reverse=True)
    anno_list = anno_list[:topk]

    annos = [value[0] for value in anno_list]
    lenth_distrb_dict = {value[0]:value[2] for value in anno_list}

    tpfpfn_dict = dict()
    for key in ['TP','FP','FN']:
        tpfpfn_dict[key] = np.zeros(len(anno_list))

    for label,file_name in [('TP',tp),('FP',fp),('FN',fn)]:
        with open(file_name,'r') as f:
            for line in f:
                if line[0]!='#':
                    anno = line.split('\t')[-1].rstrip('\n')
                    if anno in annos:
                        tpfpfn_dict[label][annos.index(anno)] += 1

    result_dict = dict()
    result_dict['precision'] = tpfpfn_dict['TP']/(tpfpfn_dict['TP']+tpfpfn_dict['FP'])
    result_dict['recall'] = tpfpfn_dict['TP']/(tpfpfn_dict['TP']+tpfpfn_dict['FN'])
    result_dict['F1'] = 2*(result_dict['precision']*result_dict['recall'])/(result_dict['precision']+result_dict['recall'])

    result_df = pd.DataFrame(result_dict, index=annos,)

    plot_perf_on_diff_rep_anno(result_df,tpfpfn_dict,lenth_distrb_dict,sv_caller,save_dir,topk)


perf_on_diff_rep_anno('Sniffles_NA24385_CCS_NGMLR_TP_repeat_persentage_info.txt',
'Sniffles_NA24385_CCS_NGMLR_FP_repeat_persentage_info.txt',
'Sniffles_NA24385_CCS_NGMLR_FN_repeat_persentage_info.txt',
'Sniffles','.')