prefix=the_name_of_your_vcf(but without .vcf)

ref=your_reference
bed=your_high_confidence_bed
bench=your_bench_vcf
bench_del=your_bench_vcf_del_only
bench_ins=your_bench_vcf_ins_only

p=0.5
P=0.5
r=500

rm -r Truvari_${prefix} 

mkdir Truvari_${prefix}

python /data/maiziezhou_lab/Yichen/Projects/MARS_long_reads/Other_SV_Caller_results/vcf_filter.py -v ./${prefix}.vcf -o_dir .
#If you are running this script on dipcall vcf (or vcfs that do not have SVTYPE in INFO field) use this line:
#python /data/maiziezhou_lab/Yichen/Projects/MARS_long_reads/Other_SV_Caller_results/vcf_filter.py --dipcall -v ./${prefix}.vcf -o_dir .
#If you are running this script on pav vcf (or vcfs that have too much small SVs) use this line:
#python /data/maiziezhou_lab/Yichen/Projects/MARS_long_reads/Other_SV_Caller_results/vcf_filter.py --remove_small_sv -v ./${prefix}.vcf -o_dir .

vcf-sort ${prefix}_DEL_INS_noXY.vcf > ${prefix}_DEL_INS_noXY_sorted.vcf
bgzip -c ${prefix}_DEL_INS_noXY_sorted.vcf > ${prefix}_DEL_INS_noXY_sorted.vcf.gz
tabix -p vcf ${prefix}_DEL_INS_noXY_sorted.vcf.gz

vcf-sort ${prefix}_DEL_noXY.vcf > ${prefix}_DEL_noXY_sorted.vcf
bgzip -c ${prefix}_DEL_noXY_sorted.vcf > ${prefix}_DEL_noXY_sorted.vcf.gz
tabix -p vcf ${prefix}_DEL_noXY_sorted.vcf.gz

vcf-sort ${prefix}_INS_noXY.vcf > ${prefix}_INS_noXY_sorted.vcf
bgzip -c ${prefix}_INS_noXY_sorted.vcf > ${prefix}_INS_noXY_sorted.vcf.gz
tabix -p vcf ${prefix}_INS_noXY_sorted.vcf.gz


#####################################################################################################################
#####################################################################################################################
#sizemin 50

truvari bench -b ${bench} -c ${prefix}_DEL_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_DEL_50_ --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 50

truvari bench -b ${bench_del} -c ${prefix}_DEL_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/DEL_50_ --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 50

truvari bench -b ${bench_ins} -c ${prefix}_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_50_  --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 50

####################################################################################################################
#sizemin 50 sizemax1000

truvari bench -b ${bench} -c ${prefix}_DEL_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_DEL_50_1k --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 50 --sizemax 1000

truvari bench -b ${bench_del} -c ${prefix}_DEL_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/DEL_50_1k --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 50 --sizemax 1000

truvari bench -b ${bench_ins} -c ${prefix}_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_50_1k  --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 50 --sizemax 1000


###################################################################################################################
#sizemin 1000 sizemax 10000

truvari bench -b ${bench} -c ${prefix}_DEL_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_DEL_1k_10k --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 1000 --sizemax 10000

truvari bench -b ${bench_del} -c ${prefix}_DEL_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/DEL_1k_10k --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 1000 --sizemax 10000

truvari bench -b ${bench_ins} -c ${prefix}_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_1k_10k  --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 1000 --sizemax 10000

###################################################################################################################
#sizemin 10000

truvari bench -b ${bench} -c ${prefix}_DEL_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_DEL_10k_ --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 10000

truvari bench -b ${bench_del} -c ${prefix}_DEL_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/DEL_10k_ --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 10000

truvari bench -b ${bench_ins} -c ${prefix}_INS_noXY_sorted.vcf.gz -f ${ref} -o Truvari_${prefix}/INS_10k_  --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin 10000

##################################################################################################################
##################################################################################################################

python Truvari_results_parser.py --truvari_results_dir Truvari_${prefix}/
