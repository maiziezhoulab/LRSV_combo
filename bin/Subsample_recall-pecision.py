import os
import numpy as np

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.lines as mlines

#colors=['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
colors=['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#800000', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']
tls=['pbhoney','nanosv','smartie-sv_aln','sniffles','svim','cutesv','nanovar','pbsv','sksv','sniffles2','mamnet','debreak','dipcall', 'pav','smartie-sv_asm','svim-asm']

color_dict = dict()
for i in range(len(tls)):
    color_dict[tls[i]]=colors[i]

#markers=["o","^","*","s","H","D"]
markers=["o","^","*","s","H"]
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

    for key in summary_dict.keys():
        if summary_dict[key] == 'NaN':
            summary_dict[key] = 0
        if decimals is not None:
            try:
                summary_dict[key] = np.round(summary_dict[key],decimals)
            except:
                pass

    return summary_dict

def main_plot(recalls, precisions, SVtype, subsample_covs, recalls_gt=None, precisions_gt=None, outdir="./"):

    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42

    fig, ax = plt.subplots(figsize=(8, 8),dpi=300)

    ax.set_xlim(-0.02, 1)
    ax.set_ylim(-0.05, 1.02)

    #plot f1 contour lines
    f1x = np.linspace(0.0, 1.0, num=100)
    for i in [x * 0.1 for x in range(1, 10)]:
        f1y=i*f1x/(2*f1x-i)
        ax.plot(f1x, np.ma.masked_where(f1y <= 0, f1y), color='gray', linestyle='--',zorder=0)
        ax.annotate("F1="+str(np.round(i,1)), (1.0, f1y[-1]-0.01), va='top', ha='right',zorder=len(recalls.keys())+1)

    #plot lines for tools
    dot_alpha=0.5
    lw=1
    mksize = [i**1.5*8 for i in range(1,len(subsample_covs)+1)]
    for j, tool in enumerate(recalls.keys()):
        ax.plot([i for i in recalls[tool] if not np.isnan(i)], [i for i in precisions[tool] if not np.isnan(i)], label=tool, zorder=j+1,color=color_dict[tool.lower()],linewidth=lw,alpha=0.9)
        #ax.plot(recalls[tool], precisions[tool], label=tool, zorder=j+1,color=color_dict[tool.lower()],linewidth=lw,alpha=0.9)
        #ax.scatter(recalls[tool], precisions[tool], s=mksize, zorder=j+1, c=colors[j],alpha=dot_alpha,)
        for i in range(len(subsample_covs)):
            ax.scatter(recalls[tool][i], precisions[tool][i], s=50, zorder=j+1, c=color_dict[tool.lower()],marker=markers[i], alpha=dot_alpha)

        # ax.plot(precisions[tool], recalls[tool], label=tool, zorder=j+1)
        # ax.scatter(precisions[tool], recalls[tool], s=mksize, zorder=j+1)

        if precisions_gt is not None and recalls_gt is not None:
            ax.plot([i for i in recalls_gt[tool] if not np.isnan(i)], [i for i in precisions_gt[tool] if not np.isnan(i)], zorder=j+1, color=color_dict[tool.lower()], linestyle='-.', linewidth=lw, alpha=0.9)
            #ax.plot(recalls_gt[tool], precisions_gt[tool], zorder=j+1, color=color_dict[tool.lower()], linestyle='-.', linewidth=lw, alpha=0.9)
            #ax.scatter(recalls_gt[tool], precisions_gt[tool], marker="^", s=mksize, zorder=j+1,c=colors[j],alpha=dot_alpha)
            for i in range(len(subsample_covs)):
                ax.scatter(recalls_gt[tool][i], precisions_gt[tool][i], marker=markers[i], s=50, zorder=j+1,c=color_dict[tool.lower()], alpha=dot_alpha)


    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    # ax.set_xlabel("Precision")
    # ax.set_ylabel("Recall")

    #ax.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    legend_lines = ax.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
    ax.add_artist(legend_lines)

    #f = lambda m,c,s: plt.plot([],[],marker=m, color=c, markersize=s, ls="none")[0]
    #handles = [f("o", "black", s**0.5) for s in mksize]
    #labels = subsample_covs
    #if precisions_gt is not None and recalls_gt is not None:
    #    handles += [f("^", "black", s**0.5) for s in mksize]
    #    labels += [i+"_gt" for i in subsample_covs]

    f = lambda m,c,s,l, lw: plt.plot([],[],marker=m, color=c, markersize=s, ls=l, linewidth=lw)[0]
    handles = [f(i, "black", 40**0.5,'-', lw) for i in markers]
    labels = subsample_covs
    if precisions_gt is not None and recalls_gt is not None:
        handles += [f(i, "black", 40**0.5, '-.', lw) for i in markers]
        labels += [i+"_gt" for i in subsample_covs]

    legend_shapes = ax.legend(handles, labels, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)

    
    plt.savefig(outdir+'/'+SVtype+'_Recall-Precision-F1.eps',bbox_inches='tight')
    plt.savefig(outdir+'/'+SVtype+'_Recall-Precision-F1.png',bbox_inches='tight')
    plt.savefig(outdir+'/'+SVtype+'_Recall-Precision-F1.pdf',bbox_inches='tight')
    ax.set_xlim(0.75, 1)
    ax.set_ylim(0.75, 1.02)
    plt.savefig(outdir+'/'+SVtype+'_Recall-Precision-F1_zoomin.eps',bbox_inches='tight')
    plt.savefig(outdir+'/'+SVtype+'_Recall-Precision-F1_zoomin.png',bbox_inches='tight')
    plt.savefig(outdir+'/'+SVtype+'_Recall-Precision-F1_zoomin.pdf',bbox_inches='tight')
    plt.close(fig)


if __name__ == '__main__':
    tools = ['nanosv','smartie-sv_aln','sniffles','svim','cutesv','nanovar','sniffles2','mamnet','debreak'] # nanopore subsampling
    subsampling = ['5x','10x','20x','30x','40x']
    SVtype = 'DEL'
    #SVtype = 'INS'
    recall = {}
    precision = {}
    gt_recall = {}
    gt_precision ={}

    for tool in tools:
        recall[tool] = []
        precision[tool] = []
        gt_recall[tool] = []
        gt_precision[tool] = []

    for tool in tools:
        for sub in subsampling:
            #Need to change this:
            summary_file = "Truvari_for_subsample_ALN_plot_p0_new/"+tool+"/"+sub+"_"+SVtype+"/summary.txt"
            #################################################

            truvari = read_truvari_summary(summary_file,decimals=None)

            recall[tool].append(truvari['recall'])
            precision[tool].append(truvari['precision'])
            gt_recall[tool].append(truvari['gt_recall'])
            gt_precision[tool].append(truvari['gt_precision'])

    main_plot(recall, precision, SVtype, subsampling, gt_recall, gt_precision)
