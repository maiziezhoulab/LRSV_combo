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
	- [MAMnet](#MAMnet)
	- [DeBreak](#DeBreak)
- [Assembly Based SV Callers](#Assembly-Based-SV-Callers)
	- [Dipcall](#Dipcall)
	- [SVIM-asm](#SVIM-asm) 
	- [PAV](#PAV)

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
```
bam=your_bamfile.bam
ref=your_reference_file.fa
outvcf=output_vcf_name.vcf
work_dir=your_working_dir

cuteSV -t 12 \
        --max_cluster_bias_INS 1000 \
        --diff_ratio_merging_INS 0.9 \
        --max_cluster_bias_DEL 1000 \
        --diff_ratio_merging_DEL 0.5 \
        --genotype \
        ${bam} \
        ${ref} \
        ${outvcf} \
        ${work_dir}
```
### Other notes
```
> For PacBio CLR data:
	--max_cluster_bias_INS		100
	--diff_ratio_merging_INS	0.3
	--max_cluster_bias_DEL	200
	--diff_ratio_merging_DEL	0.5

> For PacBio CCS(HIFI) data:
	--max_cluster_bias_INS		1000
	--diff_ratio_merging_INS	0.9
	--max_cluster_bias_DEL	1000
	--diff_ratio_merging_DEL	0.5

> For ONT data:
	--max_cluster_bias_INS		100
	--diff_ratio_merging_INS	0.3
	--max_cluster_bias_DEL	100
	--diff_ratio_merging_DEL	0.3
```
## NanoVar
### Project Links
#### Github Repo:
https://github.com/benoukraflab/NanoVar
#### Publication:
https://doi.org/10.1186/s13059-020-01968-7
### Installation & Dependencies
#### Installation
```
# Installing from bioconda automatically installs all dependencies 
conda install -c bioconda nanovar
# or
# Installing from PyPI requires own installation of dependencies
pip install nanovar
# or
# Installing from GitHub requires own installation of dependencies
git clone https://github.com/cytham/nanovar.git 
cd nanovar 
pip install .
```
#### Dependencies
```
bedtools >=2.26.0
samtools >=1.3.0
minimap2 >=2.17
makeblastdb and windowmasker
hs-blastn ==0.0.5
```
### Inputs & Outputs
### Commands used
```
datatype=your_datatype
bam=your_bamfile.bam
ref=your_reference_file.fa
work_dir=your_working_dir

nanovar -t 12 -x ${datatype} ${bam} ${ref} ${work_dir}
```
### Other notes
```
-x str, --data_type str
                        type of long-read data [ont]
                        ont - Oxford Nanopore Technologies
                        pacbio-clr - Pacific Biosciences CLR
                        pacbio-ccs - Pacific Biosciences CCS
```
## pbsv
### Project Links
#### Github Repo:
https://github.com/pacificbiosciences/pbsv/
### Installation
#### Installation
```
conda install -c bioconda pbsv
```
### Inputs & Outputs
### Commands used
```
prefix=your_vcf_name
bam=your_bamfile.bam
ref=your_reference_file.fa

pbsv discover -s NA24385 ${bam} ${prefix}.svsig.gz
pbsv call --ccs ${ref} ${prefix}.svsig.gz ${prefix}.vcf
```
### Other notes
```
--ccs is only for Pacbio CCS/HiFi reads
```
## SVIM
### Project Links
#### Github Repo:
https://github.com/eldariont/svim
#### Publication:
https://doi.org/10.1093/bioinformatics/btz041
### Installation & Dependencies
#### Installation
```
#Install via conda into a new environment (recommended): installs all dependencies including read alignment dependencies
conda create -n svim_env --channel bioconda svim

#Install via conda into existing (active) environment: installs all dependencies including read alignment dependencies
conda install --channel bioconda svim

#Install via pip (requires Python 3.6.* or newer): installs all dependencies except those necessary for read alignment (ngmlr, minimap2, samtools)
pip install svim

#Install from github (requires Python 3.6.* or newer): installs all dependencies except those necessary for read alignment (ngmlr, minimap2, samtools)
git clone https://github.com/eldariont/svim.git
cd svim
pip install .
```
#### Dependencies

-   _edlib_ for edit distance computation
-   _matplotlib>=3.3.0_ for plotting
-   _numpy_ and _scipy_ for hierarchical clustering
-   _pysam_ (>=0.15.2) for SAM/BAM file processing
-   _pyspoa_ (>=0.0.6) for consensus sequence computation
-   _py-cpuinfo_ (>=7.0.0) for CPU info retrieval (checking for SIMD capabilities)

### Inputs & Outputs
### Commands used
```
workdir=your_working_dir
bam=your_bamfile.bam
ref=your_reference_file.fa
prefix=your_output_vcf_name

svim alignment --sequence_alleles --min_sv_size 30 ${workdir} \
        ${bam} \
        ${ref}

cat ${workdir}/variants.vcf | grep -v 'SUPPORT=1;\|SUPPORT=2;\|SUPPORT=3;\|SUPPORT=4;\|SUPPORT=5;\|SUPPORT=6;\|SUPPORT=7;\|SUPPORT=8;\|SUPPORT=9;' > ${prefix}.vcf
```
### Other notes
In our evaluation, we used SVIM v1.4.2, which uses symbolic alleles (such as \<DEL\> or \<INV\>) in vcf by default. To output allele sequences, you need to add `--sequence_alleles`

In newer versions such as v2.0.0, all SV alleles are represented by nucleotide sequences by default.

Supporting read number filtering threshold (minimal number of supporting reads) depends on the coverage of your sequencing data, [DeBreak](https://github.com/Maggi-Chen/DeBreak#1---min_support-minimal-number-of-supporting-reads) has provided a list of suggested thresholds.

## Sniffles
### Project Links
#### Github Repo:
https://github.com/fritzsedlazeck/Sniffles
#### Publication:
https://doi.org/10.1038/s41592-018-0001-7
### Installation & Dependencies
#### Installation
```
conda install sniffles=1.0
```
#### Dependencies
```
Python >= 3.7
pysam
```
### Inputs & Outputs
### Commands used
```
bam=your_bam_file.bam
prefix=your_vcf_name

sniffles -t 12 --ccs_reads --cluster --genotype -m ${bam} -v ${prefix}.vcf
```
Note:`--ccs_reads` is only for Pacbio CCS/HiFi sequencing data
### Other notes
Sniffles/Sniffles2 have been tested on `python==3.9.5 pysam==0.16.0.1` according to the official repository. However, if you meet some problems with pysam (eg. segment fault), consider downgrading pysam to 0.15.2 or upgrade it to 0.17 or higher.

Sniffles also requires `MD` tag information in your alignment file. NGMLR includes `MD` tag by default, for minimap2 and Winnowmap, you need to add `--MD` flag, and for LRA you need to add `--printMD` flag when aligning reads to reference.
## Sniffles2
### Project Links
#### Github Repo:
https://github.com/fritzsedlazeck/Sniffles
#### Publication:
https://doi.org/10.1101/2022.04.04.487055
### Installation & Dependencies
#### Installation
```
conda install sniffles=2.0
```
#### Dependencies
```
Python >= 3.7
pysam
```
### Inputs & Outputs
### Commands used
```
bam=your_bamfile.bam
ref=your_reference_file.fa
prefix=your_output_vcf_name

sniffles --input ${bam} --reference ${ref} --vcf ${prefix}.vcf --threads 20
```
### Other notes
See Sniffles.
## Smartie-sv
### Project Links
#### Github Repo:
https://github.com/zeeev/smartie-sv
#### Publication:
https://www.science.org/doi/10.1126/science.aar6343
### Installation & Dependencies
#### Installation
```
git clone --recursive https://github.com/zeeev/smartie-sv.git
cd smartie-sv && make
```
#### Dependencies
```
Anaconda
Snakemake
Bedtools
```
### Inputs & Outputs
### Commands used
### Other notes

## NanoSV
### Project Links
#### Github Repo:
https://github.com/mroosmalen/nanosv
#### Publication:
https://doi.org/10.1038/s41467-017-01343-4
### Installation
```
conda install -c bioconda nanosv
# or
pip install nanosv
```
### Inputs & Outputs
### Commands used
### Other notes

## PBHoney
### Project Links
#### Github Repo:
#### Publication:
### Installation & Dependencies
#### Installation
#### Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## MAMnet
### Project Links
#### Github Repo:
https://github.com/micahvista/MAMnet
#### Publication:
https://doi.org/10.1093/bib/bbac195
### Installation & Dependencies
#### Installation
```
#Install from github (requires Python 3.6.* or newer): installs all dependencies except those necessary for read alignment (ngmlr, minimap2, samtools)
git clone https://github.com/micahvista/MAMnet.git
cd MAMnet
```
#### Dependencies
### Inputs & Outputs
### Commands used
### Other notes

## DeBreak
### Project Links
#### Github Repo:
https://github.com/Maggi-Chen/DeBreak
#### Publication:
https://doi.org/10.21203/rs.3.rs-1261915/v1
### Installation & Dependencies
#### Installation
```
conda install -c bioconda debreak
```
#### Dependencies
-   python3
-   pysam (tested with version 0.19.0)
-   minimap2 (tested with version 2.15)
-   wtdbg2 (tested with version 2.5)
### Inputs & Outputs
### Commands used
### Other notes

# Assembly Based SV Callers
## Dipcall
### Project Links
#### Github Repo:
https://github.com/lh3/dipcall
#### Publication:
https://doi.org/10.1038/s41592-018-0054-7
### Installation
```
wget https://github.com/lh3/dipcall/releases/download/v0.3/dipcall-0.3_x64-linux.tar.bz2
tar -jxf dipcall-0.3_x64-linux.tar.bz2
```
### Inputs & Outputs
### Commands used
### Other notes
## SVIM-asm
### Project Links
#### Github Repo:
https://github.com/eldariont/svim-asm
#### Publication:
https://doi.org/10.1093/bioinformatics/btaa1034
### Installation
```
# Install using Anaconda
conda install --channel bioconda svim-asm

# Or install from github (requires Python 3)
git clone https://github.com/eldariont/svim-asm.git
cd svim-asm
pip install .
```
### Inputs & Outputs
### Commands used
### Other notes
## PAV
### Project Links
#### Github Repo:
https://github.com/EichlerLab/pav
#### Publication:
https://doi.org/10.1126/science.abf7117
### Installation & Dependencies
#### Installation
```
git clone --recursive https://github.com/EichlerLab/pav.git
```
#### Dependencies
PAV requires Python 3 with the following Python libraries installed:
1.  BioPython
2.  intervaltree
3.  matplotlib
4.  numpy
5.  pandas
6.  pysam
7.  scipy

Command line tools needed:
1.  minimap2 (default aligner)
2.  lra (optional alternate aligner)
3.  samtools
4.  bedToBigBed (optional, from UCSC browser tools)
### Inputs & Outputs
### Commands used
### Other notes
PAV may crash with pysam 0.16, if you meet such problem, please downgrade pysam to 0.15.2.
