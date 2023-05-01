# SV Callers

# Table of contents
- [Alignment Based SV Callers](#Alignment-Based-SV-Callers)
	- [SKSV](#SKSV)
	- [cuteSV](#cuteSV)
	- [NanoVar](#NanoVar)
	- [pbsv](#pbsv)
	- [SVIM](#SVIM)
	- [Sniffles](#Sniffles)
	- [Sniffles2](#Sniffles2)
	- [Smartie-sv](#Smartie-sv)
	- [NanoSV](#NanoSV)
	- [PBHoney](#PBHoney)
	- [MAMnet](#MAMnet)
	- [DeBreak](#DeBreak)
- [Assembly Based SV Callers](#Assembly-Based-SV-Callers)
	- [Dipcall](#Dipcall)
	- [SVIM-asm](#SVIM-asm) 
	- [PAV](#PAV)

# Alignment Based SV Callers
## SKSV
### Project Links
#### Github Repo:
https://github.com/ydLiu-HIT/SKSV
#### Publication:
https://doi.org/10.1093/bioinformatics/btab341
### Installation & Dependencies
#### Installation Methods
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
#### Input
HiFi reads
#### Output
vcf file
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
#### Installation Methods
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
#### Input
BAM file
#### Output
vcf file
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
#### Installation Methods
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
#### Input
BAM file
#### Output
vcf file
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
#### Installation Methods
```
conda install -c bioconda pbsv
```
### Inputs & Outputs
#### Input
BAM file
#### Output
vcf file
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
#### Installation Methods
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
#### Input
BAM file
#### Output
vcf file
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
#### Installation Methods
```
conda install sniffles=1.0
```
#### Dependencies
```
Python >= 3.7
pysam
```
### Inputs & Outputs
#### Input
BAM file
#### Output
vcf file
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

If you are using Truvari without `--passonly` flag to evaluate Sniffles, please add `##FILTER=<ID=STRANDBIAS,Description="Strandbias.">` in the header if its not there. 
## Sniffles2
### Project Links
#### Github Repo:
https://github.com/fritzsedlazeck/Sniffles
#### Publication:
https://doi.org/10.1101/2022.04.04.487055
### Installation & Dependencies
#### Installation Methods
```
conda install sniffles=2.0
```
#### Dependencies
```
Python >= 3.7
pysam
```
### Inputs & Outputs
#### Input
BAM file
#### Output
vcf file
### Commands used
```
bam=your_bamfile.bam
ref=your_reference_file.fa
prefix=your_output_vcf_name

sniffles --input ${bam} --reference ${ref} --vcf ${prefix}.vcf --threads 20
```
### Other notes
1. Sniffles2 automatically decides supporting reads threshold for SV calling, while Sniffles uses 10 as default threshold for number of supporting reads. However, this automatic threshold does not always give the optimal output. For `CLR_L2` library in our analysis, we set the threshold to 10 manually to get a better result, otherwise Sniffles2 will call a large amount of false positive INSs in the 1kb~10kb SV length range.

Others are same as Sniffles.
## Smartie-sv
### Project Links
#### Github Repo:
https://github.com/zeeev/smartie-sv
#### Publication:
https://www.science.org/doi/10.1126/science.aar6343
### Installation & Dependencies
#### Installation Methods
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
#### Input
BAM file or assembled contigs
#### Output
BED files
### Commands used
For BAM inputs:
```
bam=your_bam_file
ref=your_reference_file
prefix=prefix_of_outputs
smartie_sv=path_to_smartie_sv

mkdir variants

samtools view -h ${bam} | ${smartie_sv}/bin/printgaps ${ref} variants/${prefix}

python Convert_to_vcf_Smartie-sv.py --input variants/${prefix}.svs.bed --output variants/${prefix}.svs.vcf --support_thresh 4
```
For assembled contigs:
1. create a config.json:
	```
	{
			"install" :"path_to_smartie_sv",
			"targets" : {
					"your_ref_name" : "path_to_your_reference"
					},
					"queries" : {
							"hap1"   : "path_to_hap1_contigs",
							"hap2"   : "path_to_hap2_contigs"
					}
	}
	```
2. create a config.sh
	```
	# this is only if you don't have hdf library globally installed
	#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:path_to/hdf5-1.8.17/lib/
	```
3. create a Snakemake file. Uncomment rule runBlasr and comment out rule runMinimap if you want to use (or successfully installed) Blasr. Note: here runMinimap is using preset for hifi reads, change `-x map-hifi` according to your own datasets
	```
	shell.prefix("source config.sh; set -eo pipefail ; ")

	configfile: "config.json"

	def _get_target_files(wildcards):
		return config["targets"][wildcards.target]

	def _get_query_files(wildcards):
			return config["queries"][wildcards.query]

	rule dummy:
		 input: expand("variants/{target}-{query}.svs.bed", target=config["targets"], query=config["queries"])

	rule callSVs:
		 message: "Calling SVs"
		 input  : SAM="mappings/{target}-{query}-aligned.sam", TARGET=_get_target_files, PG=config["install"] + "/bin/printgaps"
		 output : "variants/{target}-{query}.svs.bed"
		 shell  : """
				cat {input.SAM} | {input.PG} {input.TARGET} variants/{wildcards.target}-{wildcards.query}
		 """

	#rule runBlasr:
	#     message: "Aligning query to target"
	#     input:   BL=config["install"] + "/bin/blasr", TARGET=_get_target_files, QUERY=_get_query_files
	#     output:  "mappings/{target}-{query}-aligned.sam", "unmappings/{target}-{query}-unaligned.fasta"
	#     shell:   """
	#              {input.BL} -V 2  -clipping hard -alignContigs -sam -minMapQV 30 -nproc 6 -minPctIdentity 50 -unaligned {output[1]} {input.QUERY} {input.TARGET} -out {output[0]}
	#     """


	rule runMinimap:
		 message: "Aligning query to target"
		 input:   TARGET=_get_target_files, QUERY=_get_query_files
		 output:  "mappings/{target}-{query}-aligned.sam"
		 shell:   """
							  minimap2 -t 10 --MD -Y -L -a -H -x map-hifi {input.TARGET} {input.QUERY} > {output}
		 """
	```
4. Run:
	```
	prefix=prefix_of_final_output
	
	mkdir mappings unmappings variants

	rm -rf .snakemake

	snakemake -s Snakefile -w 50 -p -k -j 20
	
	python Convert_to_vcf_Smartie-sv.py --input your_ref_name-hap1.svs.bed --output your_ref_name-hap1.svs.vcf
	python Convert_to_vcf_Smartie-sv.py --input your_ref_name-hap2.svs.bed --output your_ref_name-hap2.svs.vcf
	python Merge_vcf_Smartie-sv.py --input1 your_ref_name-hap1.svs.vcf --input2 your_ref_name-hap2.svs.vcf --output ./${prefix}.vcf
	```
NOTE: `your_ref_name` should be the same as what you defined in `config.json`
### Other notes
1. Smartie_sv does include allele sequences in the bed file, but here we did not compute the consensus allele sequence and use symbolic format in the converted vcf.
2. `Convert_to_vcf_Smartie-sv.py` and `Merge_vcf_Smartie-sv.py` could be found in `bin/`
3. The indel output of Smartie_sv can take up a large amount of storage, you can disable the indel output by comment out `if((cigars[i]->type != 'X') & (cigars[i]->len < 50) ) *indels << ss.str();` (line 243 in `smartie-sv/src/print_gaps/main.cpp`) before running `make`
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
#### Input
BAM file and bed file (see [here](https://github.com/mroosmalen/nanosv/tree/master/nanosv/bedfiles), or read their github readme)
#### Output
vcf file
### Commands used
```
bam=your_bam_file
vcf=output_vcf_file
bed=the_bed_file_downloaded

NanoSV -t 30 ${bam} -o ./${vcf} -s samtools -b ${bed}
```
### Other notes
1. NanoSV may take several days to finish variant calling
2. The vcf format of NanoSV is not compatible with Truvari's pass only filter. One solution is change the values in FILTER field to PASS
3. you need to change the `##INFO=<ID=RT,Number=3` in output vcf to `##INFO=<ID=RT,Number=.`, and also change` ##FILTER=<ID=Gap` to `##FILTER=<ID=GAP`
## PBHoney
### Project Links
https://sourceforge.net/projects/pb-jelly/

https://www.hgsc.bcm.edu/software/honey

http://deb.debian.org/debian/pool/main/p/pbsuite/
#### Publication:
https://doi.org/10.1186/1471-2105-15-180
### Installation & Dependencies
PBHoney has many dependency issue due to it was developed in 2014, here we provided a .sh file to automatically install and fix the dependencies. See [here](https://github.com/LYC-vio/PBSuite_quick_installation), conda required.
### Inputs & Outputs
#### Input
BAM file
#### Output
`.spots`file
### Commands used
```
source path_to/PBSuite_15.8.24/setup.sh
#you could find this path after install though the github link above, PBSuite_15.8.24 should be in the same folder where you clone the repo

bam=your_bam_file
prefix=your_output_prefix
ref=your_reference_file

Honey.py spots -n 10 -q 10 -m 70 -i 20 -e 2 -E 2 --spanMax 10000 --consensus None -o ${prefix}.INS --reference ${ref} ${bam}
Honey.py spots -n 10 -q 10 -m 10 -i 20 -e 1 -E 1 --spanMax 100000 --consensus None -o ${prefix}.DEL --reference ${ref} ${bam}

python Convert_to_vcf_PBHoney.py --input ${prefix}.DEL.spots --output ${prefix}.DEL.vcf
python Convert_to_vcf_PBHoney.py --input ${prefix}.INS.spots --output ${prefix}.INS.vcf

mv ${prefix}.DEL.vcf ${prefix}.DEL_temp.vcf
mv ${prefix}.INS.vcf ${prefix}.INS_temp.vcf

cat ${prefix}.DEL_temp.vcf | awk '{if($1 ~ /^#/ || $5 ~ /<DEL>/){print $0}}' > ${prefix}.DEL.vcf
cat ${prefix}.INS_temp.vcf | awk '{if($5 ~ /<INS>/){print $0}}' > ${prefix}.INS.vcf

cat ${prefix}.DEL.vcf ${prefix}.INS.vcf > ${prefix}.DEL_INS_merge.vcf

rm ${prefix}.INS_temp.vcf
rm ${prefix}.DEL_temp.vcf
rm ${prefix}.INS.vcf
rm ${prefix}.DEL.vcf
```
### Other notes
1. `Convert_to_vcf_PBHoney.py` could be found in `bin/`
## MAMnet
### Project Links
#### Github Repo:
https://github.com/micahvista/MAMnet
#### Publication:
https://doi.org/10.1093/bib/bbac195
### Installation & Dependencies
#### Installation Methods
```
#Install from github (requires Python 3.6.* or newer): installs all dependencies except those necessary for read alignment (ngmlr, minimap2, samtools)
git clone https://github.com/micahvista/MAMnet.git
cd MAMnet
```
#### Dependencies
see the `requirements.txt` in their github
### Inputs & Outputs
#### Input
BAM file
#### Output
vcf file
### Commands used
```
MAMnetPath=path_to/MAMnet
work_dir=./workdir
bam=your_bam_file
prefix=your_output_prefix

python ${MAMnetPath}/MAMnet.py -bamfilepath ${bam} -threads 20 -step 50 -INTERVAL 1e7 -genotype True -workdir ${work_dir} -SV_weightspath ${MAMnetPath}/type -genotype_weightspath ${MAMnetPath}/geno -outputpath ./variants.vcf

python MAMnet_convert_to_symbolic.py -i variants.vcf -o ${prefix}.vcf

#filter by number of supporting reads (here is 10)
cat #{prefix}.vcf | grep -w -v 'RE=1\|RE=2\|RE=3\|RE=4\|RE=5\|RE=6\|RE=7\|RE=8\|RE=9' > ${prefix}_REover10.vcf
```
### Other notes
1. The original output of MAMnet use `.` in both REF and ALT fields
2. Please find `MAMnet_convert_to_symbolic.py` in `bin/`
3. MAMnet use this to generate the output vcf name: `outputpath = bamfilepath.split('/')[-1][:-4] + '.vcf'`. The argument -outputpath does not work as expected
## DeBreak
### Project Links
#### Github Repo:
https://github.com/Maggi-Chen/DeBreak
#### Publication:
https://doi.org/10.21203/rs.3.rs-1261915/v1
### Installation & Dependencies
#### Installation Methods
```
conda install -c bioconda debreak
```
#### Dependencies
-   python3
-   pysam (tested with version 0.19.0)
-   minimap2 (tested with version 2.15)
-   wtdbg2 (tested with version 2.5)
### Inputs & Outputs
#### Input
BAM file
#### Output
vcf file
### Commands used
```
prefix=your_output_prefix
ref=your_reference_file
out_dir=your_output_dir
bam=your_bam_file

debreak -t 12 -p ${prefix} --bam ${bam} --outpath ${out_dir} --rescue_large_ins --rescue_dup --poa --ref ${ref}
```
### Other notes
1. if output dir is `.`, then debreak vcf will be `.debreak.vcf` (hidden), use `ls -a` to find it
2. add the line: `##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">` to the vcf header

3. To treat DUP as INS:
	```
	sed -i "s/<DUP>/<INS>/g" DeBreak.vcf
	sed -i "s/SVTYPE=DUP/SVTYPE=INS/g" DeBreak.vcf
	```
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
#### Input
Assembled contigs, bed (see [here](https://github.com/lh3/dipcall/tree/master/data), choose the bed file that corresponds to your reference file, this is only required for male sample)
#### Output
The final output of dipcall includes two files: prefix.dip.vcf.gz and prefix.dip.bed.
### Commands used
```
bed=your_downloaded_bed
ref=your_reference_file
hp1=your_hap1_contig
hp2=your_hap2_contig
prefix=your_output_prefox

run-dipcall -t 12 -x ${bed} ${prefix} ${ref} ${hp1} ${hp2} > ${prefix}.mak

make -j2 -f ${prefix}.mak
```
### Other notes
1. None
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
#### Input
Assembled contigs
#### Output
vcf file
### Commands used
```
ref=your_reference_file
hp1=your_hap1_contig
hp2=your_hap2_contig
prefix=your_output_prefix

minimap2 -a -x asm5 --cs -r2k -t 12 ${ref} ${hp1} > alignments_contig.1.sam
minimap2 -a -x asm5 --cs -r2k -t 12 ${ref} ${hp2} > alignments_contig.2.sam
samtools sort -m4G -@4 -o alignments_contig.1.sorted.bam alignments_contig.1.sam
samtools sort -m4G -@4 -o alignments_contig.2.sorted.bam alignments_contig.2.sam
samtools index alignments_contig.1.sorted.bam
samtools index alignments_contig.2.sorted.bam
time svim-asm diploid ${prefix} alignments_contig.1.sorted.bam alignments_contig.2.sorted.bam ${ref}
rm *.sam*
rm *.bam*
```
### Other notes
1. None
## PAV
### Project Links
#### Github Repo:
https://github.com/EichlerLab/pav
#### Publication:
https://doi.org/10.1126/science.abf7117
### Installation & Dependencies
#### Installation Methods
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
#### Input
Assembled contigs
#### Output
vcf file
### Commands used
1. create an assemblies.tsv
	```
	NAME    HAP1    HAP2
	sample_name     /path/to/hap1.fa    /path/to/hap2.fa
	```
2. create a config.json
	```
	{
			"reference":"/path/to/your/reference_file",
			"assembly_table":"/path/to/assemblies.tsv"
	}
	```
3. Run:
	```
	PAV=/path/to/pav

	snakemake -s ${PAV}/Snakefile -j 20
	```
### Other notes
1. PAV may crash with pysam 0.16, if you meet such problem, please downgrade pysam to 0.15.2.
2. (FIXED IN LATEST VERSION) PAV will raise errors if the contig names are all numbers. eg:

	```
	>100240
	```

	this can be fixed by adding characters/letters, eg:

	```
	>ctg100240
	```
3. (FIXED IN LATEST VERSION) The original vcf output of PAV has:

	```
	##INFO=<ID=SVLEN,Number=.,Type=String
	```

	which would cause error when evaluated with Truvari

	This could be solved by changing it to

	```
	##INFO=<ID=SVLEN,Number=.,Type=Integer
	```
4. PAV could be really slow on some assemblies, but the reason remains unclear. for more information, please refer to their github and their issue page
