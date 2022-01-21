'''
#Support_Read_Number_Tag: The name of the variable that contains the support read number information
#Field: The name of the field that Support_Read_Number_Tag is in (INFO,FORMAT)
#Type: The type of the Support_Read_Number_Tag (number,count)
#Index: The index of the number that represents the supporting reads of the ALT in Support_Read_Number_Tag. If Type is 'count', this information is ignored (could be left blank)
#caller_name    vcf_file_dir    Support_Read_Number_Tag Field,Type,Index
'''
import re
import os

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
header_infofield='''##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=SUPPORT,Number=1,Type=Integer,Description="Number of reads supporting this variant">
##INFO=<ID=SC,Number=.,Type=String,Description="SV Caller(s) that supports this variant">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample
'''

def vcf_regularization(vlf,out_dir):

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    caller_vcf_dict = dict()

    with open(vlf,'r') as vlf_file:
        for line in vlf_file:
            if line[0] != '#':
                sv_caller, vcf_dir,SR_Tag,fti = line.rstrip('\n').split('\t')
                fti = fti.split(',')
                if fti[0] == 'INFO':
                    fti[0] = 7
                elif fti[0] == 'FORMAT':
                    fti[0] = 8
                try:
                    fti[2] = int(float(fti[2]))
                except:
                    pass
                caller_vcf_dict[sv_caller] = [vcf_dir,SR_Tag,fti]

    for sv_caller,vcf_info in caller_vcf_dict.items():
        vcf_dir = vcf_info[0]
        SR_Tag = vcf_info[1]
        field_index = vcf_info[2][0]
        info_type = vcf_info[2][1]
        try:
            info_index = vcf_info[2][2]
        except:
            pass

        header_alt=''
        with open(vcf_dir,'r') as ori_vcf:
            with open(out_dir+'/'+sv_caller+'_regularized_format.vcf','w') as new_vcf:
                new_vcf.write(header_fformat)
                new_vcf.write(header_chrome)

                for line in ori_vcf:
                    if line[0] == '#':
                        if '##ALT=' in line:
                            header_alt+=line
                    else:
                        break
                new_vcf.write(header_alt)
                new_vcf.write(header_infofield)
                
                for line in ori_vcf:
                    if line[0] != '#':
                        fields = line.rstrip('\n').split('\t')
                        ###################################
                        #if 'chr' not in fields[0]:
                        #    fields[0] = 'chr'+fields[0]
                        ###################################TODO:what if the input vcf is not filtered to only chr1-22
                        format_field = fields[8].split(':')
                        sample_field = fields[9].split(':')

                        svtype = re.findall("SVTYPE=(\w+)",line)[0]
                        svlen  = re.findall("SVLEN=(-?\d+)",line)[0]
                        end    = re.findall("END=(\d+)",line)[0]
                        genotype = sample_field[format_field.index('GT')]

                        if field_index==7:
                            if info_type=='number':
                                support = re.findall(SR_Tag+"=([\d,]+)",line)[0].split(',')[info_index]
                            elif info_type=='count':
                                support = str(len(re.findall(SR_Tag+"=([^;\t]+)",line)[0].split(',')))

                        elif field_index==8:
                            support_ = sample_field[format_field.index(SR_Tag)].split(',')
                            if info_type=='number':
                                support = support_[info_index]
                            elif info_type=='count':
                                support = str(len(support_))

                        new_line = fields[0]+'\t'+fields[1]+'\t'+fields[2]+'\tN\t<'+svtype+'>\t'+fields[5]+'\t'+fields[6]+'\t'+'SVTYPE='+svtype+';END='+end+';SVLEN='+svlen+';SUPPORT='+support+';SC='+sv_caller+'\tGT\t'+genotype+'\n'
                        new_vcf.write(new_line)



    


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--vcf_list_file','-vlf',)
    parser.add_argument('--out_dir','-o_dir')

    args = parser.parse_args()

    vlf = args.vcf_list_file
    out_dir = args.out_dir

    vcf_regularization(vlf,out_dir)
