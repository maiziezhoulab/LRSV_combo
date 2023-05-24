from argparse import ArgumentParser
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--bedfile','-bed')
parser.add_argument('--outpath','-o')
args = parser.parse_args()
bedfile = args.bedfile
outpath = args.outpath


# @FF
# S1	N[S2[
# S1	]S2]N
# E1	]E2]N
# E1	N[E2[
# @RR
# S1	N]E2]
# S1	[E2[N
# E1	N]S2]
# E1	[S2[N
# @FR
# S1	N]E2]
# S1	]S2]N
# E1	N[E2[
# E1	[S2[N
# @RE
# S1	N[S2[
# S1	[E2[N
# E1	]E2]N
# E1	N]S2]

with open("bnd_format.txt",'r') as f:
	s = f.read().split('@')[1:]

dc_format = {}
for x in s:
	strand = x.split('\n')[0]
	dc_format[strand] = '\n'.join(x.split('\n')[1:])
print(dc_format)




idx = 0
finals = []
with open(bedfile,'r') as f:
	for line in f:
		data = line.split('\t')
		# print(data[4])
		chrom1 = 'chr'+data[0]
		start1 = int(data[1])
		end1 = int(data[2])
		chrom2 = 'chr'+data[4].split(':')[1]
		start2 = int(data[4].split(':')[2])
		end2 = start2 + (end1 - start1)
		dc = {}
		dc['S1'] = '%s\t%d'%(chrom1,start1)
		dc['E1'] = '%s\t%d'%(chrom1,end1)
		dc['S2'] = '%s:%d'%(chrom2,start2)
		dc['E2'] = '%s:%d'%(chrom2,end2)
		if "forward:forward" in line:
			strand = 'FF'
		if "forward:reverse" in line:
			strand = 'FR'
		if "reverse:forward" in line:
			strand = 'RF'
		if "reverse:reverse" in line:
			strand = 'RR'
		s = dc_format[strand]

		for key,val in dc.items():
			s = s.replace(key,val)
		s = s.split('\n')[:-1]

		for i in range(len(s)):
			s[i] = s[i] + '\tID=%d\n'%(idx)
		idx+=1
		finals.extend(s)

def translate(line):
	data = line.split()
	chrom1 = data[0]
	start1 = data[1]
	chrom2 = 'chr'+data[2].split('chr')[1].split(':')[0]

	if ']' in data[2]:
		start2 = data[2].split(':')[1].split(']')[0]
		sep = ']'
		sep_trans = '['
	else:
		start2 = data[2].split(':')[1].split('[')[0]
		sep = '['
		sep_trans = ']'

	data[0] = chrom2
	data[1] = start2

	x = data[2].split(sep) 
	x [1] = "%s:%s"%(chrom1,start1)
	data[2] = sep.join(x)


	if ("N[" in line ) or ("]N" in line):
		if data[2][0]=='N':
			data[2] = data[2][1:].replace(sep, sep_trans)+'N'
		else:
			data[2] = 'N'+data[2][:-1].replace(sep, sep_trans)
	return '\t'.join(data) + '\n'


		

finals1 = [ translate(line) for line in finals]




with open(outpath,'w') as f:
	f.writelines(finals)

with open(outpath+'.translate','w') as f:
	f.writelines(finals1)

























