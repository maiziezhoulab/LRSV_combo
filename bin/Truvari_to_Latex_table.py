from Truvari_results_parser import read_truvari_summary
import os
import numpy as np

def parse_single_tool_truvari(truvari_results_dir,
                              table_value_dict,
                              supplementary_truvari_results_dir=None,
                              table_keys=["TP-call","FP","FN","recall","precision","f1"],):
    
    truvari_results_list = [d for d in next(os.walk(truvari_results_dir))[1]]

    for truvari_result in truvari_results_list:
        if truvari_result not in table_value_dict:
            table_value_dict[truvari_result] = dict()
            for key in table_keys:
                table_value_dict[truvari_result][key] = list()

        summary_file = truvari_results_dir+'/'+truvari_result+'/summary.txt'
        summary_dict = read_truvari_summary(summary_file)
        if supplementary_truvari_results_dir is not None:
            supp_summary_file = supplementary_truvari_results_dir+'/'+truvari_result+'/summary.txt'
            supp_summary_dict = read_truvari_summary(supp_summary_file)

        for key in table_keys:
            table_value = [None,None,0]

            if summary_dict[key] == 'NaN':
                table_value[0] = -1
            else:
                table_value[0] = summary_dict[key]

            if supplementary_truvari_results_dir is not None:
                if supp_summary_dict[key] == 'NaN':
                    table_value[1] = -1
                else:
                    table_value[1] = supp_summary_dict[key]

            # elif key in ["TP-call","FP","FN"]:
            #     table_value[0] = int(summary_dict[key])
            # elif key in ["precision","recall","f1"]:
            #     table_value[0] = float(summary_dict[key])

            table_value_dict[truvari_result][key].append(table_value)

    return table_value_dict

def cell_content_generator(cell_value,key):

    cell_content="& "
    if cell_value[2] == 1:
        cell_content += "\\cellcolor{green}"

    if cell_value[0] == -1:
        cell_content += "NAN "
    elif key in ["precision","recall","f1"]:
        cell_content += str(np.round(cell_value[0]*100,1))+"\\% "
    elif key in ["TP-call","FP","FN"]:
        cell_content += format(cell_value[0],",")+" "

    if cell_value[1] is not None:
        cell_content += "\\textcolor{blue}{("
        if cell_value[1] == -1:
            cell_content += "NAN"
        elif key in ["precision","recall","f1"]:
            cell_content += str(np.round(cell_value[1]*100,1))+"\\%"
        elif key in ["TP-call","FP","FN"]:
            cell_content += format(cell_value[1],",")
        cell_content += ")} "

    return cell_content

def truvari_to_latex_table(config_file,out_dir,table_keys=["TP-call","FP","FN","recall","precision","f1"]):

    table_value_dict = dict()
    with open(config_file,"r") as conf:
        for line in conf:
            if line[0]!="#":
                line = line.rstrip("\n").split("\t")
                if len(line) == 2:
                    line.append(None)
                table_value_dict = parse_single_tool_truvari(line[1],table_value_dict,line[2],table_keys)

    for sub_table_name,sub_table_content in table_value_dict.items():
        with open(out_dir+"/"+sub_table_name+".txt","w") as sub_table:
            for key in table_keys:
                if key in ["TP-call","FP","FN"]:
                    table_row = "& \\textbf{"+key[:2]+"} "
                if key in ["precision","recall","f1"]:
                    table_row = "& \\textbf{"+key.capitalize()+"} "
                    max_value = max(sub_table_content[key], key=lambda x: x[0])[0]
                    for i in range(len(sub_table_content[key])):
                        if sub_table_content[key][i][0] == max_value:
                            sub_table_content[key][i][2] = 1
                
                for i in range(len(sub_table_content[key])):
                    table_row += cell_content_generator(sub_table_content[key][i],key)

                table_row += "\\\\\n"
                sub_table.write(table_row)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--config_file','-i',)
    parser.add_argument('--out_dir','-o_dir')

    args = parser.parse_args()

    truvari_to_latex_table(args.config_file,args.out_dir,table_keys=["TP-call","FP","FN","recall","precision","f1"])