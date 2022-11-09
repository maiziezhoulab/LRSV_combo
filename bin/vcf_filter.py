import os
import re


def filter(vcf, out_dir,chrs=None,dipcall=False,remove_small_sv=False):
    if chrs is None:
        chrs = list()
        for chrnum in range(1,23):
            chrs.append('chr'+str(chrnum))

    #out_vcf = out_dir+'/'+vcf.rstrip('.vcf').split('/')[-1]+'_DEL_INS_noXY.vcf'
    out_vcf = out_dir+'/'+vcf[:-4].split('/')[-1]+'_DEL_INS_noXY.vcf'
    #out_INS_vcf = out_dir+'/'+vcf.rstrip('.vcf').split('/')[-1]+'_INS_noXY.vcf'
    out_INS_vcf = out_dir+'/'+vcf[:-4].split('/')[-1]+'_INS_noXY.vcf'
    #out_DEL_vcf = out_dir+'/'+vcf.rstrip('.vcf').split('/')[-1]+'_DEL_noXY.vcf'
    out_DEL_vcf = out_dir+'/'+vcf[:-4].split('/')[-1]+'_DEL_noXY.vcf'
    with open(vcf,'r') as fin:
        with open(out_vcf,'w') as fout:
            with open(out_INS_vcf,'w') as fins:
                with open(out_DEL_vcf,'w') as fdel:

                    for line in fin:
                        if line[0] == '#':
                            if 'contig=' in line:
                                chrinfo = line.split(",")[0].split("=")[-1]
                                if chrinfo in chrs:
                                    fout.write(line)
                                    fins.write(line)
                                    fdel.write(line)
                            else:
                                fout.write(line)
                                fins.write(line)
                                fdel.write(line)
                        else:
                            line = line.replace("SVLEN=>", "SVLEN=") #for NanoVar
                            svinfo = line.split("\t")
                            chrinfo = svinfo[0]
                            #svtype = svinfo[7].split(";")[0]

                            if remove_small_sv:
                                try:
                                    svlen = float(re.findall("SVLEN=-?(\d+)",line)[0])
                                except:
                                    svlen = abs(len(svinfo[3])-len(svinfo[4]))
                                if svlen < 50:
                                    continue

                            #if chrinfo in chrs and svtype == 'SVTYPE=DEL':
                            if dipcall:
                                if chrinfo in chrs and (len(svinfo[3])-len(svinfo[4]))>0:
                                    fout.write(line)
                                    fdel.write(line)
                                #elif chrinfo in chrs and svtype == 'SVTYPE=INS':
                                elif chrinfo in chrs and (len(svinfo[3])-len(svinfo[4]))<0:
                                    fout.write(line)
                                    fins.write(line)
                            else:
                                if chrinfo in chrs and 'SVTYPE=DEL' in svinfo[7]:
                                    fout.write(line)
                                    fdel.write(line)
                                #elif chrinfo in chrs and svtype == 'SVTYPE=INS':
                                elif chrinfo in chrs and 'SVTYPE=INS' in svinfo[7]:
                                    fout.write(line)
                                    fins.write(line)

                            

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--vcf','-v',)
    parser.add_argument('--out_dir','-o_dir')
    parser.add_argument('--chrs', nargs='+')
    parser.add_argument('--dipcall',action="store_true")
    parser.add_argument('--remove_small_sv',action="store_true")

    args = parser.parse_args()

    filter(args.vcf, args.out_dir, args.chrs, args.dipcall, args.remove_small_sv)
