# Analysis Code Readme

## Truvari Evaluation
### Code
[Truvari_eval.sh](https://github.com/maiziezhoulab/LRSV_combo/blob/main/bin/Truvari_eval.sh)

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

### Usage
Performs Truvari evaluation on a given vcf

Outputs are stored in `Truvari_${prefix}`, this dir will be referred as **Truvari_dir** in latter parts

## SV Length Distribution Analysis
### Code
[SVLEN_distribution_analysis.py](https://github.com/maiziezhoulab/LRSV_combo/blob/main/bin/SVLEN_distribution_analysis.py)

[SVLEN_distribution_analysis_scatter.py](https://github.com/maiziezhoulab/LRSV_combo/blob/main/bin/SVLEN_distribution_analysis_scatter.py)

### Parameters:
```
'--vcf_list_file','-vlf'
'--out_dir','-o_dir'
```
**vcf_list_file:** A file which has three columns seperated by tab, one for caller name, one for the location of corresponding vcf file, one for caller type, each line corresponds to one SV caller. Example line:  `cuteSV  path/to/cuteSV/vcf  alignment`

### Usage
Plot the SV length distribution of the given vcf(s), correspond to Figure 2 in paper. (Figure 2 was plotted with `SVLEN_distribution_analysis.py`)

## Breakpoint Shift Analysis
### Code
[Breakpoint_shift.py](https://github.com/maiziezhoulab/LRSV_combo/blob/main/bin/Breakpoint_shift.py)

### Parameters:
```
'--truv_rslt_dir','-trd'
```
**truv_rslt_dir:** Truvari result dir, where you can find `tp-base.vcf` and `tp-call.vcf`. Typically it should be a dir like `${Truvari_dir}/INS_DEL_50_`

### Usage
Illustrates the breakpoint shift distribution of the SV calling results. Corresponds to Figure 3c and Figure 3g in paper main text.

## Sequence Similarity Distribution Analysis
### Code
[Sequence_similarity_distribution.py](https://github.com/maiziezhoulab/LRSV_combo/blob/main/bin/Sequence_similarity_distribution.py)

### Parameters:
```
'--truv_rslt_dir','-trd'
```
**truv_rslt_dir:** Truvari result dir, where you can find `tp-call.vcf`. Typically it should be a dir like `${Truvari_dir}/INS_DEL_50_`

### Usage
Illustrates the sequence similarity distribution of the SV calling results. Corresponds to Figure 3d and Figure 3h in paper main text.

