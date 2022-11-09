# Analysis Code Readme

## Truvari Evaluation
### Code
[Truvari_eval.sh](https://github.com/maiziezhoulab/LRSV_combo/blob/main/bin/Truvari_eval.sh)

### Usage
Performs Truvari evaluation on a given vcf 

### Parameters:
```
prefix=the_name_of_your_vcf(but without .vcf)

ref=your_reference
bed=your_high_confidence_bed
bench=your_bench_vcf
bench_del=your_bench_vcf_del_only
bench_ins=your_bench_vcf_ins_only

p=0.5
P=0.5
r=500
```
bench and bed files can be found in the ../bench dir. Note: these benchmarks only contain chr1-22, you may also need to run `tabix -p vcf ${bench}` on the benchmark vcfs to generate .vcf.gz.tbi files 
