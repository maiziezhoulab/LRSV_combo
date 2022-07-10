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
#### Dependencies
```
python3
Biopython
numpy
samtools  # samtools was used to extract read sequence in order to generate allele sequence.
```
### Inputs & Outputs
### Commands used
```
ref=your_reference_file.fasta
fastq=your_read_file.fastq
out_prefix=the_desired_prefix_of_the_output(name of output files)
out_dir=.

SKSV=/path/to/SKSV/SKSV

# build index
time ${SKSV} index ${ref} ${out_dir} 
# skeleton-alignment
time ${SKSV} aln ${out_dir} ${fastq} --output sk.svseg 
# call variants using in.svseg file
time ${SKSV} call --genotype --print_allele_seq --read ${fastq} sk.svseg ${ref} ${out_prefix}.vcf ${out_dir} 
```
### Other notes
#### Common problems
If you see the error
```
‘for’ loop initial declarations are only allowed in C99 mode
```
try again with a newer version of gcc. Here we use GCC/10.2.0

## cuteSV
### Project Links
#### Github Repo:
https://github.com/tjiangHIT/cuteSV
#### Publication:
https://doi.org/10.1186/s13059-020-02107-y
### Installation & Dependencies
#### Installation
```
$ pip install cuteSV
or
$ conda install -c bioconda cutesv
or 
$ git clone https://github.com/tjiangHIT/cuteSV.git && cd cuteSV/ && python setup.py install 
```
#### Dependencies
```
python3
pysam
Biopython
cigar
numpy
pyvcf
```
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
#### Publication:
https://www.science.org/doi/10.1126/science.aar6343
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
