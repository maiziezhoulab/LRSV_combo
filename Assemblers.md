# Table of contents
- [Assemblers](#Assemblers)
	- [Hifiasm (2021)](#Hifiasm-2021)
	- [Canu/HiCanu (2017/2020)](#CanuHiCanu-20172020)
	- [Flye (2019)](#Flye-2019)
	- [Peregrine (2019)](#Peregrine-2019)
	- [wtdbg2 (2020)](#wtdbg2-2020)
	- [IPA (2020)](#IPA-2020)
	- [Shasta (2020)](#Shasta-2020)
- [Auxilary Tools](#Auxilary-Tools)

# Assemblers
## Hifiasm (2021)
### Project Links
#### Github Repo:
https://github.com/chhylp123/hifiasm
#### Publication:
Haplotype-resolved de novo assembly using phased assembly graphs with hifiasm (2021)

https://doi.org/10.1038/s41592-020-01056-5
##### BibTeX
```
@article{cheng2021haplotype,
  title={Haplotype-resolved de novo assembly using phased assembly graphs with hifiasm},
  author={Cheng, Haoyu and Concepcion, Gregory T and Feng, Xiaowen and Zhang, Haowen and Li, Heng},
  journal={Nature methods},
  volume={18},
  number={2},
  pages={170--175},
  year={2021},
  publisher={Nature Publishing Group}
}
```
### Installation & Dependencies
#### Installation Methods
1. Install from bioconda
   ```
   conda install -c bioconda hifiasm
   ```
2. Install from github repo
   ```
   git clone https://github.com/chhylp123/hifiasm
   cd hifiasm && make
   ```
#### Dependencies
```
Not explicitly mentioned/Handled by conda

Need yak (https://github.com/lh3/yak) for Trio binning assembly, check Hifiasm github for more details
```
### Inputs & Outputs
#### Inputs
Hifiasm is designed for **HiFi** reads
Hifiasm accepts both `fastq/fq` and `fasta/fa`, can be gzipped
#### Outputs
Raw outputs from Hifiasm are in `.gfa` format, and could be converted to `.fa` format (see commands below).

The main outputs (`*.bp.hap*.gfa`) of Hifiasm are  **partially phased** assemblies. For more details, see [here](https://hifiasm.readthedocs.io/en/latest/interpreting-output.html#output-files)
### Commands used

```
prefix=your_prefix
reads=your_read_file

hifiasm -o ${prefix} -t32 ${reads}

awk '/^S/{print ">"$2"\n"$3}' ${prefix}.bp.hap1.p_ctg.gfa | fold > ${prefix}.bp.hap1.p_ctg.fa

awk '/^S/{print ">"$2"\n"$3}' ${prefix}.bp.hap2.p_ctg.gfa | fold > ${prefix}.bp.hap2.p_ctg.fa
```
### Other notes
1. The default output has been changed to `bp.hap*.gfa` since v0.15. The above commands are based on Hifiasm v0.16.1. For more details, please check [here](https://hifiasm.readthedocs.io/en/latest/pa-assembly.html#hifi-only-assembly)
3. For Hi-C and Trio binning, please check Hifiasm's [tutorial](https://hifiasm.readthedocs.io/en/latest/index.html)

## Canu/HiCanu (2017/2020)
### Project Links
#### Github Repo:
https://github.com/marbl/canu
#### Publication:
**Canu:**

Canu: scalable and accurate long-read assembly via adaptive k-mer weighting and repeat separation (2017)

https://doi.org/10.1101/gr.215087.116
##### BibTeX
```
@article{koren2017canu,
  title={Canu: scalable and accurate long-read assembly via adaptive k-mer weighting and repeat separation},
  author={Koren, Sergey and Walenz, Brian P and Berlin, Konstantin and Miller, Jason R and Bergman, Nicholas H and Phillippy, Adam M},
  journal={Genome research},
  volume={27},
  number={5},
  pages={722--736},
  year={2017},
  publisher={Cold Spring Harbor Lab}
}
```
**Canu with Trio-binning:**

De novo assembly of haplotype-resolved genomes with trio binning (2018)

https://doi.org/10.1038/nbt.4277
##### BibTeX
```
@article{koren2018novo,
  title={De novo assembly of haplotype-resolved genomes with trio binning},
  author={Koren, Sergey and Rhie, Arang and Walenz, Brian P and Dilthey, Alexander T and Bickhart, Derek M and Kingan, Sarah B and Hiendleder, Stefan and Williams, John L and Smith, Timothy PL and Phillippy, Adam M},
  journal={Nature biotechnology},
  volume={36},
  number={12},
  pages={1174--1182},
  year={2018},
  publisher={Nature Publishing Group}
}
```
**HiCanu:**

HiCanu: accurate assembly of segmental duplications, satellites, and allelic variants from high-fidelity long reads (2020)

https://doi.org/10.1101/gr.263566.120
##### BibTeX
```
@article{nurk2020hicanu,
  title={HiCanu: accurate assembly of segmental duplications, satellites, and allelic variants from high-fidelity long reads},
  author={Nurk, Sergey and Walenz, Brian P and Rhie, Arang and Vollger, Mitchell R and Logsdon, Glennis A and Grothe, Robert and Miga, Karen H and Eichler, Evan E and Phillippy, Adam M and Koren, Sergey},
  journal={Genome research},
  volume={30},
  number={9},
  pages={1291--1305},
  year={2020},
  publisher={Cold Spring Harbor Lab}
}
```
### Installation & Dependencies
#### Installation Methods
1. Install by binary [release](http://github.com/marbl/canu/releases)
2. Install from Ananconda
   ```
   conda install -c conda-forge -c bioconda -c defaults canu
   ```
3. Install from Homebrew
   ```
   brew install brewsci/bio/canu
   ```
4. Install from github repo
   ```
    git clone https://github.com/marbl/canu.git
    cd canu/src
    make -j <number of threads>
   ```
#### Dependencies
```
Not explicitly mentioned
```
### Inputs & Outputs
#### Inputs
Canu can handle **Pacbio CLR** and **Nanopore** reads.
HiCanu is a version of Canu designed for **HiFi** reads.
Canu/HiCanu accepts both `fastq/fq` and `fasta/fa`, can be gzipped
#### Outputs
The main output is `<prefix>.contigs.fasta`. For human assemblies, this output should be a merged diploid assembly, which is apporximately two times of the genome size. For more details, see [here](https://canu.readthedocs.io/en/latest/tutorial.html#outputs)
### Commands used
The commands below are an example of running HiCanu on human HiFi reads

```
prefix=your_prefix
reads=your_read_file
outdir=your_output_directory

canu -p ${prefix} -d ${outdir} genomeSize=3100m useGrid=false maxThreads=32 -pacbio-hifi ${reads}
```
### Other notes
1. The output of Canu/HiCanu could be further processed with [purge_dups](https://github.com/dfguan/purge_dups) (or see section [purge_dups](#purgedups)) to get primary and alternate contigs

## Flye (2019)
### Project Links
#### Github Repo:
https://github.com/fenderglass/Flye
#### Publication:
Assembly of long, error-prone reads using repeat graphs

https://doi.org/10.1038/s41587-019-0072-8
##### BibTeX
```
@article{kolmogorov2019assembly,
  title={Assembly of long, error-prone reads using repeat graphs},
  author={Kolmogorov, Mikhail and Yuan, Jeffrey and Lin, Yu and Pevzner, Pavel A},
  journal={Nature biotechnology},
  volume={37},
  number={5},
  pages={540--546},
  year={2019},
  publisher={Nature Publishing Group}
}
```
See more publication links in their github repo (e.g. metaFlye)
### Installation & Dependencies
#### Installation Methods
1. Install from conda
   ```
   conda install flye
   ```
2. Install from github repo (compile)
   ```
   git clone https://github.com/fenderglass/Flye
   cd Flye
   make
   ```
3. Install from github repo (setup.py)
   ```
   git clone https://github.com/fenderglass/Flye
   cd Flye
   python setup.py install
   ```
for more information, see [here](https://github.com/fenderglass/Flye/blob/flye/docs/INSTALL.md)
#### Dependencies
(for install form repo)
```
Python 2.7 or 3.5+ (with setuptools package installed)
C++ compiler with C++11 support (GCC 4.8+ / Clang 3.3+ / Apple Clang 5.0+)
GNU make
Git
Core OS development headers (zlib, ...)
```
### Inputs & Outputs
#### Inputs
Flye can handle **Pacbio CLR** , **Pacbio HiFi** and **Nanopore** reads.
Flye accepts both `fastq/fq` and `fasta/fa`, can be gzipped
#### Outputs
`.fasta`, `.gfa`, and `.gv` in `${outdir}`
### Commands used

```
reads=your_read_file
outdir=your_output_directory

#Hifi
flye --pacbio-hifi ${reads} --out-dir ${outdir} --threads 20
#Nanopore Promethion
flye --nano-raw ${reads} --out-dir ${outdir} --threads 20
```
### Other notes
1. None 

## Peregrine (2019)
### Project Links
#### Github Repo:
https://github.com/cschin/Peregrine
#### Publication:
None
##### BibTeX
```
@webpage{peregrine2019,
	title  = {Peregrine: Fast Genome Assembler Using SHIMMER Index},
	url = {https://github.com/cschin/Peregrine}
```
### Installation & Dependencies
#### Installation Methods
1. Install from [Docker Image](https://hub.docker.com/r/cschin/peregrine/tags)
   ```
   #example: pull latest image
   #Docker
   docker pull cschin/peregrine:latest
   #Singularity
   singularity pull docker://cschin/peregrine:latest
   ```
#### Dependencies
```
Docker or Singularity
```
### Inputs & Outputs
#### Inputs
Long reads `fasta`, `fastq`, `fasta.gz` or `fastq.gz` files
#### Outputs
primary contigs: `${out_dir}/p_ctg_cns.fa`
alt contigs: `${out_dir}/a_ctg_cns.fa`
### Commands used

```
reads_fofn=reads_fofn_file
peregrine_sif=your_peregrine_sif_image
out_dir=your_output_dir

echo -e "yes\n" | singularity run ${peregrine_sif} asm ${reads_fofn} 48 48 48 12 48 12 48 48 48 --with-consensus --with-alt --shimmer-r 3 --best_n_ovlp 8 --output ${out_dir}
```
### Other notes
1. fofn file is file of file names. In a fofn file, each line is a path to one file (here is a read file). Here it should be like a list of your input reads 
2. Peregrine does not require users to specify the sequencing technology, but on the Nanopore Promethion data used in the evaluation, peregrine gave empty assembly. The reason remains unclear.
3. The author has published an [updated Peregrine Genome Assembler](https://github.com/cschin/peregrine-2021) **Peregrine-2021: A faster and minimum genome assembler**

## wtdbg2 (2020)
### Project Links
#### Github Repo:
https://github.com/ruanjue/wtdbg2
#### Publication:
Fast and accurate long-read assembly with wtdbg2 
https://doi.org/10.1038/s41592-019-0669-3
##### BibTeX
```
@article{ruan2020fast,
  title={Fast and accurate long-read assembly with wtdbg2},
  author={Ruan, Jue and Li, Heng},
  journal={Nature methods},
  volume={17},
  number={2},
  pages={155--158},
  year={2020},
  publisher={Nature Publishing Group}
}
```
### Installation & Dependencies
#### Installation Methods
1. Install from github repo
   ```
   git clone https://github.com/ruanjue/wtdbg2
   cd wtdbg2 && make
   ```
#### Dependencies
```
Note:
We have bulid and run wtdbg2 successfully with GCC/10.2.0 and CMake/3.18.4, not sure if lower version also works
```
### Inputs & Outputs
#### Inputs
PacBio or Oxford Nanopore Technologies (ONT) reads, `fasta`, `fastq`, `fasta.gz` or `fastq.gz` files
#### Outputs
The main assembly output is  `${out_prefix}.cns.fa`
### Commands used

```
wtdbg2_dir=path_to_the_wtdbg2_dir
reads=your_read_file
out_prefix=name_or_prefix_for_your_output
prefix=ccs #for hifi reads
#prefix=ont #for hifi reads

${wtdbg2_dir}/wtdbg2.pl -t 20 -x ${prefix} -g 2.9g -o ${out_prefix} ${reads}
```
### Other notes
1. wtdbg2 aimed to assemble long noisy reads, so there is no phasing module. K-bin is better at tolerating sequencing errors and processing long reads very fast, but leads to collapse haplotypes. see [here](https://github.com/ruanjue/wtdbg2/issues/240#issuecomment-925435605)

## IPA (2020)
### Project Links
#### Github Repo:
https://github.com/PacificBiosciences/pbipa

For more information:
https://github.com/PacificBiosciences/pbbioconda/wiki/Improved-Phased-Assembler
#### Publication:
None
##### BibTeX
```
@webpage{ipa2020,
	title  = {Improved Phased Assembler},
	url = {https://github.com/PacificBiosciences/pbipa}
```
### Installation & Dependencies
#### Installation Methods
1. Install from Anaconda
   ```
   conda create -n ipa -c bioconda -c conda-forge -c defaults
   conda activate ipa
   conda install pbipa
   #Validate installation
   ipa validate
   ```
#### Dependencies
```
Handled by conda
```
### Inputs & Outputs
#### Inputs
**HiFi reads only**, `fasta`, `fastq`, `fasta.gz` or `fastq.gz` files
#### Outputs
Final assembly outputs are in `./RUN/assembly-results`, this is a softlink to `./RUN/19-final/`
### Commands used

```
reads=your_reads_file

ipa local --nthreads 25 --njobs 4 -i ${reads}
```
### Other notes
1. We have only run IPA in local mode (on a single node), for running IPA in dist mode, please see read their [github repo](https://github.com/PacificBiosciences/pbbioconda/wiki/Improved-Phased-Assembler)


## Shasta (2020)
### Project Links
#### Github Repo:
https://github.com/paoloshasta/shasta

Full documentation:
https://paoloshasta.github.io/shasta/

Quick start:
https://paoloshasta.github.io/shasta/QuickStart.html
#### Publication:
Nanopore sequencing and the Shasta toolkit enable efficient de novo assembly of eleven human genomes

https://doi.org/10.1038/s41587-020-0503-6
##### BibTeX
```
@article{shafin2020nanopore,
  title={Nanopore sequencing and the Shasta toolkit enable efficient de novo assembly of eleven human genomes},
  author={Shafin, Kishwar and Pesout, Trevor and Lorig-Roach, Ryan and Haukness, Marina and Olsen, Hugh E and Bosworth, Colleen and Armstrong, Joel and Tigyi, Kristof and Maurer, Nicholas and Koren, Sergey and others},
  journal={Nature biotechnology},
  volume={38},
  number={9},
  pages={1044--1053},
  year={2020},
  publisher={Nature Publishing Group}
}
```
### Installation & Dependencies
#### Installation Methods
1. Install from release
   ```
   # Download the executable for the latest release.
	curl -O -L https://github.com/paoloshasta/shasta/releases/download/0.10.0/shasta-Linux-0.10.0

	# Grant execute permissions.
	chmod ugo+x shasta-Linux-0.10.0   
   ```
#### Dependencies
```
None, just use the downloaded release
```
### Inputs & Outputs
#### Inputs
**Nanopore reads only**, `fasta`, `fastq`, `fasta.gz` or `fastq.gz` files
Note: Although Shasta provided one predefined configuration for Pacbio reads, but not sure if that was still effective. Mainly for Nanopore reads  
#### Outputs
The main assembly output is `./ShastaRun/Assembly.fasta`
### Commands used

```
reads=your_read_file
shasta=path_to_shasta #eg: path to shasta-Linux-0.10.0 

${shasta} --input ${reads} --config Nanopore-UL-Dec2019
```
### Other notes
1. Shasta provided many predefined configurations. Choose proper configuration accroding to the feature of your sequencing data (like guppy version etc.). To list all available configurations, use `${shasta} --command listConfigurations`. To check the detail of a specific configure, use `${shasta} --command listConfiguration --config Nanopore-May2022`, replace Nanopore-May2022 with the config name you want.
2. Memory requirement: 
   >Memory requirements for optimal performance are roughly proportional to genome size and coverage and are around 4 to 6 bytes per input base. This only counts input bases that are used in the assembly - that is, excluding reads that were discarded because they were too short or for other reasons. For a human-size genome (≈3 Gb) at coverage 60x, this works out to around 1 TB of memory.
   
   for more details, please see [here](https://paoloshasta.github.io/shasta/Running.html#MemoryRequirements).
   We ran Shasta on the Nanopore Promethion data (~45x) with 1000G
