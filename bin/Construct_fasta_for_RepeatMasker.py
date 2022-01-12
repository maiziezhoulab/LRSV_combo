import re

'''chr1	121480372	D20	N	<DEL>	.	PASS	IMPRECISE;SVMETHOD=picky;END=121484101;SVTYPE=DEL;RE=2;RNAMES=m64015_190922_010918/19858208/ccs,m64012_190920_173625/57412007/ccs;SVLEN=3730;CIPOS=0,0;CIEND=-1,1;NOTE=CIPOS_CIEND;ISVTYPE=DEL(2)	GT	./.'''
def construct_fasta_RepeatMasker(vcf,sample,sv_caller,out_dir):

    with open(vcf,'r') as vcf_file:
        with open(out_dir+'/'+sv_caller+'_'+sample+'_del.fasta','w') as del_fa:
            with open(out_dir+'/'+sv_caller+'_'+sample+'_ins.fasta','w') as ins_fa:
                for line in vcf_file:
                    if line[0]!='#':
                        line = line.rstrip('\n').split('\t')
                        chrnum = line[0]
                        start = line[1]
                        ref = line[3]
                        alt = line[4]
                        info = line[7]
                        svtype = re.findall("SVTYPE=(\w+)",info)[0]
                        if svtype not in ['INS','DEL']:
                            continue
                        svlen  = re.findall("SVLEN=-?(\d+)",info)[0]

                        if svtype=='DEL' and ref != 'N':
                            del_fa.write('>'+sv_caller+'_'+sample+'_'+chrnum+'_s'+start+'_l'+svlen+'\n')
                            del_fa.write(ref+'\n')
                        elif svtype=='INS' and alt != '<INS>':
                            ins_fa.write('>'+sv_caller+'_'+sample+'_'+chrnum+'_s'+start+'_l'+svlen+'\n')
                            ins_fa.write(alt+'\n')


construct_fasta_RepeatMasker('pbsv_NA24385_NGMLR.vcf','NA24385_CCS_NGMLR','pbsv','.')
construct_fasta_RepeatMasker('Sniffles_NA24385_NGMLR.vcf','NA24385_CCS_NGMLR','Sniffles','.')
construct_fasta_RepeatMasker('SKSV_NA24385_Pacbio_CCS.vcf','NA24385_CCS','SKSV','.')
