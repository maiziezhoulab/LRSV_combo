from argparse import ArgumentParser
from tqdm import tqdm
import os
import json 
from collections import defaultdict,Counter
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--callvcf','-callvcf')
parser.add_argument('--outdir','-o')
parser.add_argument('--dist_thresh','-d',type = int, default = 500)
parser.add_argument('--min_size_sim','-P',type = float, default = 0.5)
parser.add_argument('--benchfile','-bench',help="optional, default = /data/maiziezhou_lab/Yichen/Projects/LRSV_Project/nc_review_analysis/SV_simulation/workdir/sim_dup.bed",
	default = "/data/maiziezhou_lab/Yichen/Projects/LRSV_Project/nc_review_analysis/SV_simulation/workdir/sim_dup.bed")

args = parser.parse_args()
callvcf = args.callvcf
outdir = args.outdir
dist_thresh = args.dist_thresh
benchfile = args.benchfile
min_size_sim = args.min_size_sim


os.system("mkdir -p " + outdir)


dc_gt={
	"1":1,
	"2":0,
	"3":1,
	"4":1,
	"5":0,
	"6":1,
	"7":0,
	"8":1,
	"9":0,
	"10":1,
	"11":0,
	"12":1,
	"13":0,
	"14":1,
	"15":0,
	"16":1,
	"17":0,
	"18":1,
	"19":0,
	"20":1,
	"21":0,
	"22":1,
	"X":0,
	"Y":0,
	"MT":0
}

## 0:homo; 1:het

def load_benchfile(benchfile):
	with open(benchfile,'r') as f:
		bench_list = []
		idx = 0
		for line in f:
			chrom,pos1,pos2 = line.split()[:3]
			pos1 = int(pos1)
			pos2 = int(pos2)
			gt = dc_gt[chrom]
			if gt == 0:
				gt = '1/1'
			else:
				gt = '0/1'

			bench_list.append((chrom,pos1,pos2,pos2-pos1,gt,idx))
			idx+=1
	return bench_list


def load_call(callvcf):
	call_list = []
	gt_list = []
	with open(callvcf,'r') as f:
		for line in f:
			if line[0]!='#':
				if 'SVTYPE=DUP' in line:
					data = line.split()
					chrom = data[0]
					pos1 = int(data[1])
					pos2 = int(data[7].split('END=')[1].split(';')[0])
					gt = data[-1].split(':')[0]
					if gt == '1|1':
						gt = '1/1'
					elif gt in {'0|1','1|0'}:
						gt = '0/1'
					gt_list.append(gt)
					call_list.append((chrom,pos1,pos2,pos2-pos1,gt,line))
	print(Counter(gt_list))
	return call_list 


def compare_inv(bench_list,call_list,min_size_sim,dist_thresh):
	tp_call = []
	tp_idx_list = []
	tp_gt_call = []
	tp_gt_idx_list = []
	for call in call_list:
		chrom,pos1,pos2,size,gt,line =  call 
		for bench in bench_list:
			chromb,pos1b,pos2b,sizeb,gtb,idxb =  bench
			if chrom == chromb:
				size_sim = min(size,sizeb)/max(size,sizeb)
				if size_sim >= min_size_sim:
					s1 = abs(pos1 - pos1b)
					s2 = abs(pos2 - pos2b)
					if (s1<= dist_thresh) & (s2 <= dist_thresh):
						tp_call.append(call)
						tp_idx_list.append(idxb)
						if gt == gtb:
							tp_gt_call.append(call)
							tp_gt_idx_list.append(idxb)
						break 

	return tp_call,tp_gt_call ,tp_idx_list,tp_gt_idx_list

def write_result(tp_call_list,tp_gt_call_list,tp_idx_list,tp_gt_idx_list,bench_list,call_list ):
	tp_bench = len(set(tp_idx_list))
	tp_call = len(tp_call_list)
	total_bench = len(bench_list)
	total_call = len(call_list)
	if total_call:

		fp = total_call - tp_call
		fn = total_bench - tp_bench
		recall = tp_bench / total_bench
		precision = tp_call / total_call
		if (recall+precision):
			f1 = recall * precision *2 / (recall+precision)
		else:
			f1 = 0


		tp_gt_bench = len(set(tp_gt_idx_list))
		tp_gt_call = len(tp_gt_call_list)

		recall_gt = tp_gt_bench / (fn + tp_gt_bench)
		precision_gt = tp_gt_call / total_call
		if recall_gt+precision_gt:
			f1_gt = recall_gt * precision_gt *2 / (recall_gt+precision_gt)
		else:
			f1_gt = 0

		dc = {"Total bench": total_bench,
			"Total call":total_call,
			"TP_bench": tp_bench,
			"TP_call": tp_call,
			"FP": fp,
			"recall": recall,
			"precision":precision,
			"f1":f1 ,
			"tp_gt_bench":tp_gt_bench,
			"tp_gt_call":tp_gt_call,
			"recall_gt":recall_gt,
			"precision_gt":precision_gt,
			"f1_gt":f1_gt
			}

		#### wirte tp-call.txt 
		with open(outdir+'/tp-call.vcf','w') as f:
			for i in range(len(tp_idx_list)):
				idx = tp_idx_list[i]
				line = tp_call_list[i][-1]
				data = line.split()
				data[7] = data[7]+';matching_bench_line_ID=%d'%(idx)
				line = '\t'.join(data)+'\n'
				f.write(line)
	else:
		dc = {"Total bench": total_bench,
			"Total call":total_call,
			"TP_bench": tp_bench,
			"TP_call": 0,
			"FP": 0,
			"recall": 0,
			"precision": 0,
			"f1": 0,
			"tp_gt_bench": 0,
			"tp_gt_call": 0,
			"recall_gt": 0,
			"precision_gt": 0,
			"f1_gt": 0
			}

	#### write summary.txt 
	outfile = outdir+'/summary.txt'
	print(dc)
	with open(outfile,'w') as f:
		json.dump(dc,f, indent = 4)
	return 


bench_list = load_benchfile(benchfile)
call_list = load_call(callvcf)
tp_call_list,tp_gt_call_list,tp_idx_list,tp_gt_idx_list = compare_inv(bench_list,call_list,min_size_sim,dist_thresh)
write_result(tp_call_list,tp_gt_call_list,tp_idx_list,tp_gt_idx_list,bench_list,call_list )





