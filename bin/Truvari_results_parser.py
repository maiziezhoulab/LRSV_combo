import xlwt
import os
import numpy as np

def write_excel(path, value, sheet_name="Sheet1"):
    index = len(value)
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i,j,value[i][j])
    workbook.save(path)

def read_truvari_summary(summary_file):
    with open(summary_file,"r") as sumryf:
        summary_dict=eval(sumryf.read())
    return summary_dict

def truvari_results_parser(truvari_results_dir,):
    truvari_results_list = os.listdir(truvari_results_dir)
    content={
        "TP-call": list(),
        "FP": list(),
        "FN": list(),
        "precision": list(),
        "recall": list(),
        "f1": list(),
        "TP-call_TP-gt": list(),
        "TP-call_FP-gt": list(),
        "gt_precision": list(),
        "gt_recall": list(),
        "gt_f1": list()
        }

    content_items = ["TP-call","FP","FN","recall","precision","f1","TP-call_TP-gt","TP-call_FP-gt","FN","gt_recall","gt_precision","gt_f1"]

    for truvari_result in truvari_results_list:
        summary_file = truvari_results_dir+'/'+truvari_result+'/summary.txt'
        summary_dict = read_truvari_summary(summary_file)
        for key in content.keys():
            content[key].append(str(np.round(summary_dict[key],3)))

    excel_values = [["",]+truvari_results_list]
    for key in content_items:
        excel_values.append([key,]+content[key])

    write_excel(truvari_results_dir+'/Truvari_results.xls', excel_values, sheet_name="Sheet1")
    

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--truvari_results_dir', type=str,)
    args = parser.parse_args()

    truvari_results_dir = args.truvari_results_dir

    truvari_results_parser(truvari_results_dir,)