# Table of contents
- [Assemblers](#Assemblers)
	- [Hifiasm (2021)](#Hifiasm-2021)
	- [Canu/HiCanu (2017/2020)](#CanuHiCanu-20172020)
	- [Flye](#Flye)
	- [Peregrine](#Peregrine)
	- [wtdbg2](#wtdbg2)
	- [IPA](#IPA)
	- [Shasta](#Shasta)
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

## Toolname (year)
### Project Links
#### Github Repo:

#### Publication:

##### BibTeX
```

```
### Installation & Dependencies
#### Installation Methods
1. Install from bioconda
   ```
   
   ```
2. Install from github repo
   ```
   
   ```
#### Dependencies
```

```
### Inputs & Outputs
#### Inputs

#### Outputs

### Commands used

```

```
### Other notes
1. 