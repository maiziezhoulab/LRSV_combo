# LRSV_combo

# Table of contents
- [Datasets](#Datasets)
  - [Pacbio](#Pacbio)
  - [Oxford Nanopore Technologies](#Oxford-Nanopore-Technologies)
- [Alignment Based SV Callers](#Alignment-Based-SV-Callers)
  - [SKSV](#SKSV)
  - [cuteSV](#cuteSV)
  - [NanoVar](#NanoVar)
  - [pbsv](#pbsv)
  - [SVIM](#SVIM)
  - [Sniffles](#Sniffles)
  - [Smartie-sv](#Smartie-sv)
  - [NanoSV](#NanoSV)
  - [PBHoney](#PBHoney)
- [Assembly Based SV Callers](#Assembly-Based-SV-Callers)
- [Other SV Callers](#Other-SV-Callers)

# Datasets
## Pacbio

## Oxford Nanopore Technologies

# Alignment Based SV Callers
## SKSV
### Project Links
#### Github Repo:
https://github.com/ydLiu-HIT/SKSV
#### Publication:
https://doi.org/10.1093/bioinformatics/btab341
### Installation & Dependencies
#### Installation
```
git clone https://github.com/ydLiu-HIT/SKSV.git
cd SKSV/skeleton/
make
cd ..
```
### Inputs & Outputs
### Commands used
```
ref=your_reference_file.fasta
fastq=your_read_file.fastq
out_prefix=the_desired_prefix_of_the_output(name of output files)
out_dir=.

SKSV=/path/to/SKSV/SKSV

time ${SKSV} index ${ref} ${out_dir}
time ${SKSV} aln ${out_dir} ${fastq} --output sk.svseg 
time ${SKSV} call --genotype --print_allele_seq --read ${fastq} sk.svseg ${ref} ${out_prefix}.vcf ${out_dir}
```
### Other notes
If you see the error
```
‘for’ loop initial declarations are only allowed in C99 mode
```
Try again with a newer version of gcc. Here we use GCC/10.2.0

## cuteSV
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## NanoVar
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## pbsv
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## SVIM
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## Sniffles
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## Smartie-sv
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## NanoSV
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## PBHoney
### Project Links
### Installation & Dependencies
### Inputs & Outputs
### Commands used
### Other notes

# Assembly Based SV Callers

# Other SV Callers
