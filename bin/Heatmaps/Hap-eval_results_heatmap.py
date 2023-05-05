import os
import numpy as np
import pickle

# plot heatmap #
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import math




def read_hap_eval_output(out_file):
    hapeval_results = list()
    with open(out_file,"r") as outf:
        for line in outf:
            if line[:3]=="pre":
                result=dict()
                pre_key,pre_value,rec_key,rec_value,f1_key,f1_value = line.rstrip("\n").split()
                result[pre_key] = float(pre_value)
                result[rec_key] = float(rec_value)
                result[f1_key] = float(f1_value)
                hapeval_results.append(result)
    if len(hapeval_results) != 2:
        raise ValueError("Missing or found extra Hap-eval output in "+out_file)

    return hapeval_results

def heatmap_hap_eval_results_parser(main_dir,tools,data_key="f1"): #data_key can be: "precision","f1","recall"
    valid_tools = [i for i in tools if os.path.isdir(main_dir+'/hap-eval_'+i+'_hm')]
    print("Valid tools for heatmap evaluation:",valid_tools)

    hap_eval_hms_del = dict()
    hap_eval_hms_ins = dict()
    maxdists=list()
    maxdiffs=list()

    for tool in valid_tools:
        for f in os.listdir(main_dir+'/hap-eval_'+tool+'_hm'):
            if f.endswith('.out'):
                _, maxdist, _, maxdiff = f[:-4].split("_")
                maxdists.append(maxdist)
                maxdiffs.append(maxdiff)
        maxdists = sorted(set(maxdists),key=lambda x: float(x))
        maxdiffs = sorted(set(maxdiffs),key=lambda x: float(x))
        hap_eval_hms_del[tool] = np.zeros((len(maxdists),len(maxdiffs)))
        hap_eval_hms_ins[tool] = np.zeros((len(maxdists),len(maxdiffs)))

        for i in range(len(maxdists)):
            for j in range(len(maxdiffs)):
                hapeval_results = read_hap_eval_output(main_dir+'/hap-eval_'+tool+'_hm/maxdist_'+maxdists[i]+'_maxdiff_'+maxdiffs[j]+'.out')
                hap_eval_hms_del[tool][i,j] = hapeval_results[0][data_key]
                hap_eval_hms_ins[tool][i,j] = hapeval_results[1][data_key]

    return valid_tools, hap_eval_hms_del, hap_eval_hms_ins, maxdists, maxdiffs

def truvari_results_heatmap(valid_tools, hap_eval_hms_del, hap_eval_hms_ins, maxdists, maxdiffs, save_dir, data_key="f1"):

    with open(save_dir+'/hap-eval_heatmap_DEL_data.pkl','wb') as hmdpk:
        pickle.dump(hap_eval_hms_del,hmdpk)
    with open(save_dir+'/hap-eval_heatmap_INS_data.pkl','wb') as hmipk:
        pickle.dump(hap_eval_hms_ins,hmipk)

    tool_num = len(valid_tools)
    col_hm = math.ceil(tool_num**0.5) 
    col = col_hm+1 #additional axis for colorbar
    row = math.ceil(tool_num/col_hm)

    fig, axes = plt.subplots(row,col,figsize=(col_hm*10+3,row*10),gridspec_kw={'width_ratios': [10]*col_hm+[0.5]},squeeze=False)
    mpl.rcParams['pdf.fonttype'] = 42
    for i, tool in enumerate(valid_tools):
        ax_row = i//col_hm
        ax_col = i%col_hm
        if ax_col == col_hm-1:
            sns.heatmap(hap_eval_hms_del[tool], annot=True, ax=axes[ax_row][ax_col],cmap="rainbow",vmin=0, vmax=1,fmt='.3f',cbar=True,cbar_ax=axes[ax_row][ax_col+1])
        else:
            sns.heatmap(hap_eval_hms_del[tool], annot=True, ax=axes[ax_row][ax_col],cmap="rainbow",vmin=0, vmax=1,fmt='.3f',cbar=False,)

        axes[ax_row][ax_col].set_xlabel("maxdiff")
        axes[ax_row][ax_col].set_ylabel("maxdist")
        axes[ax_row][ax_col].set_xticklabels(maxdiffs)
        axes[ax_row][ax_col].set_yticklabels(maxdists,rotation=0)
        axes[ax_row][ax_col].set_title(tool)

    plt.suptitle('DEL '+data_key+' hap-eval heatmap',y=0.95)
    plt.savefig(save_dir+'/DEL_'+data_key+'_hap-eval_heatmap.pdf',bbox_inches='tight')
    plt.close()

    fig, axes = plt.subplots(row,col,figsize=(col_hm*10+3,row*10),gridspec_kw={'width_ratios': [10]*col_hm+[0.5]},squeeze=False)
    mpl.rcParams['pdf.fonttype'] = 42
    for i, tool in enumerate(valid_tools):
        ax_row = i//col_hm
        ax_col = i%col_hm
        if ax_col == col_hm-1:
            sns.heatmap(hap_eval_hms_ins[tool], annot=True, ax=axes[ax_row][ax_col],cmap="rainbow",vmin=0, vmax=1,fmt='.3f',cbar=True,cbar_ax=axes[ax_row][ax_col+1])
        else:
            sns.heatmap(hap_eval_hms_ins[tool], annot=True, ax=axes[ax_row][ax_col],cmap="rainbow",vmin=0, vmax=1,fmt='.3f',cbar=False,)

        axes[ax_row][ax_col].set_xlabel("maxdiff")
        axes[ax_row][ax_col].set_ylabel("maxdist")
        axes[ax_row][ax_col].set_xticklabels(maxdiffs)
        axes[ax_row][ax_col].set_yticklabels(maxdists,rotation=0)
        axes[ax_row][ax_col].set_title(tool)

    plt.suptitle('INS '+data_key+' hap-eval heatmap',y=0.95)
    plt.savefig(save_dir+'/INS_'+data_key+'_hap-eval_heatmap.pdf',bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--data_type', type=str,default="f1")
    parser.add_argument('--save_dir', type=str,default=".")
    parser.add_argument('--input_dir', type=str,)
    args = parser.parse_args()

    data_type = args.data_type
    save_dir = args.save_dir
    main_dir = args.input_dir

    tools=["PBHoney","NanoSV","Smartie-sv_aln","Sniffles","SVIM","cuteSV","NanoVar","pbsv","SKSV","Sniffles2","MAMnet","DeBreak","Dipcall","Smartie-sv_asm","SVIM-asm","PAV"]

    valid_tools, hap_eval_hms_del, hap_eval_hms_ins, maxdists, maxdiffs = heatmap_hap_eval_results_parser(main_dir,tools,data_key=data_type)
    truvari_results_heatmap(valid_tools, hap_eval_hms_del, hap_eval_hms_ins, maxdists, maxdiffs, save_dir, data_key=data_type)
