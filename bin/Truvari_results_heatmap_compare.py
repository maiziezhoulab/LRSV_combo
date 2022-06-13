import os
import numpy as np
import pickle

# plot heatmap #
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib as mpl

import math

def truvari_results_heatmap_compare(hm_file1,hm_file2,dataset_name1,dataset_name2,arg1,arg2,sv_type,tools,save_dir,data_key="f1"):
    #sv_tool_name\ttruvari_results_dir

    with open(hm_file1,"rb") as hmf1:
        hm1 = pickle.load(hmf1)
    with open(hm_file2,"rb") as hmf2:
        hm2 = pickle.load(hmf2)

    arg_pair = (arg1,arg2)
    print("SV types:",list(hm1.keys()))

    #heat_map_info[sv_type][arg_pair].append([line[0], args, heat_map_data[sv_type][arg_pair]])
    hm_compare = list()
    for tool in tools:
        temp = list()
        for i in hm1[sv_type][arg_pair]:
            if i[0]==tool:
                temp.append(i)
                break
        for i in hm2[sv_type][arg_pair]:
            if i[0]==tool:
                temp.append(i)
                break
        if len(temp)==1:
            tools.remove(tool)
            continue
        hm_compare.append([temp[0][0],temp[0][1],temp[0][2],temp[1][2]])

    col = math.ceil(len(tools)**0.5) 
    row = math.ceil(len(tools)/col)

    fig, axes = plt.subplots(row,col,figsize=(col*4+3,row*4))#figsize=(col_hm*10+3,row*10),gridspec_kw={'width_ratios': [10]*col_hm+[0.5]})
    mpl.rcParams['pdf.fonttype'] = 42
    for i, hm_info in enumerate(hm_compare):
        ax_row = i//col
        ax_col = i%col
        color_cycle = plt.rcParams['axes.prop_cycle']()
        if i==len(hm_compare)-1:
            for j in range(len(hm_info[2])):
                color = next(color_cycle)['color']
                axes[ax_row][ax_col].plot(hm_info[1][arg2],hm_info[2][j],color=color,linewidth=0.5,label=dataset_name1+" ("+arg1+"="+hm_info[1][arg1][j]+")")
                axes[ax_row][ax_col].plot(hm_info[1][arg2],hm_info[3][j],color=color,linewidth=0.5,linestyle='--',label=dataset_name2+" ("+arg1+"="+hm_info[1][arg1][j]+")")
                axes[ax_row][ax_col].legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
        else:
            for j in range(len(hm_info[2])):
                color = next(color_cycle)['color']
                axes[ax_row][ax_col].plot(hm_info[1][arg2],hm_info[2][j],color=color,linewidth=0.5)
                axes[ax_row][ax_col].plot(hm_info[1][arg2],hm_info[3][j],color=color,linewidth=0.5,linestyle='--')

        axes[ax_row][ax_col].set_title(hm_info[0])
        
        axes[ax_row][ax_col].set_xlabel(arg2)
        axes[ax_row][ax_col].set_ylabel(data_key.title(),rotation=0)
        axes[ax_row][ax_col].set_ylim(-0.05, 1)

        #axes[ax_row][ax_col].set_xticklabels(hm_info[1][arg1])
        #axes[ax_row][ax_col].set_yticklabels(hm_info[1][arg_pair[0]],rotation=0)

        plt.subplots_adjust(hspace=0.3, wspace=0.2)

        #plt.yticks(rotation=90)

    plt.suptitle(sv_type+' '+data_key.title()+' '+str(arg_pair),y=0.95)
    plt.savefig(save_dir+'/'+sv_type+data_key.title()+str(arg_pair)+'_truvari_heatmap_compare.pdf', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--hm1', type=str)
    parser.add_argument('--hm2', type=str)
    parser.add_argument('--dataname1', type=str)
    parser.add_argument('--dataname2', type=str)
    parser.add_argument('--arg1', type=str)
    parser.add_argument('--arg2', type=str)
    parser.add_argument('--sv_type', type=str)
    parser.add_argument('--tools', nargs="+")
    parser.add_argument('--data_type', type=str,default="f1")
    parser.add_argument('--save_dir', type=str,default=".")
    args = parser.parse_args()

    hm_file1 = args.hm1
    hm_file2 = args.hm2
    dataset_name1 = args.dataname1
    dataset_name2 = args.dataname2
    arg1 = args.arg1
    arg2 = args.arg2
    sv_type = args.sv_type
    tools = args.tools
    data_type = args.data_type
    save_dir = args.save_dir

    truvari_results_heatmap_compare(hm_file1,hm_file2,dataset_name1,dataset_name2,arg1,arg2,sv_type,tools,save_dir,data_type)