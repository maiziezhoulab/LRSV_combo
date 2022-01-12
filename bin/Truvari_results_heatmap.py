import os
import numpy as np

# plot heatmap #
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(plot_info,save_dir,data_key,xtks,ytks):

    for SV_dir in plot_info.keys():
        fig, ax = plt.subplots(figsize=(10,8))
        #sns.heatmap(plot_info[SV_dir], annot=False, ax=ax,cmap="rainbow",vmin=0, vmax=1)
        sns.heatmap(plot_info[SV_dir], annot=True, ax=ax,cmap="rainbow",vmin=0, vmax=1,fmt='.3f')
        ax.set_xlabel("r")
        ax.set_ylabel("p")
        ax.set_xticklabels(xtks)
        ax.set_yticklabels(ytks)
        ax.set_title(SV_dir+data_key)
        plt.yticks(rotation=0)
        plt.ylabel('y',rotation=0)
        plt.savefig(save_dir+'/'+SV_dir+data_key+'_truvari_heatmap.png',bbox_inches='tight')
        plt.close()
    return 0

def read_truvari_summary(summary_file):
    with open(summary_file,"r") as sumryf:
        summary_dict=eval(sumryf.read())
    return summary_dict

def truvari_results_heatmap(truvari_results_dir,data_key="f1"): #data_key can be: "TP-call","FP","FN","recall","precision","f1","TP-call_TP-gt","TP-call_FP-gt","gt_recall","gt_precision","gt_f1"
    '''p_0.1_r_100/DEL_50_'''
    Truvari_config_list = [i for i in os.listdir(truvari_results_dir) if os.path.isdir(truvari_results_dir+'/'+i)]
    ps = list()
    rs = list()
    for config in Truvari_config_list:
        config = config.split('_')
        ps.append(float(config[1]))
        rs.append(float(config[3]))
    ps = sorted(set(ps))
    rs = sorted(set(rs))
    p_num = len(ps)
    r_num = len(ps)

    heat_map_data = dict()
    
    for config_dir in Truvari_config_list:
        SV_dirs = [i for i in os.listdir(truvari_results_dir+'/'+config_dir) if os.path.isdir(truvari_results_dir+'/'+config_dir+'/'+i)]
        p_index = np.round(float(config_dir.split('_')[1])/0.1-1).astype(int)
        r_index = np.round(float(config_dir.split('_')[3])/100-1).astype(int)
        for SV_dir in SV_dirs:
            if SV_dir not in heat_map_data:
                heat_map_data[SV_dir] = np.zeros((p_num,r_num))
            summary_dict = read_truvari_summary(truvari_results_dir+'/'+config_dir+'/'+SV_dir+'/summary.txt')
            if summary_dict[data_key] == 'NaN':
                summary_dict[data_key] = 0
            heat_map_data[SV_dir][p_index,r_index] = float(summary_dict[data_key])

    plot_heatmap(heat_map_data,truvari_results_dir,data_key,rs,ps)

    

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--truvari_results_dir', type=str,)
    parser.add_argument('--data_type', type=str,default="f1")
    args = parser.parse_args()

    truvari_results_dir = args.truvari_results_dir
    data_type = args.data_type

    truvari_results_heatmap(truvari_results_dir,data_type)