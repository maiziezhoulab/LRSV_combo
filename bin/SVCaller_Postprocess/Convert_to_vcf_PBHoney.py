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

def convert_spots_to_vcf(input, output):
    chrnums = ['chr'+str(i) for i in range(1,23)]
    
    with open(output,'w') as outfile:
        outfile.write(header)
        with open(input,'r') as infile:
            for line in infile:
                if line[0] != "#":
                    line = line.rstrip("\n").split("\t")
                    chrnum = line[0]
                    if chrnum in chrnums:
                        start = line[1]
                        svtype = line[3]
                        svlen = line[4]
                        if svtype == "DEL":
                            end = str(int(start)+int(svlen))
                            svlen = "-"+svlen
                        else:
                            end = start

                        support = line[5].split(";")[4].split("=")[1].split(".")[0]

                        outfile.write(chrnum+"\t"+start+"\t.\tN\t<"+svtype+">\t.\t.\tSVTYPE="+svtype+";END="+end+";SVLEN="+svlen+";SUPPORT="+support+"\tGT\t./.\n")

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

    convert_spots_to_vcf(input, output)