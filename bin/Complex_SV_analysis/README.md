# Complex SV analysis 

**Special Note:** The benchmark VCFs and high confidence BED file are provided [here](https://github.com/maiziezhoulab/LRSV_combo/tree/main/benchmarks) 
# Table of Contents
- [Evaluate real data](#real_data)
- [Evaluate simulated data](#sim_data)
    - [Evaluate DUP](#dup)
    - [Evaluate INV](#inv)
    - [Evaluate TRA](#tra)



# Evaluate real data
## Inputs & Outputs
### Inputs
somatic VCF, Bench excel (provided in data folder)
### Outputs
precision.txt recall.txt

## Commands used
```
python3 eval_real_data.py -i path/to/vcffile -b path/to/benchfile
```



# Evaluate simulated data
## Inputs
call VCF, bench bed file(used for simulation)

## Outputs
summary.txt

## Commands used
```
# evaluate DUP
python3 eval_dup.py -callvcf path/to/dupvcf -bench path/to/dupbench -o eval_dup

# evaluate INV
python3 eval_inv.py -callvcf path/to/invvcf -bench path/to/invbench -o eval_inv

# evaluate TRA
## For tra, you need to convert the bench bedfile to a pseudo-vcf file using the below command
python3 convert_tra_bed_to_vcf.py -bed path/to/trabench_bed -o path/to/trabench_vcf

python3 eval_tra.py -callvcf path/to/travcf -bench path/to/trabench_vcf -o eval_tra



```





