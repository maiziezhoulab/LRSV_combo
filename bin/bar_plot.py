import os
import numpy as np

# plot heatmap #
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl


def read_truvari_summary(summary_file):
    with open(summary_file,"r") as sumryf:
        summary_dict=eval(sumryf.read())
    return summary_dict

def truvari_result_bar(truvari_results_dir,gtype):
    # truvari_results_list = os.listdir(truvari_results_dir)
    content={
        "precision": list(),
        "recall": list(),
        "f1": list(),
        "gt_precision": list(),
        "gt_recall": list(),
        "gt_f1": list(),
        }

    summary_file = truvari_results_dir+'/'+gtype+'/summary.txt'
    summary_dict = read_truvari_summary(summary_file)
    for key in content.keys():
        if summary_dict[key] == 'NaN':
            summary_dict[key] = 0
        try:
            content[key].append(np.round(summary_dict[key],3))
        except:
            content[key].append(summary_dict[key])
    return content

def bar_plot(ax, data,ylabel, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(['5x','5x','10x','20x','30x','40x','50x'])
    ax.set_ylim([0,1])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys(),bbox_to_anchor=(1.05, 0), loc=3)


# if __name__ == "__main__":
#     # Usage example:
#     data = {
#         "a": [1, 2, 3, 2, 1],
#         "b": [2, 3, 4, 3, 1],
#         "c": [3, 2, 1, 4, 2],
#         "d": [5, 9, 2, 1, 8],
#         "e": [1, 3, 2, 2, 3],
#         "f": [4, 3, 1, 1, 4],
#     }

#     fig, ax = plt.subplots()
#     bar_plot(ax, data, total_width=.8, single_width=.9)
#     plt.show()




if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--truvari_results_dir', type=str,default="Truvari_NGMLR_sniffles_aligned_results" )
    # parser.add_argument('--data_type', type=str, default="f1")
    args = parser.parse_args()

    truvari_results_dir = args.truvari_results_dir
    # data_type = args.data_type
    gtype = 'INS_50_'
    #gtype = 'DEL_50_'
    # tools = ['nanosv','smartie-sv','sniffles','svim','cutesv','nanovar'] # nanopore subsampling
    # tools = ['nanosv','smartie-sv','sniffles','svim','cutesv','nanovar','pbhoney','pbsv'] # pacbio hifi subsampling
    tools = ['pbhoney','nanosv','smartie-sv','sniffles','svim','cutesv','nanovar','pbsv','sksv'] # pacbio hifi subsampling
    subsampling = ['5x','10x','20x','30x','40x','50x']
    recall = {}
    precision = {}
    f1={}
    gt_recall = {}
    gt_precision ={}
    gt_f1 = {}
    for tool in tools:
        recall[tool] = []
        precision[tool] = []
        f1[tool] = []
        gt_recall[tool] = []
        gt_precision[tool] = []
        gt_f1[tool] = []
    for tool in tools:
        for sub in subsampling:
            dir_path = "rasusa-"+sub+"/vcfs/"+"Truvari_mmp2_"+tool+"_aligned_results"
            truvari = truvari_result_bar(dir_path,gtype)

            recall[tool].append(truvari['recall'][0])
            precision[tool].append(truvari['precision'][0])
            f1[tool].append(truvari['f1'][0])
            gt_recall[tool].append(truvari['gt_recall'][0])
            gt_precision[tool].append(truvari['gt_precision'][0])
            gt_f1[tool].append(truvari['gt_f1'][0])
    # print(recall,precision,f1)
    fig1, ax1 = plt.subplots()
    bar_plot(ax1, recall,'recall', total_width=.8, single_width=.9)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig('recall_'+gtype+'.pdf',bbox_inches='tight')
    plt.close()
    
    fig2, ax2 = plt.subplots()
    bar_plot(ax2, precision,'precision', total_width=.8, single_width=.9)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig('precision_'+gtype+'.pdf',bbox_inches='tight')
    plt.close()
    
    fig3, ax3 = plt.subplots()
    bar_plot(ax3, f1,'f1', total_width=.8, single_width=.9)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig('f1_'+gtype+'.pdf',bbox_inches='tight')
    plt.close()
    
    fig4, ax4 = plt.subplots()
    bar_plot(ax4, gt_recall,'gt_recall', total_width=.8, single_width=.9)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig('gt_recall_'+gtype+'.pdf',bbox_inches='tight')
    plt.close()
    
    fig5, ax5 = plt.subplots()
    bar_plot(ax5, gt_precision,'gt_precision', total_width=.8, single_width=.9)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig('gt_precision_'+gtype+'.pdf',bbox_inches='tight')
    plt.close()
    
    fig6, ax6 = plt.subplots()
    bar_plot(ax6, gt_f1,'gt_f1', total_width=.8, single_width=.9)
    mpl.rcParams['pdf.fonttype'] = 42
    plt.savefig('gt_f1_'+gtype+'.pdf',bbox_inches='tight')
    plt.close()

