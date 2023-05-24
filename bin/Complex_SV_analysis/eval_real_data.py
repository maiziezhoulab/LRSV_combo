from argparse import ArgumentParser
import pandas as pd 
from collections import defaultdict
import numpy as np 
from tqdm import tqdm
import json 
import os
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--benchfile','-b')
parser.add_argument('--dist_thresh_tra','-rt',type = int, default = 1000, help = "default = 1000")
parser.add_argument('--dist_thresh_non_tra','-rnt',type = int, default = 500, help = "default = 500")
parser.add_argument('--min_size_sim','-P',type=float, default = 0.5, help = "default = 0.5")

args = parser.parse_args()
input_path = args.input_path
benchfile = args.benchfile
dist_thresh_tra = args.dist_thresh_tra
dist_thresh_non_tra = args.dist_thresh_non_tra
min_size_sim = args.min_size_sim

# benchfile = "/data/h_constantinidis_lab/ukbb/MaizieZhouLab_backup/Datasets/Cancer_Data/HCC1395/High_confidence_callset.xlsx"

def load_bench(benchfile):
	df = pd.read_excel(benchfile)
	dc = defaultdict(list)
	for i in range(df.shape[0]):
		svtype = df['SV_type'][i]
		if svtype in ['INS','DEL','DUP','INV','TRA']:
			chrom1 = df['Chrom1'][i]
			pos1 = df['Pos1'][i]
			chrom2 = df['Chrom2'][i]
			pos2 = df['Pos2'][i]
			svlen = df['SV_Size or breakpoints distance'][i]
			dc[svtype].append((chrom1,pos1,chrom2,pos2,svlen))
	print("bench set")
	for key in dc:
		print(key,len(dc[key]))
	return dc 

def load_callset(input_path):
	dc = defaultdict(list)
	with open(input_path,'r') as f:
		for line in f:
			if line[0]!='#':
				data = line.split()
				chrom = data[0]
				pos = int(data[1])
				svlen = int(data[7].split("SVLEN=")[1].split(';')[0])
				svtype = data[7].split("SVTYPE=")[1].split(';')[0]
				end = int(data[7].split("END=")[1].split(';')[0])
				if svtype in ['INS','DEL','DUP','INV','TRA']:
					if svtype=='TRA':
						if '[' in data[4]:
							sep = '['
						else:
							sep = ']'
						loc = data[4].split(sep)[1]
						chrom2 = loc.split(':')[0]
						pos2 = int(loc.split(':')[1])
						dc[svtype].append((chrom,pos,chrom2,pos2,0))
					else:
						dc[svtype].append((chrom,pos,chrom, end,svlen))
	print("call set")
	for key in dc:
		print(key,len(dc[key]))

	return dc 

def match_sv(sv_call,sv_bench,dist_thresh_tra,dist_thresh_non_tra,min_size_sim,tra_mode):
	chrom1c,pos1c,chrom2c,pos2c,svlenc = sv_call
	chrom1b,pos1b,chrom2b,pos2b,svlenb = sv_bench 
	if tra_mode:
		if ((chrom1c==chrom1b) & (chrom2c==chrom2b) &( abs(pos1c-pos1b) <= dist_thresh_tra) &( abs(pos2c-pos2b) <= dist_thresh_tra) )| ((chrom1c==chrom2b) & (chrom2c==chrom1b) &( abs(pos1c-pos2b) <= dist_thresh_tra) &( abs(pos2c-pos1b) <= dist_thresh_tra) ):
			return 1 
		else:
			return 0 
	else:
		svlenc = abs(svlenc)
		svlenb = abs(svlenb)
		size_sim = min(svlenb,svlenc)/max(svlenb,svlenc)
		if (chrom1c==chrom1b) & (chrom2c==chrom2b) &( abs(pos1c-pos1b) <= dist_thresh_non_tra) &( abs(pos2c-pos2b) <= dist_thresh_non_tra) & (size_sim>=min_size_sim):
			return 1 
		else:
			return 0


def compare_callset(dc_bench,dc_call,dist_thresh_tra,dist_thresh_non_tra,min_size_sim):
	dc_match = {}
	for svtype in dc_call:
		if svtype in dc_bench:
			call_list = dc_call[svtype]
			bench_list = dc_bench[svtype]
			match_list = []
			if svtype =='TRA':
				tra_mode = True 
			else:
				tra_mode = False 

			for sv_call in tqdm(call_list):
				match_idx = -1
				for i in range(len(bench_list)):
					sv_bench = bench_list[i]
					if match_sv(sv_call,sv_bench,dist_thresh_tra,dist_thresh_non_tra,min_size_sim,tra_mode):
						match_idx = i
						break
				match_list.append(match_idx)
			dc_match[svtype] = np.array(match_list)

		else:
			print(svtype, "not in bench file")
			match_list= [-1]*len(dc_call[svtype])
			dc_match[svtype] = np.array(match_list)

	#### calculate recall 
	dc_recall = {}
	dc_percision = {}
	for svtype in dc_bench:
		if svtype:
			if svtype in dc_call:

				match_list = dc_match[svtype]
				TP = len(set(match_list)) -1 
				recall = TP/len(dc_bench[svtype])
				dc_recall[svtype] = recall 
				dc_percision[svtype] = (match_list!=-1).mean()
			else:
				dc_recall[svtype] = 0
	print("========recall========")
	print(dc_recall)
	print("========precision========")
	print(dc_percision)
	outfile_rc = out_dir+'/recall.txt'
	outfile_pr = out_dir+'/precision.txt'
	with open(outfile_rc,'w') as f:
		json.dump(dc_recall,f, indent = 4)
	with open(outfile_pr,'w') as f:
		json.dump(dc_percision,f, indent = 4)
	return

		

dc_bench = load_bench(benchfile)
dc_call = load_callset(input_path)
out_dir = os.path.dirname(os.path.abspath(input_path))
compare_callset(dc_bench,dc_call,dist_thresh_tra,dist_thresh_non_tra,min_size_sim)















