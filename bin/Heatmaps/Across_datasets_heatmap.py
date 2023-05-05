import os
import numpy as np
import pickle

# plot heatmap #
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import pandas as pd

from collections import OrderedDict
import math

all_keys=["TP-base","TP-call","FP","FN",\
        "precision","recall","f1",\
        "base cnt","call cnt",\
        "TP-call_TP-gt","TP-call_FP-gt","TP-base_TP-gt","TP-base_FP-gt",\
        "gt_precision","gt_recall","gt_f1"]

def read_truvari_summary(summary_file,decimals=None):
    try:
        with open(summary_file,"r") as sumryf:
            summary_dict=eval(sumryf.read())
    except:
        summary_dict = {i:np.nan for i in all_keys}
        return summary_dict

    for key in summary_dict.keys():
        if summary_dict[key] == 'NaN':
            summary_dict[key] = 0
        if decimals is not None:
            try:
                summary_dict[key] = np.round(summary_dict[key],decimals)
            except:
                pass

    return summary_dict

def heatmap_input_parser(input_dir,data_key="f1",tools=None): #data_key can be: "TP-call","FP","FN","recall","precision","f1","TP-call_TP-gt","TP-call_FP-gt","gt_recall","gt_precision","gt_f1"
    '''eg: data/svcaller/DEL_50_'''
    datasets = [i for i in next(os.walk(input_dir))[1]]
    datasets.sort()
    if tools is None:
        tools = list()
        for dataset in datasets:
            tools += [i for i in next(os.walk(input_dir+'/'+dataset))[1]]
        tools = list(set(tools))

    heat_map_data = OrderedDict()
    for tool in tools:
        heat_map_data[tool] = list()
        for dataset in datasets:
            for svtype in ['DEL',"INS"]:
                summary_dict = read_truvari_summary(input_dir+'/'+dataset+'/'+tool+'/'+svtype+'_50_/summary.txt')
                heat_map_data[tool].append(summary_dict[data_key])
    
    columns = list()
    for dataset in datasets:
        for svtype in ['DEL',"INS"]:
            columns.append(dataset+"_"+svtype)

    #heatmap_df = pd.DataFrame.from_dict(heat_map_data, orient='index',columns=columns)
    heatmap_df = pd.DataFrame.from_dict(heat_map_data, orient='index')
    heatmap_df.columns = columns

    return heatmap_df


def plot_heatmap(heatmap_df,save_dir,data_key,save_df=True):

    if save_df:
        with open(save_dir+'/'+data_key+'_across_datasets_heatmap_data.pkl','wb') as hmpk:
            pickle.dump(heatmap_df,hmpk)
    
    fig, ax = plt.subplots(figsize=(len(heatmap_df.columns)+1,len(heatmap_df.index)))
    #sns.heatmap(heatmap_df, annot=True, ax=ax,cmap='viridis',vmin=0, vmax=1,fmt='.1f',mask=heatmap_df.isnull())
    sns.heatmap(heatmap_df, annot=True, ax=ax,cmap='viridis',vmin=0, vmax=1,mask=heatmap_df.isnull())
    ax.xaxis.tick_top() # x axis on top
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    #plt.title(data_key)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig(save_dir+'/'+data_key+'_across_datasets_heatmap.pdf',bbox_inches='tight')
    plt.close()
    return 0


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input_dir', type=str,)
    parser.add_argument('--data_type', type=str,default="f1")
    parser.add_argument('--save_dir', type=str,default=".")
    args = parser.parse_args()

    input_dir = args.input_dir
    data_type = args.data_type
    save_dir = args.save_dir

    #heatmap_df = heatmap_input_parser(input_dir,data_key=data_type,)
    
    #Temporary solution for tool order
    tools=["PBHoney","NanoSV","Smartie-sv_aln","Sniffles","SVIM","cuteSV","NanoVar","pbsv","SKSV","Sniffles2","MAMnet","DeBreak","Dipcall","Smartie-sv_asm","SVIM-asm","PAV"]
    heatmap_df = heatmap_input_parser(input_dir,data_key=data_type,tools=tools)
    plot_heatmap(heatmap_df,save_dir,data_type,save_df=True)
