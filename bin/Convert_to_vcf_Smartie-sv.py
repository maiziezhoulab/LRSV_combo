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

'''chr1	899976	900051	deletion	75	+	m64015_190920_185703/27329313/ccs	11022	11022	13090	13063	13170	0.991875	TCCGCAGTGGGGATGTGCTGCGGGGAGGGGGGCGCGGGTCCGCAGTGGGGATGTGCTGCCGGGAGGGGGGCGCGG'''

# def merge_svs(sv_list):
#     if not sv_list:#if empty
#         return sv_list
    
#     merged_sv_list = list()
#     sv_list = sorted(sv_list, key =lambda x:x[0]) #sort by start position

#     temp_cluster = list()

#     for sv in sv_list:
#         if not temp_cluster: #if empty
#             temp_cluster.append(sv)
#         else:
#             current_cluster_avg = np.mean(temp_cluster,axis=0).astype(int)
#             if abs(sv[0]-current_cluster_avg[0])<=10 and abs(sv[1]-current_cluster_avg[1])<=10 and abs(sv[2]-current_cluster_avg[2])<=10:
#                 temp_cluster.append(sv)
#             else:
#                 merged_sv_list.append(list(current_cluster_avg).append(len(temp_cluster)))
#                 temp_cluster = list()
#                 temp_cluster.append(sv)

#     current_cluster_avg = np.mean(temp_cluster,axis=0).astype(int)
#     merged_sv_list.append(list(current_cluster_avg).append(len(temp_cluster)))

#     return merged_sv_list

def convert_svsbed_to_vcf(input, output):
    chrnums = ['chr'+str(i) for i in range(1,23)]

    SV_del_temp = dict()
    SV_ins_temp = dict()

    for chrnum in chrnums:
        SV_del_temp[chrnum] = list()
        SV_ins_temp[chrnum] = list()
    
    with open(input,'r') as infile:
        for line in infile:
            if line[0] != "#":
                line = line.rstrip("\n").split("\t")
                chrnum = line[0]
                if chrnum in chrnums:
                    start = int(line[1])
                    end   = int(line[2])
                    svlen = int(line[4])
                    if line[3] == 'deletion':
                        SV_del_temp[chrnum].append([start,end,svlen])
                    elif line[3] == 'insertion':
                        SV_ins_temp[chrnum].append([start,end,svlen])

    SV_del = dict()
    SV_ins = dict()
    
    # for chrnum in chrnums:
    #     if SV_del_temp[chrnum]: # if not empty
    #         SV_del[chrnum] = merge_svs(SV_del_temp[chrnum])
    #     if SV_ins_temp[chrnum]: # if not empty
    #         SV_ins[chrnum] = merge_svs(SV_ins_temp[chrnum])

    # with open(output,'w') as outfile:
    #     outfile.write(header)
    #     for chrnum, sv_info in SV_del.items():
    #         outfile.write(chrnum+"\t"+str(sv_info[0])+"\t.\tN\t<DEL>\t.\t.\tSVTYPE=DEL;END="+str(sv_info[1])+";SVLEN=-"+str(sv_info[2])+";SUPPORT="+str(sv_info[3])+"\tGT\t./.\n")

    #     for chrnum, sv_info in SV_ins.items():
    #         outfile.write(chrnum+"\t"+str(sv_info[0])+"\t.\tN\t<INS>\t.\t.\tSVTYPE=INS;END="+str(sv_info[1])+";SVLEN="+str(sv_info[2])+";SUPPORT="+str(sv_info[3])+"\tGT\t./.\n")

    

if __name__ == '__main__':
    import argparse
    import os
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input', type=str,default="./NA24385_hg19_Pacbio_CCS_NGMLR_Smartie-sv.svs.bed")
    parser.add_argument('--output', type=str,default="./NA24385_hg19_Pacbio_CCS_NGMLR_Smartie-sv.svs.vcf")
    args = parser.parse_args()

    input = args.input
    output = args.output

    convert_svsbed_to_vcf(input, output)