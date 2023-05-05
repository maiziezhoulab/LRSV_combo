import os
import numpy as np

def read_truvari_summary(summary_file, decimals=None):
    all_keys=["TP-base","TP-call","FP","FN",\
        "precision","recall","f1",\
        "base cnt","call cnt",\
        "TP-call_TP-gt","TP-call_FP-gt","TP-base_TP-gt","TP-base_FP-gt",\
        "gt_precision","gt_recall","gt_f1"]
    try:
        with open(summary_file,"r") as sumryf:
            summary_dict=eval(sumryf.read())
    except:
        summary_dict = {i:-1 for i in all_keys}
        return summary_dict

    for key in summary_dict.keys():
        if summary_dict[key] == 'NaN':
            summary_dict[key] = -1
        if decimals is not None and key in ["precision","recall","f1","gt_precision","gt_recall","gt_f1"]:
            try:
                summary_dict[key] = np.round(summary_dict[key],decimals)
            except:
                pass

    return summary_dict

def parse_single_tool_truvari(truvari_results_dir,
                              table_value_dict,
                              all_fields,
                              table_keys=["TP-call","FP","FN","recall","precision","f1"]):
    
    #all_fields = [d for d in next(os.walk(truvari_results_dir))[1]]

    for field in all_fields:
        if field not in table_value_dict:
            table_value_dict[field] = dict()
            for key in table_keys:
                table_value_dict[field][key] = list()

        summary_file = truvari_results_dir+'/'+field+'/summary.txt'
        summary_dict = read_truvari_summary(summary_file)

        for key in table_keys:
            table_value = [None,None,0] #value(black), gt value(blue), if max (0 False, 1 True)
            table_value[0] = summary_dict[key]

            if key == "TP-call":
                table_value[1] = summary_dict["TP-call_TP-gt"]
            if key in ["recall","precision","f1"]:
                table_value[1] = summary_dict["gt_"+key]

            table_value_dict[field][key].append(table_value)

    return table_value_dict

def cell_content_generator(cell_value,key):

    cell_content="& "
    if cell_value[2] == 1:
        cell_content += "\\cellcolor{green}"

    if cell_value[0] == -1:
        cell_content += "N/A "
    elif key in ["precision","recall","f1"]:
        cell_content += str(np.round(cell_value[0]*100,1))+"\\% "
    elif key in ["TP-call","FP","FN"]:
        cell_content += format(cell_value[0],",")+" "

    if cell_value[1] is not None:
        cell_content += "\\textcolor{blue}{("
        if cell_value[1] == -1:
            cell_content += "N/A"
        elif key in ["precision","recall","f1"]:
            cell_content += str(np.round(cell_value[1]*100,1))+"\\%"
        elif key in ["TP-call","FP","FN"]:
            cell_content += format(cell_value[1],",")
        cell_content += ")} "

    return cell_content

def truvari_to_latex_table(in_dir,out_dir,tools):

    tools_available=list()
    all_fields=set()
    table_value_dict = dict()
    for tool in tools:
        tool_truvari_dir = os.path.join(in_dir, tool)
        if os.path.isdir(tool_truvari_dir):
            tools_available.append(tool)
            for fd in next(os.walk(tool_truvari_dir))[1]:
                all_fields.add(fd)

    for tool in tools_available:
        tool_truvari_dir = os.path.join(in_dir, tool)
        table_value_dict = parse_single_tool_truvari(tool_truvari_dir,table_value_dict,all_fields)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for sub_table_name,sub_table_content in table_value_dict.items():
        with open(out_dir+"/"+sub_table_name+".txt","w") as sub_table:
            sub_table.write("& "+" &".join(tools_available)+"\n")
            for key in ["TP-call","FP","FN","recall","precision","f1"]:
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

    parser.add_argument('--truvari_results','-i',help="the dir that contains the Truvari results. example: if you have Hifi/cuteSV/DEL_50_/summary.txt, Hifi/Sniffles/DEL_50_/summary.txt, then the input should be --truvari_results Hifi/")
    parser.add_argument('--out_dir','-o_dir',help="the dir to save the latex table, if not given, the output will be saved in Truvari_Latex_Tables under the same dir as --truvari_results")
    parser.add_argument('--tools',nargs="+",help="if given, only tools specified here will be outputed in the table (but if the folder for the tool does not exist, it will be ignored), and will be in the same order as specified here. If not given, will use the built-in tool list:PBHoney NanoSV Smartie-sv_aln Sniffles SVIM cuteSV NanoVar pbsv SKSV Sniffles2 MAMnet DeBreak Dipcall Smartie-sv_asm SVIM-asm PAV")

    args = parser.parse_args()
    
    in_dir = args.truvari_results
    if args.out_dir is None:
        out_dir = in_dir+"/Truvari_Latex_Tables/"
    else:
        out_dir = args.out_dir
    if args.tools is None:
        tools = ["PBHoney","NanoSV","Smartie-sv_aln","Sniffles","SVIM","cuteSV","NanoVar","pbsv","SKSV","Sniffles2","MAMnet","DeBreak","Dipcall","Smartie-sv_asm","SVIM-asm","PAV"]
    else:
        tools = args.tools

    truvari_to_latex_table(in_dir,out_dir,tools)#table_keys=["TP-call","FP","FN","recall","precision","f1"])
