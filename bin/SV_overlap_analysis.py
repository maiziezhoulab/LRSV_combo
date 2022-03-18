#content in vcf_list_file:
'''
#Support_Read_Number_Tag: The name of the variable that contains the support read number information
#Field: The name of the field that Support_Read_Number_Tag is in (INFO,FORMAT)
#Type: The type of the Support_Read_Number_Tag (number,count)
#Index: The index of the number that represents the supporting reads of the ALT in Support_Read_Number_Tag. If Type is 'count', this information is ignored (could be left blank)
#caller_name    vcf_file_dir    Support_Read_Number_Tag(optional) Field,Type,Index(optional)
'''
#content in truvari_config_file:
'''
#Truvari parameters for overlap analysis
#truvari bench -b benchmark.vcf.gz -c comp.vcf.gz -o ${out_dir} -> this part will be handled by the script
#the other parameters shoud be specified in this file
#example line:
#-f ${ref} --includebed ${bed} -p 0.5 -P 0.5 -r 500 --passonly --sizemin 50
'''


import re
import os
from collections import OrderedDict

import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


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
##INFO=<ID=SC,Number=.,Type=String,Description="SV Caller(s) that supports this variant">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample
'''

def vcf_regularization(vlf,out_dir,output_reg_vcfs=True):

    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    caller_vcf_dict = OrderedDict()

    with open(vlf,'r') as vlf_file:
        for line in vlf_file:
            if line[0] != '#':
                if len(line.rstrip('\n').split('\t'))==4:
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
                elif len(line.rstrip('\n').split('\t'))==2:
                    sv_caller, vcf_dir = line.rstrip('\n').split('\t')
                    SR_Tag=None
                    fti = [None,None,None]
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
                new_vcf.write('##source='+sv_caller+'\n')
                new_vcf.write(header_chrome)

                for line in ori_vcf:
                    if line[0] == '#':
                        if '##ALT=' in line:
                            header_alt+=line
                    else:
                        break
                new_vcf.write(header_alt)
                if SR_Tag is not None:
                    new_vcf.write('##INFO=<ID=SUPPORT,Number=1,Type=Integer,Description="Number of reads supporting this variant">\n')
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

                        if SR_Tag is not None:
                            new_line = fields[0]+'\t'+fields[1]+'\t'+fields[2]+'\tN\t<'+svtype+'>\t'+fields[5]+'\t'+fields[6]+'\t'+'SVTYPE='+svtype+';END='+end+';SVLEN='+svlen+';SUPPORT='+support+';SC='+sv_caller+'\tGT\t'+genotype+'\n'
                        else:
                            new_line = fields[0]+'\t'+fields[1]+'\t'+fields[2]+'\tN\t<'+svtype+'>\t'+fields[5]+'\t'+fields[6]+'\t'+'SVTYPE='+svtype+';END='+end+';SVLEN='+svlen+';SC='+sv_caller+'\tGT\t'+genotype+'\n'
                        new_vcf.write(new_line)

    if output_reg_vcfs:
        reg_vcfs = OrderedDict()
        for sv_caller in caller_vcf_dict.keys():
            reg_vcfs[sv_caller] = out_dir+'/'+sv_caller+'_regularized_format.vcf'

        return reg_vcfs


def gz_sort_and_tabix(input_vcf):

    os.popen('vcf-sort '+input_vcf+' > '+input_vcf.rstrip('.vcf')+'_sorted.vcf').read()
    os.popen('bgzip -c '+input_vcf.rstrip('.vcf')+'_sorted.vcf > '+input_vcf.rstrip('.vcf')+'_sorted.vcf.gz').read()
    os.popen('tabix -p vcf '+input_vcf.rstrip('.vcf')+'_sorted.vcf.gz').read()
    os.popen('rm '+input_vcf.rstrip('.vcf')+'_sorted.vcf').read()

    output_vcfgz = input_vcf.rstrip('.vcf')+'_sorted.vcf.gz'

    return output_vcfgz

def truvari_eval(benchmark_vcf,comp_vcf,comp_sv_caller,out_dir,truvari_parameters,out_vcf_name='Multi_SV_Caller_Merged'):

    #if not os.path.isdir(out_dir+'/truvari_tmp'):
    #    os.mkdir(out_dir+'/truvari_tmp')

    bmk_vcfgz = gz_sort_and_tabix(benchmark_vcf)
    cmp_vcfgz = gz_sort_and_tabix(comp_vcf)

    os.popen('truvari bench -b '+bmk_vcfgz+' -c '+cmp_vcfgz+' -o '+out_dir+'/truvari_tmp '+truvari_parameters.rstrip('\n')).read()

    bmk_only = out_dir+'/truvari_tmp/fn.vcf'
    cmp_only = out_dir+'/truvari_tmp/fp.vcf'
    overlap  = out_dir+'/truvari_tmp/tp-base.vcf'

    with open(bmk_only,'r') as bmk_file:
        with open(cmp_only,'r') as cmp_file:
            with open(overlap,'r') as ovlp_file:
                with open(out_dir+'/'+out_vcf_name+'.vcf','w') as merged_file:
                    for ovlp_line in ovlp_file:
                        if ovlp_line[0] == '#':
                            merged_file.write(ovlp_line.replace('##source=', '##source='+comp_sv_caller+'/'))
                        else:
                            merged_file.write(ovlp_line.replace('SC=', 'SC='+comp_sv_caller+','))

                    for cmp_line in cmp_file:
                        if cmp_line[0] !='#':
                            merged_file.write(cmp_line)

                    for bmk_line in bmk_file:
                        if bmk_line[0] !='#':
                            merged_file.write(bmk_line)

    #clean up
    os.popen('rm -r '+out_dir+'/truvari_tmp').read()
    os.popen('rm '+bmk_vcfgz+' '+bmk_vcfgz+'.tbi').read()
    os.popen('rm '+cmp_vcfgz+' '+cmp_vcfgz+'.tbi').read()
    
    new_benchmark_vcf = out_dir+'/Multi_SV_Caller_Merged.vcf'

    return new_benchmark_vcf

def truvari_overlap(reg_vcfs,out_dir,tcf): #reg_vcfs is OrderedDict()

    with open(tcf,'r') as tcf_file:
        for line in tcf_file:
            if line[0]!='#':
                truvari_parameters = line.rstrip('\n')
                break

    merged_vcf=''

    for sv_caller,vcf_file in reg_vcfs.items():
        if merged_vcf=='':
            merged_vcf=vcf_file
        else:
            merged_vcf=truvari_eval(merged_vcf,vcf_file,sv_caller,out_dir,truvari_parameters)

    return merged_vcf


def plot_overlap_by_callers(vcf_file,save_dir,sv_types=['ALL','DEL','INS']):

    #overlap_dict = OrderedDict()

    overlap_dict = dict()
    for sv_type in sv_types:
        overlap_dict[sv_type] = OrderedDict()
    
    with open(vcf_file,'r') as vcf:
        for line in vcf:
            if '##source=' in line:
                all_sv_callers = line.rstrip('\n').lstrip('##source=').split('/')
                all_sv_callers.reverse()
                total_sv_caller_num = len(all_sv_callers)
                break
        
        #for i in range(total_sv_caller_num,0,-1):
        #    overlap_dict[i] = [0]*total_sv_caller_num
        for sv_type in sv_types:
            for i in range(total_sv_caller_num,0,-1):
                overlap_dict[sv_type][i] = [0]*total_sv_caller_num

        for line in vcf:
            if line[0] != '#':
                sv_callers=re.findall("SC=([^;\t]+)",line)[0].split(',')
                sv_caller_num = len(sv_callers)
                sv_type = re.findall("SVTYPE=(\w+)",line)[0]

                if 'ALL' in overlap_dict.keys():
                    for sv_caller in sv_callers:
                        overlap_dict['ALL'][sv_caller_num][all_sv_callers.index(sv_caller)] += 1

                if sv_type in overlap_dict.keys():
                    for sv_caller in sv_callers:
                        overlap_dict[sv_type][sv_caller_num][all_sv_callers.index(sv_caller)] += 1

    for sv_type in overlap_dict.keys():
        overlap_df = pd.DataFrame(overlap_dict[sv_type], index=all_sv_callers,)
        fig, ax = plt.subplots(figsize=(8,4))
        overlap_df.plot.bar(stacked=True,ax=ax,colormap='Blues_r', edgecolor='gray', linewidth=0.2)
        #overlap_df.plot.bar(stacked=True,ax=ax, edgecolor='gray', linewidth=0.2)
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
        plt.savefig(save_dir+'/'+sv_type+'_SV_overlap_by_callers.pdf',bbox_inches='tight')
        plt.close(fig)




    


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--vcf_list_file','-vlf',)
    parser.add_argument('--truvari_config_file','-tcf',)
    parser.add_argument('--out_dir','-o_dir')

    args = parser.parse_args()

    vlf = args.vcf_list_file
    tcf = args.truvari_config_file
    out_dir = args.out_dir

    reg_vcfs = vcf_regularization(vlf,out_dir)
    merged_vcf = truvari_overlap(reg_vcfs,out_dir,tcf)
    plot_overlap_by_callers(merged_vcf,out_dir,sv_types=['ALL','DEL','INS'])
