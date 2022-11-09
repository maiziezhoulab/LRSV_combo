#from pathlib import Path
#Path('/root/dir/sub/file.ext').stem -> file

def break1(content):
    return content == 1

def normal_region(content):
    return content == 2

def no_cover(content):
    return content == 0

def complex_cover(content):
    return content > 2

def different_depth(content):
    return content

def decision_func(chrom,content,old_region,criteria):

    if criteria(content):
        skip_base = False
        if old_region is None or chrom == old_region[0]:
            write_old = False
        else:
            write_old = True
    else:
        skip_base = True
        if old_region is None:
            write_old = False
        else:
            write_old = True
    return skip_base, write_old


def update_bed_region(chrom,loc,content,out_file,criteria,old_region=None):

    skip_base, write_old = decision_func(chrom,content,old_region,criteria)

    if skip_base:
        new_region = None
    elif old_region is None or write_old:
        new_region = [chrom,loc-1,loc] #NOTE:standard bed file use 0-based for start and 1-based for end, here we assume loc is 1-based
    else: #chrom==old_region[0]
        new_region = [chrom, old_region[1], loc]

    if write_old:
        out_file.write(old_region[0]+"\t"+str(old_region[1])+"\t"+str(old_region[2])+"\n")

    return new_region


def depth_to_bed_compare(depth_file1,depth_file2,out_dir):

    #NOTE: here we assume that the coordinate in the depth file is one based

    prefix1 = depth_file1.split("/")[-1].rsplit(".",1)[0]
    prefix2 = depth_file2.split("/")[-1].rsplit(".",1)[0]

    region1_nocov = None
    region1_compl = None
    region1_brk1  = None
    region1_normal= None
    region2_nocov = None
    region2_compl = None
    region2_brk1  = None
    region2_normal= None
    region_difcov = None

    with open(depth_file1,"r") as df1, open(depth_file2,"r") as df2, \
            open(out_dir+"/"+prefix1+"_nocov.bed","w") as nf1, open(out_dir+"/"+prefix1+"_complexcov.bed","w") as cf1, \
            open(out_dir+"/"+prefix1+"_break1.bed","w") as bk11, open(out_dir+"/"+prefix1+"_normal.bed","w") as nm1, \
            open(out_dir+"/"+prefix2+"_nocov.bed","w") as nf2, open(out_dir+"/"+prefix2+"_complexcov.bed","w") as cf2, \
            open(out_dir+"/"+prefix2+"_break1.bed","w") as bk12, open(out_dir+"/"+prefix2+"_normal.bed","w") as nm2, \
            open(out_dir+"/"+prefix1+"_"+prefix2+"_diffcov.bed","w") as dif:
        for d1line, d2line in zip(df1, df2):
            chr_d1, loc_d1, depth_d1 = d1line.rstrip("\n").split("\t")
            chr_d2, loc_d2, depth_d2 = d2line.rstrip("\n").split("\t")

            #check if the two depth file align to each other:
            if chr_d1 != chr_d2 or loc_d1 != loc_d2:
                raise ValueError("depth_file1 and depth_file2 does not have the same base sequence, please use -aa in samtools depth")

            chrom = chr_d1
            loc = int(loc_d1)
            depth_d1 = int(depth_d1)
            depth_d2 = int(depth_d2)
            diff_depth = depth_d1 != depth_d2

            region1_nocov = update_bed_region(chrom,loc,depth_d1,nf1,no_cover,region1_nocov)
            region1_compl = update_bed_region(chrom,loc,depth_d1,cf1,complex_cover,region1_compl)
            region1_brk1  = update_bed_region(chrom,loc,depth_d1,bk11,break1,region1_brk1)
            region1_normal= update_bed_region(chrom,loc,depth_d1,nm1,normal_region,region1_normal)

            region2_nocov = update_bed_region(chrom,loc,depth_d2,nf2,no_cover,region2_nocov)
            region2_compl = update_bed_region(chrom,loc,depth_d2,cf2,complex_cover,region2_compl)
            region2_brk1  = update_bed_region(chrom,loc,depth_d2,bk12,break1,region2_brk1)
            region2_normal= update_bed_region(chrom,loc,depth_d2,nm2,normal_region,region2_normal)
            
            region_difcov = update_bed_region(chrom,loc,diff_depth,dif,different_depth,region_difcov)

        for r, f in [(region1_nocov,nf1),(region1_compl,cf1), (region1_brk1,bk11), (region1_normal,nm1), \
                (region2_nocov,nf2),(region2_compl,cf2),(region2_brk1,bk12),(region2_normal,nm2),(region_difcov,dif)]:
            if r is not None:
                f.write(r[0]+"\t"+str(r[1])+"\t"+str(r[2]))


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--depth_file1', type=str,)
    parser.add_argument('--depth_file2', type=str,)
    parser.add_argument('--output_dir','-o', type=str,)
    args = parser.parse_args()

    depth_to_bed_compare(args.depth_file1,args.depth_file2,args.output_dir)

