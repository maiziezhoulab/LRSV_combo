import numpy as np

header = '''##fileformat=VCFv4.2
##contig=<ID=chr1,length=249250621>
##contig=<ID=chr2,length=243199373>
##contig=<ID=chr3,length=198022430>
##contig=<ID=chr4,length=191154276>
##contig=<ID=chr5,length=180915260>
##contig=<ID=chr6,length=171115067>
##contig=<ID=chr7,length=159138663>
##contig=<ID=chr8,length=146364022>
##contig=<ID=chr9,length=141213431>
##contig=<ID=chr10,length=135534747>
##contig=<ID=chr11,length=135006516>
##contig=<ID=chr12,length=133851895>
##contig=<ID=chr13,length=115169878>
##contig=<ID=chr14,length=107349540>
##contig=<ID=chr15,length=102531392>
##contig=<ID=chr16,length=90354753>
##contig=<ID=chr17,length=81195210>
##contig=<ID=chr18,length=78077248>
##contig=<ID=chr19,length=59128983>
##contig=<ID=chr20,length=63025520>
##contig=<ID=chr21,length=48129895>
##contig=<ID=chr22,length=51304566>
##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=INS,Description="Insertion">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=SUPPORT,Number=1,Type=Integer,Description="Number of reads supporting this variant">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	Sample
'''

def construct_line(sv_info,gt):
    info = 'SVTYPE='+sv_info[1][0]+';END='+sv_info[1][1]+';SVLEN='+sv_info[1][2]+';SUPPORT='+str(sv_info[1][3])
    sv_info[0].append(info)
    sv_info[0].append('GT')
    if gt=='hete':
        GT='0/1'
    elif gt=='homo':
        GT='1/1'

    sv_info[0].append(GT)

    line = '\t'.join(sv_info[0])+'\n'

    return line

def merge_vcf(input1,input2,output):

    in1_dict=dict()
    in2_dict=dict()

    out=list()

    for input_file,sv_dict in [(input1,in1_dict),(input2,in2_dict)]:
        with open(input_file,'r') as infile:
            for line in infile:
                if line[0]!='#':
                    line = line.rstrip('\n').split('\t')
                    
                    info_ = line[7].split(';')
                    info = [i.split('=')[1] for i in info_] 
                    info[-1] = int(info[-1])

                    sv_dict[(line[0],line[1],info[0],info[1])] = [line[:7],info]

    for key,value in in1_dict.items():
        if key in in2_dict:
            out.append(construct_line(value,'homo'))
        else:
            out.append(construct_line(value,'hete'))

    for key,value in in2_dict.items():
        if key not in in1_dict:
            out.append(construct_line(value,'hete'))

    with open(output,'w') as outf:
        outf.write(header)
        for line in out:
            outf.write(line)


if __name__ == '__main__':
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input1', type=str,)
    parser.add_argument('--input2', type=str,)
    parser.add_argument('--output', type=str,)
    args = parser.parse_args()

    input1 = args.input1
    input2 = args.input2
    output = args.output

    merge_vcf(input1,input2,output)