#import numpy as np

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

'''chr1	121480372	D20	N	<DEL>	.	PASS	IMPRECISE;SVMETHOD=picky;END=121484101;SVTYPE=DEL;RE=2;RNAMES=m64015_190922_010918/19858208/ccs,m64012_190920_173625/57412007/ccs;SVLEN=3730;CIPOS=0,0;CIEND=-1,1;NOTE=CIPOS_CIEND;ISVTYPE=DEL(2)	GT	./.'''

def vcf_reformat(input, output):
    with open(input,'r') as infile:
        with open(output,'w') as outfile:
            outfile.write(header)
            for line in infile:
                if line[0] != '#':
                    fields = line.rstrip('\n').split('\t')
                    info = fields[7].split(';')
                    END = info[2]
                    SVTYPE = info[3]
                    SVLEN = info[6]
                    SUPPORT = 'SUPPORT='+info[4].split('=')[1]
                    if fields[6] != 'PASS':
                        fields[6] = '.'
                    outfile.write("\t".join(fields[:7])+"\t"+SVTYPE+";"+END+";"+SVLEN+";"+SUPPORT+"\t"+"\t".join(fields[-2:])+"\n")




if __name__ == '__main__':
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input', type=str,)
    parser.add_argument('--output', type=str,)
    args = parser.parse_args()

    input = args.input
    output = args.output

    vcf_reformat(input, output)