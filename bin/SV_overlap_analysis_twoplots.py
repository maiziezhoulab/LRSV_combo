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
# header_chrome  = '''##contig=<ID=chr1,length=249250621>
# ##contig=<ID=chr2,length=243199373>
# ##contig=<ID=chr3,length=198022430>
# ##contig=<ID=chr4,length=191154276>
# ##contig=<ID=chr5,length=180915260>
# ##contig=<ID=chr6,length=171115067>
# ##contig=<ID=chr7,length=159138663>
# ##contig=<ID=chr8,length=146364022>
# ##contig=<ID=chr9,length=141213431>
# ##contig=<ID=chr10,length=135534747>
# ##contig=<ID=chr11,length=135006516>
# ##contig=<ID=chr12,length=133851895>
# ##contig=<ID=chr13,length=115169878>
# ##contig=<ID=chr14,length=107349540>
# ##contig=<ID=chr15,length=102531392>
# ##contig=<ID=chr16,length=90354753>
# ##contig=<ID=chr17,length=81195210>
# ##contig=<ID=chr18,length=78077248>
# ##contig=<ID=chr19,length=59128983>
# ##contig=<ID=chr20,length=63025520>
# ##contig=<ID=chr21,length=48129895>
# ##contig=<ID=chr22,length=51304566>
# '''
header_chrome = '''##contig=<ID=chr1,length=249250621>
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
##contig=<ID=chrX,length=155270560>
##contig=<ID=chrY,length=59373566>
##contig=<ID=chrM,length=16571>
##contig=<ID=chr1_gl000191_random,length=106433>
##contig=<ID=chr1_gl000192_random,length=547496>
##contig=<ID=chr4_gl000193_random,length=189789>
##contig=<ID=chr4_gl000194_random,length=191469>
##contig=<ID=chr7_gl000195_random,length=182896>
##contig=<ID=chr8_gl000196_random,length=38914>
##contig=<ID=chr8_gl000197_random,length=37175>
##contig=<ID=chr9_gl000198_random,length=90085>
##contig=<ID=chr9_gl000199_random,length=169874>
##contig=<ID=chr9_gl000200_random,length=187035>
##contig=<ID=chr9_gl000201_random,length=36148>
##contig=<ID=chr11_gl000202_random,length=40103>
##contig=<ID=chr17_gl000203_random,length=37498>
##contig=<ID=chr17_gl000204_random,length=81310>
##contig=<ID=chr17_gl000205_random,length=174588>
##contig=<ID=chr17_gl000206_random,length=41001>
##contig=<ID=chr18_gl000207_random,length=4262>
##contig=<ID=chr19_gl000208_random,length=92689>
##contig=<ID=chr19_gl000209_random,length=159169>
##contig=<ID=chr21_gl000210_random,length=27682>
##contig=<ID=chrUn_gl000211,length=166566>
##contig=<ID=chrUn_gl000212,length=186858>
##contig=<ID=chrUn_gl000213,length=164239>
##contig=<ID=chrUn_gl000214,length=137718>
##contig=<ID=chrUn_gl000215,length=172545>
##contig=<ID=chrUn_gl000216,length=172294>
##contig=<ID=chrUn_gl000217,length=172149>
##contig=<ID=chrUn_gl000218,length=161147>
##contig=<ID=chrUn_gl000219,length=179198>
##contig=<ID=chrUn_gl000220,length=161802>
##contig=<ID=chrUn_gl000221,length=155397>
##contig=<ID=chrUn_gl000222,length=186861>
##contig=<ID=chrUn_gl000223,length=180455>
##contig=<ID=chrUn_gl000224,length=179693>
##contig=<ID=chrUn_gl000225,length=211173>
##contig=<ID=chrUn_gl000226,length=15008>
##contig=<ID=chrUn_gl000227,length=128374>
##contig=<ID=chrUn_gl000228,length=129120>
##contig=<ID=chrUn_gl000229,length=19913>
##contig=<ID=chrUn_gl000230,length=43691>
##contig=<ID=chrUn_gl000231,length=27386>
##contig=<ID=chrUn_gl000232,length=40652>
##contig=<ID=chrUn_gl000233,length=45941>
##contig=<ID=chrUn_gl000234,length=40531>
##contig=<ID=chrUn_gl000235,length=34474>
##contig=<ID=chrUn_gl000236,length=41934>
##contig=<ID=chrUn_gl000237,length=45867>
##contig=<ID=chrUn_gl000238,length=39939>
##contig=<ID=chrUn_gl000239,length=33824>
##contig=<ID=chrUn_gl000240,length=41933>
##contig=<ID=chrUn_gl000241,length=42152>
##contig=<ID=chrUn_gl000242,length=43523>
##contig=<ID=chrUn_gl000243,length=43341>
##contig=<ID=chrUn_gl000244,length=39929>
##contig=<ID=chrUn_gl000245,length=36651>
##contig=<ID=chrUn_gl000246,length=38154>
##contig=<ID=chrUn_gl000247,length=36422>
##contig=<ID=chrUn_gl000248,length=39786>
##contig=<ID=chrUn_gl000249,length=38502>
##contig=<ID=hs37d5,length=35477943>
'''
header_infofield='''##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=SC,Number=.,Type=String,Description="SV Caller(s) that supports this variant">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSample
'''

def vcf_regularization(vlf,out_dir,keep_refalt_seq=False,output_reg_vcfs=True):

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

    filters = dict()
    for sv_caller,vcf_info in caller_vcf_dict.items():
        with open(vcf_info[0],'r') as ori_vcf:
            for line in ori_vcf:
                if line[0] != "#":
                    ftr = line.rstrip("\n").split("\t")[6]
                    filters[ftr] = 0
    header_filters=''
    for ftr in filters.keys():
        header_filters += '##FILTER=<ID='+ftr+',Description="None">\n'


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
        #header_alt_contig=''
        with open(vcf_dir,'r') as ori_vcf:
            with open(out_dir+'/'+sv_caller+'_regularized_format.vcf','w') as new_vcf:
                new_vcf.write(header_fformat)
                new_vcf.write('##source='+sv_caller+'\n')
                new_vcf.write(header_chrome)

                for line in ori_vcf:
                    if line[0] == '#':
                        if '##ALT=' in line:
                        #if '##ALT=' in line or '##contig=' in line:
                            header_alt+=line
                            #header_alt_contig+=line
                    else:
                        break
                new_vcf.write(header_alt)
                new_vcf.write(header_filters)
                #new_vcf.write(header_alt_contig)
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
                            else:
                                continue
                            svlen = abs(len(fields[3])-len(fields[4]))
                            if svtype == 'DEL':
                                end = str(int(fields[1])+svlen)
                            else:
                                end = fields[1]
                            svlen = str(svlen)

                        if svtype not in ['DEL','INS','ins','del']:#Currently only support DEL and INS
                            continue

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

                        if keep_refalt_seq:
                            ref_seq=fields[3]
                            alt_seq=fields[4]
                        else:
                            ref_seq='N'
                            alt_seq='<'+svtype+'>'
                        
                        if SR_Tag is not None:
                            new_line = fields[0]+'\t'+fields[1]+'\t'+fields[2]+'\t'+ref_seq+'\t'+alt_seq+'\t'+fields[5]+'\t'+fields[6]+'\t'+'SVTYPE='+svtype+';END='+end+';SVLEN='+svlen+';SUPPORT='+support+';SC='+sv_caller+'\tGT\t'+genotype+'\n'
                        else:
                            new_line = fields[0]+'\t'+fields[1]+'\t'+fields[2]+'\t'+ref_seq+'\t'+alt_seq+'\t'+fields[5]+'\t'+fields[6]+'\t'+'SVTYPE='+svtype+';END='+end+';SVLEN='+svlen+';SC='+sv_caller+'\tGT\t'+genotype+'\n'
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

def filter_subset_id(merged_vcf, subset_sv, out_dir, comp):
    subset_ids = dict()
    with open(subset_sv, "r") as sf:
        for line in sf:
            if line[0]!="#":
                subset_ids[line.rstrip("\n").split("\t")[2]] = 0
    out_vcf = out_dir+"/IDfiltered_Merged_SV.vcf"
    with open(merged_vcf, "r") as mf:
        with open(out_vcf, "w") as otf:
            for line in mf:
                if line[0] == "#":
                    otf.write(line)
                else:
                    curid = line.rstrip("\n").split("\t")[2]
                    if curid in subset_ids and not comp:
                        otf.write(line)
                    elif curid not in subset_ids and comp:
                        otf.write(line)

    return out_vcf

def get_overlap_dict(vcf_file, sv_types=['ALL','DEL','INS']):
    #overlap_dict = OrderedDict()

    overlap_dict = dict()
    for sv_type in sv_types:
        overlap_dict[sv_type] = OrderedDict()
    
    with open(vcf_file,'r') as vcf:
        for line in vcf:
            if '##source=' in line:
                all_sv_callers = line.rstrip('\n')[9:].split('/')
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
    
    return overlap_dict, all_sv_callers

def plot_overlap_by_callers(vcf_file, out_dir, sv_types=['ALL','DEL','INS'], vcf_file2=None):

    overlap_dict, all_sv_callers = get_overlap_dict(vcf_file, sv_types)
    if vcf_file2 is not None:
        overlap_dict2, all_sv_callers2 = get_overlap_dict(vcf_file2, sv_types)
        if all_sv_callers != all_sv_callers2:
            raise ValueError("SV callers in vcf list file 2 should be the same as vcf list file 1 (including their order in the list)")
    else:
        overlap_dict2 = None

    for sv_type in sv_types:
        overlap_df = pd.DataFrame(overlap_dict[sv_type], index=all_sv_callers,)
        if overlap_dict2 is None:
            overlap_df.to_excel(out_dir+'/'+sv_type+'_SV_overlap_by_callers.xlsx')
            fig, ax = plt.subplots(figsize=(len(all_sv_callers)*0.5,3))
            overlap_df.plot.bar(stacked=True,ax=ax,colormap="Blues_r", edgecolor='gray', linewidth=0.2)
            ax.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
        else:
            overlap_df2 = pd.DataFrame(overlap_dict2[sv_type], index=all_sv_callers,)
            overlap_df.to_excel(out_dir+'/overlap1/'+sv_type+'_SV_overlap_by_callers.xlsx')
            overlap_df2.to_excel(out_dir+'/overlap2/'+sv_type+'_SV_overlap_by_callers.xlsx')
            fig, axes = plt.subplots(2, 1, figsize=(len(all_sv_callers)*0.5,3))
            overlap_df.plot.bar(stacked=True,ax=axes[0],colormap="Blues_r", edgecolor='gray', linewidth=0.2)
            overlap_df2.plot.bar(stacked=True,ax=axes[1],colormap="Oranges_r", edgecolor='gray', linewidth=0.2)
            if len(all_sv_callers) > 5:
                axes[0].legend(bbox_to_anchor=(-0.15, 1), loc=1, borderaxespad=0)
            else:
                axes[0].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
            axes[1].legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
            axes[1].invert_yaxis()
            axes[0].set_xticks([])
            plt.subplots_adjust(wspace=0, hspace=0)
        #overlap_df.plot.bar(stacked=True,ax=ax, edgecolor='gray', linewidth=0.2)
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        plt.savefig(out_dir+'/'+sv_type+'_SV_overlap_by_callers.pdf',bbox_inches='tight')
        plt.close(fig)


def plot_svlen_by_shared_callers(vcf_file,save_dir,sv_types=['ALL','DEL','INS']):

    svlen_dict = dict()
    for sv_type in sv_types:
        svlen_dict[sv_type] = OrderedDict()
    
    with open(vcf_file,'r') as vcf:
        for line in vcf:
            if '##source=' in line:
                all_sv_callers = line.rstrip('\n')[9:].split('/')
                #all_sv_callers.reverse()
                total_sv_caller_num = len(all_sv_callers)
                break

        for sv_type in sv_types:
            for i in range(total_sv_caller_num,0,-1):
                svlen_dict[sv_type][i] = list()

        for line in vcf:
            if line[0] != '#':
                sv_callers=re.findall("SC=([^;\t]+)",line)[0].split(',')
                sv_caller_num = len(sv_callers)
                sv_type = re.findall("SVTYPE=(\w+)",line)[0]
                svlen = float(re.findall("SVLEN=-?(\d+)",line)[0])

                if 'ALL' in svlen_dict.keys():
                    svlen_dict['ALL'][sv_caller_num].append(svlen)

                if sv_type in svlen_dict.keys():
                    svlen_dict[sv_type][sv_caller_num].append(svlen)

    for sv_type in svlen_dict.keys():
        sv_lens = list(svlen_dict[sv_type].values())
        caller_numbers = list(svlen_dict[sv_type].keys())
        # sv_lens = list()
        # caller_numbers = list()
        # for i in range(total_sv_caller_num,0,-1):
        #     sv_lens.append(svlen_dict[sv_type][i])
        #     caller_numbers.append(i)
        fig, ax = plt.subplots(figsize=(8,4))
        #ax.boxplot(sv_lens)
        ax.violinplot(sv_lens)
        ax.set_xticks([y+1 for y in range(len(caller_numbers))])
        ax.set_xticklabels(caller_numbers)
        ax.set_yscale("log")
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42
        #plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)
        plt.savefig(save_dir+'/'+sv_type+'_SV_overlap_svlen_by_shared_callers.pdf',bbox_inches='tight')
        plt.close(fig)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--vcf_list_file','-vlf',)
    parser.add_argument('--vcf_list_file2','-vlf2',)
    parser.add_argument('--truvari_config_file','-tcf',)
    parser.add_argument('--truvari_config_file2','-tcf2',)
    parser.add_argument('--out_dir','-o_dir')
    parser.add_argument('--keep_refalt_seq','-kpseq',action='store_true')
    parser.add_argument('--subset_sv','-s',help="a vcf file that contains the subset of SVs to be included in overlap analysis")
    parser.add_argument('--complement','-c',action='store_true',help="use SVs inside subset_sv or out side subset_sv. If set, use outside")

    args = parser.parse_args()

    #NOTE: Currently we only support DEL and INS overlaping

    vlf = args.vcf_list_file
    vlf2 = args.vcf_list_file2
    tcf = args.truvari_config_file
    tcf2 = args.truvari_config_file2
    
    out_dir = args.out_dir
    if vlf2 is not None and tcf2 is not None:
        if not os.path.isdir(out_dir+'/overlap1'):
            os.mkdir(out_dir+'/overlap1')
        if not os.path.isdir(out_dir+'/overlap2'):
            os.mkdir(out_dir+'/overlap2')
        out_dir2=out_dir+'/overlap2/'
        out_dir=out_dir+'/overlap1/'
    else:
        out_dir2=None
    
    subset_sv = args.subset_sv
    comp = args.complement

    keep_refalt_seq = args.keep_refalt_seq

    reg_vcfs = vcf_regularization(vlf,out_dir,keep_refalt_seq=keep_refalt_seq)
    merged_vcf = truvari_overlap(reg_vcfs,out_dir,tcf)
    if subset_sv is not None:
        merged_vcf = filter_subset_id(merged_vcf, subset_sv, out_dir,comp)

    
    if vlf2 is not None and tcf2 is not None:
        reg_vcfs2 = vcf_regularization(vlf2,out_dir2,keep_refalt_seq=keep_refalt_seq)
        merged_vcf2 = truvari_overlap(reg_vcfs2,out_dir2,tcf2)
        if subset_sv is not None:
            merged_vcf2 = filter_subset_id(merged_vcf2, subset_sv, out_dir2,comp)
    else:
        reg_vcfs2 = None
        merged_vcf2 = None


    plot_overlap_by_callers(merged_vcf,args.out_dir,sv_types=['ALL','DEL','INS'],vcf_file2=merged_vcf2)

    plot_svlen_by_shared_callers(merged_vcf,out_dir,sv_types=['ALL','DEL','INS'])
    if vlf2 is not None and tcf2 is not None:
        plot_svlen_by_shared_callers(merged_vcf2,out_dir2,sv_types=['ALL','DEL','INS'])
