# SV Evaluators
**Special Note:** The benchmark VCFs and high confidence BED file are provided [here](https://github.com/maiziezhoulab/LRSV_combo/tree/main/benchmarks) 
# Table of Contents
- [Truvari](#Truvari)
- [hap-eval](#hap-eval)
- [SURVIVOR](#SURVIVOR)


# Truvari
## Project Links
### Github Repo:
https://github.com/ACEnglish/truvari
### Publication:
Truvari: refined structural variant comparison preserves allelic diversity

https://doi.org/10.1186/s13059-022-02840-6
#### BibTeX
```
@article{english2022truvari,
  title={Truvari: refined structural variant comparison preserves allelic diversity},
  author={English, Adam C and Menon, Vipin K and Gibbs, Richard A and Metcalf, Ginger A and Sedlazeck, Fritz J},
  journal={Genome Biology},
  volume={23},
  number={1},
  pages={1--20},
  year={2022},
  publisher={Springer}
}
```
## Installation & Dependencies
### Installation Methods
See [here](https://github.com/acenglish/truvari/wiki/Installation)
### Dependencies
```
Not explicilty mentioned. Handled by Conda/Mamba/pip
```
## Commands used
```
prefix=${the file name of your VCF (.vcf suffix removed)}
ref=${reference_genome}
bed=HG002_SVs_Tier1_v0.6_chr_noXY.bed

bench=HG002_SVs_Tier1_v0.6_chr_noXY.vcf.gz
bench_del=HG002_SVs_Tier1_v0.6_chr_del_noXY.vcf.gz
bench_ins=HG002_SVs_Tier1_v0.6_chr_ins_noXY.vcf.gz

out_dir=Truvari_${prefix}_p0

p=0
P=0.5
r=500
# This example is comparing the SVs within 50~1kbp size range 
minsize=50
maxsize=1000

rm -r ${out_dir}

mkdir ${out_dir}


python vcf_filter.py -v ./${prefix}.vcf -o_dir . #if running on Dipcall result, please add --dipcall flag

vcf-sort ${prefix}_DEL_INS_noXY.vcf > ${prefix}_DEL_INS_noXY_sorted.vcf
bgzip -c ${prefix}_DEL_INS_noXY_sorted.vcf > ${prefix}_DEL_INS_noXY_sorted.vcf.gz
tabix -p vcf ${prefix}_DEL_INS_noXY_sorted.vcf.gz

vcf-sort ${prefix}_DEL_noXY.vcf > ${prefix}_DEL_noXY_sorted.vcf
bgzip -c ${prefix}_DEL_noXY_sorted.vcf > ${prefix}_DEL_noXY_sorted.vcf.gz
tabix -p vcf ${prefix}_DEL_noXY_sorted.vcf.gz

vcf-sort ${prefix}_INS_noXY.vcf > ${prefix}_INS_noXY_sorted.vcf
bgzip -c ${prefix}_INS_noXY_sorted.vcf > ${prefix}_INS_noXY_sorted.vcf.gz
tabix -p vcf ${prefix}_INS_noXY_sorted.vcf.gz

truvari bench -b ${bench} -c ${prefix}_DEL_INS_noXY_sorted.vcf.gz -f ${ref} -o ${out_dir}/INS_DEL_50_1k --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin ${minsize} --sizemax ${maxsize}

truvari bench -b ${bench_del} -c ${prefix}_DEL_noXY_sorted.vcf.gz -f ${ref} -o ${out_dir}/DEL_50_1k --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin ${minsize} --sizemax ${maxsize}

truvari bench -b ${bench_ins} -c ${prefix}_INS_noXY_sorted.vcf.gz -f ${ref} -o ${out_dir}/INS_50_1k  --includebed ${bed} -p ${p} -P ${P} -r ${r} --passonly --sizemin ${minsize} --sizemax ${maxsize}

```
## Other notes
1.For more detailed usage, please refer to their [wiki page](https://github.com/ACEnglish/truvari/wiki)

# hap-eval
## Project Links
### Github Repo:
https://github.com/Sentieon/hap-eval

### Publication:
Currently None

#### BibTeX
```

```
## Installation & Dependencies
### Installation Methods
```
git clone --recurse-submodules https://github.com/Sentieon/hap-eval.git
pip install ./hap-eval
```
### Dependencies
```
Handled by pip
```
## Inputs & Outputs
### Inputs

### Outputs

## Commands used
```

```
## Other notes
### Pipeline and parameter definition

# SURVIVOR
## Project Links
### Github Repo:

### Publication:

#### BibTeX
```

```
## Installation & Dependencies
### Installation Methods

### Dependencies
```

```
## Inputs & Outputs
### Inputs

### Outputs

## Commands used
```

```
## Other notes
