from argparse import ArgumentParser
from tqdm import tqdm
import os
import json 
from collections import defaultdict
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--callvcf','-callvcf')
parser.add_argument('--outdir','-o')
parser.add_argument('--dist_thresh','-d',type = int, default = 1000)
parser.add_argument('--benchfile','-bench')

args = parser.parse_args()
callvcf = args.callvcf
outdir = args.outdir
dist_thresh = args.dist_thresh
benchfile = args.benchfile


os.system("mkdir -p " + outdir)


## load bed

def load_bench_pair(benchfile):
	with open(benchfile,'r') as f:
		s = f.readlines()
	def get_chroms(line):
		data = line.split()
		chr1 = data[0]
		pos1 = int(data[1])
		if '[' in data[2]:
			# print(data[2].split('['))
			chr2 = data[2].split('[')[1].split(':')[0]
			pos2 = int(data[2].split('[')[1].split(':')[1])
			x = data[2].split('[')
			x[1] = ''
			pattern = '['.join(x)
		else:
			# print(data[2].split(']'))
			chr2 = data[2].split(']')[1].split(':')[0]
			pos2 = int(data[2].split(']')[1].split(':')[1])
			x = data[2].split(']')
			x[1] = ''
			pattern = ']'.join(x)
		return chr1,pos1,chr2,pos2,pattern
	dc = defaultdict(list)
	for i in range(len(s)):
		line = s[i]
		chr1,pos1,chr2,pos2,pattern = get_chroms(line)
		dc[(chr1,chr2,pattern)].append([pos1,pos2,line[:-1]+'\tln=%d'%i])
	return dc 


def load_callset(callvcf):
	dc = defaultdict(list)
	with open(callvcf,'r') as f:
		for line in f:
			if line[0]!='#':
				if 'SVTYPE=BND' in line:
					data = line.split()
					chr1 = data[0]
					pos1 = int(data[1])
					alt = data[4]
					if '[' in alt:
						chr2 = alt.split('[')[1].split(':')[0]
						pos2 = int(alt.split('[')[1].split(':')[1])
						x = alt.split('[')
						x[1] = ''
						pattern = '['.join(x)
						if pattern[0]=='[':
							pattern = pattern[:2]+'N'
						else:
							pattern = 'N'+pattern[1:]

					else:
						chr2 = alt.split(']')[1].split(':')[0]
						pos2 = int(alt.split(']')[1].split(':')[1])
						x = alt.split(']')
						x[1] = ''
						pattern = ']'.join(x)
						if pattern[0]==']':
							pattern = pattern[:2]+'N'
						else:
							pattern = 'N'+pattern[1:]
					dc[('chr'+chr1,'chr'+chr2,pattern)].append([pos1,pos2,line])
	return dc 

def compare_tra(dc_bench,dc_call,dist_thresh,benchtype):
	## benchtype can be either "og" or "trans"
	dc_tp = {}
	# print(dc_bench.keys())
	# print(dc_call.keys())
	for key,val_list in dc_call.items():
		if key in dc_bench:
			# print(key)
			chr1,chr2,pattern = key
			for val in val_list:
				pos1,pos2,line = val
				for valb in dc_bench[key]:
					pos1b,pos2b,lineb = valb
					if (abs(pos1 - pos1b)<= dist_thresh) &  (abs(pos2 - pos2b)<= dist_thresh):
						dc_tp[(chr1,pos1,chr2,pos2,pattern)] = (line,pos1b,pos2b,lineb+'\tbtype='+benchfile)
						break
	return dc_tp

def combine_eval(dc_og,dc_ts):
	dc = defaultdict(list)
	dc_lines = {}
	all_tp = []
	for key in dc_og:
		tp_idx = int(dc_og[key][3].split('ln=')[1].split('btype')[0])
		dc[key].append(tp_idx)
		dc_lines[key] = dc_og[key][0]
		all_tp.append(tp_idx)
	for key in dc_ts:
		tp_idx = int(dc_ts[key][3].split('ln=')[1].split('btype')[0])
		dc[key].append(tp_idx)
		dc_lines[key] = dc_ts[key][0]
		all_tp.append(tp_idx)
	assert len(dc_lines) == len(dc)

	num_tp = len(set(all_tp))
	num_correct_call = len(dc)
	return dc,dc_lines,num_tp

def write_result(dc_call,dc_eval,dc_eval_lines,num_tp,benchfile):
	num_correct_call = len(dc_eval)
	with open(benchfile,'r') as f:
		num_bench = len(f.readlines())
	total_call = 0
	for key,val  in dc_call.items():
		total_call+=len(val)

	if total_call:
		recall = num_tp / num_bench 
		fp = total_call - num_correct_call 
		precision = num_correct_call / total_call 
		# print(num_tp,num_correct_call)
		f1 = precision*recall*2/ (precision+recall)
		dc = {"Total bench": num_bench,
		"Total call":total_call,
		"TP_bench": num_tp,
		"TP_call": num_correct_call,
		"FP": fp,
		"recall": recall,
		"precision":precision,
		"f1":f1 
		}

		#### write tp-call.vcf 
		with open(outdir+'/tp-call.vcf','w') as f:
			for key in dc_eval:
				ids = list(set(dc_eval[key]))
				ids = [str(idx) for idx in ids]
				line = dc_eval_lines[key]
				data = line.split()
				data[7] = data[7]+';matching_bench_line_ID='+':'.join(ids)
				f.write('\t'.join(data)+'\n')
	else:
		dc = {"Total bench": num_bench,
		"Total call":0,
		"TP_bench": 0,
		"TP_call": 0,
		"FP": 0,
		"recall": 0,
		"precision":0,
		"f1":0
		}


	#### write summary.txt 
	outfile = outdir+'/summary.txt'
	print(dc)
	with open(outfile,'w') as f:
		json.dump(dc,f, indent = 4)

	return 




dc_bench_og = load_bench_pair(benchfile)
# print(dc_bench_og)
dc_bench_ts = load_bench_pair(benchfile+'.translate')
dc_call = load_callset(callvcf)
dc_tp_og = compare_tra(dc_bench_og,dc_call,dist_thresh,benchtype = 'og')
dc_tp_ts = compare_tra(dc_bench_ts,dc_call,dist_thresh,benchtype = 'trans')
# print(dc_tp_og)
dc_eval,dc_eval_lines,num_tp = combine_eval(dc_tp_og,dc_tp_ts)
write_result(dc_call,dc_eval,dc_eval_lines,num_tp,benchfile)


























