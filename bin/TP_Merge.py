import re

header_fformat = '##fileformat=VCFv4.2\n'
header_chrome  = '''##contig=<ID=chr1,length=249250621>
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
'''
header_alt = '''##ALT=<ID=DEL,Description="Deletion">
##ALT=<ID=INV,Description="Inversion">
##ALT=<ID=DUP,Description="Duplication">
##ALT=<ID=INS,Description="Insertion">
##ALT=<ID=BND,Description="Breakend">
'''
# '''##ALT=<ID=DUP:TANDEM,Description="Tandem Duplication">
# ##ALT=<ID=DUP:INT,Description="Interspersed Duplication">
# '''
header_infofield='''##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=SC,Number=.,Type=String,Description="Source SV Caller">
##INFO=<ID=TruScore,Number=1,Type=Float,Description="Truvari score for similarity of match">
##INFO=<ID=BenchId,Number=1,Type=String,Description="Corresponding SV ID in Benchmark">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample
'''

def regularize_SV_record(line,sv_caller,SV_ID,symbolic_SV=False):

    fields = line.rstrip('\n').split('\t')
    format_field = fields[8].split(':')
    sample_field = fields[9].split(':')

    try:
        svtype = re.findall("SVTYPE=(\w+)",line)[0]
        svlen  = re.findall("SVLEN=(-?\d+)",line)[0]
        end    = re.findall("END=(\d+)",line)[0]
    except:
        if len(fields[3])-len(fields[4]) > 0:
            svtype = 'DEL'
        elif len(fields[3])-len(fields[4]) < 0:
            svtype = 'INS'
        svlen = abs(len(fields[3])-len(fields[4]))
        if svtype == 'DEL':
            end = str(int(fields[1])+svlen)
        else:
            end = fields[1]
        svlen = str(svlen)
    genotype = sample_field[format_field.index('GT')]
    TruScore = re.findall("TruScore=([\d\.]+)",line)[0]

    if not symbolic_SV:
        ref_seq=fields[3]
        alt_seq=fields[4]
    else:
        ref_seq='N'
        alt_seq='<'+svtype+'>'
    
    new_line = fields[0]+'\t'+fields[1]+'\t'+fields[2]+'\t'+\
        ref_seq+'\t'+alt_seq+'\t'+fields[5]+'\t'+fields[6]+'\t'+\
            'SVTYPE='+svtype+';END='+end+';SVLEN='+svlen+';SC='+sv_caller+";TruScore="+TruScore+";BenchId="+SV_ID+\
                '\tGT\t'+genotype+'\n'

    return new_line

def TP_merge_(merged_tp,sv_caller,tp_base,tp_call,symbolic_SV=False):

    MatchId_to_ID = dict()
    with open(tp_base,'r') as basef:
        for line in basef:
            if line[0]!="#":
                line = line.rstrip('\n').split('\t')
                ID = line[2]
                MatchId = int(re.findall("MatchId=(\d+)",line[7])[0])
                MatchId_to_ID[MatchId] = ID

    with open(tp_call,'r') as callf:
        for line in callf:
            if line[0]!="#":
                TruScore = float(re.findall("TruScore=([\d\.]+)",line)[0])
                MatchId = int(re.findall("MatchId=(\d+)",line)[0])
                SV_ID = MatchId_to_ID[MatchId]
                SV_record = regularize_SV_record(line,sv_caller,SV_ID,symbolic_SV)

                if SV_ID in merged_tp:
                    if merged_tp[SV_ID][0]<TruScore:
                        merged_tp[SV_ID] = [TruScore,SV_record]
                else:
                    merged_tp[SV_ID] = [TruScore,SV_record]

    return merged_tp


def TP_merge(input_list, out_dir, symbolic_SV=False):

    merged_tp=dict()
    sv_callers = list()

    with open(input_list,'r') as inlf:
        for line in inlf:
            if line[0]!='#':
                line = line.rstrip('\n').split('\t')
                sv_caller = line[0]
                sv_callers.append(sv_caller)
                tp_base = line[1]
                tp_call = line[2]
                merged_tp = TP_merge_(merged_tp,sv_caller,tp_base,tp_call,symbolic_SV)

    with open(out_dir+'/Merged_tp_from_'+'_'.join(sv_callers)+'.vcf','w') as new_vcf:
        new_vcf.write(header_fformat)
        new_vcf.write('##source='+'/'.join(sv_callers)+'\n')
        new_vcf.write(header_chrome)
        new_vcf.write(header_alt)
        new_vcf.write(header_infofield)

        for sv_line in merged_tp.values():
            new_vcf.write(sv_line[1])


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input_list','-i', type=str,)
    parser.add_argument('--out_dir','-o', type=str,default=".")
    parser.add_argument('--symbolic_SV','-symbsv',action='store_true')
    args = parser.parse_args()

    input_list = args.input_list
    out_dir = args.out_dir
    symbolic_SV = args.symbolic_SV

    TP_merge(input_list, out_dir, symbolic_SV)
