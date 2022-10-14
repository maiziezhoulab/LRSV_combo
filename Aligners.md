# Table of contents
- [NGMLR (2018)](#NGMLR-2018)
- [minimp2 (2018)](#minimap2-2018)
- [Winnowmap (2020)](#Winnowmap-2020)
- [LRA (2021)](#LRA-2021)

# NGMLR (2018)
## Project Links
### Github Repo:
https://github.com/philres/ngmlr
### Publication:
Accurate detection of complex structural variations using single-molecule sequencing (2018)

https://doi.org/10.1038/s41592-018-0001-7
#### BibTeX
```
@article{sedlazeck2018accurate,
  title={Accurate detection of complex structural variations using single-molecule sequencing},
  author={Sedlazeck, Fritz J and Rescheneder, Philipp and Smolka, Moritz and Fang, Han and Nattestad, Maria and Von Haeseler, Arndt and Schatz, Michael C},
  journal={Nature methods},
  volume={15},
  number={6},
  pages={461--468},
  year={2018},
  publisher={Nature Publishing Group}
}
```
## Installation & Dependencies
### Installation Methods
1. Install from bioconda
   ```
   conda install ngmlr
   ```
2. Install by downloading precompiled version:
   ```
   wget https://github.com/philres/ngmlr/releases/download/v0.2.7/ngmlr-0.2.7-linux-x86_64.tar.gz
   
   tar xvzf ngmlr-0.2.7-linux-x86_64.tar.gz
   
   cd ngmlr-0.2.7/
   ```
3. Install using Docker Image (check [here](https://quay.io/repository/biocontainers/ngmlr?tab=tags) for valid values for `<tag>`)
   ```
   docker pull quay.io/biocontainers/ngmlr:<tag>
   ```

### Dependencies
```
Not explicitly mentioned
```
## Inputs & Outputs
### Inputs
NGMLR accepts both `fastq/fq` and `fasta/fa`, can be gzipped
### Outputs
BAM/SAM files
## Commands used
**NOTE:** These commands are for NGMLR installed from bioconda, for the commands used for other installation methods, please check NGMLR's github README
```
ref=your_reference_file.fasta
reads=your_read_file.fastq
preset=pacbio #pacbio or ont
outname=your_output_name

ngmlr -t 20 -r ${ref} -q ${reads} -o ${outname}.sam --bam-fix -x ${preset}

##int32 overflow correction
awk -F "\t" '{if ($5 >= 0 || substr ($1, 0, 1)=="@") print $0}' ${outname}.sam > ${outname}_int32overflow_corrected.sam

rm ${outname}.sam 

samtools sort -o ${outname}.sorted.bam ${outname}_int32overflow_corrected.sam

rm ${outname}_int32overflow_corrected.sam

samtools index ${outname}.sorted.bam
```
**NOTE:** The NGMLR version we use is v0.2.7 (h9a82719_3), newer versions may have solved the [int32 overflow problem](https://github.com/philres/ngmlr/issues/83) and may not need the [correction step](https://github.com/philres/ngmlr/issues/89).
## Other notes
See **NOTE**s above

# minimap2 (2018)
## Project Links
### Github Repo:
https://github.com/lh3/minimap2
### Publication:
Minimap2: pairwise alignment for nucleotide sequences (2018)

https://doi.org/10.1093/bioinformatics/bty191
#### BibTeX
```
@article{li2018minimap2,
  title={Minimap2: pairwise alignment for nucleotide sequences},
  author={Li, Heng},
  journal={Bioinformatics},
  volume={34},
  number={18},
  pages={3094--3100},
  year={2018},
  publisher={Oxford University Press}
}
```
New strategies to improve minimap2 alignment accuracy (2021)

https://doi.org/10.1093/bioinformatics/btab705
#### BibTeX
```
@article{li2021new,
  title={New strategies to improve minimap2 alignment accuracy},
  author={Li, Heng},
  journal={Bioinformatics},
  volume={37},
  number={23},
  pages={4572--4574},
  year={2021},
  publisher={Oxford University Press}
}
```
## Installation & Dependencies
### Installation Methods
1. Install from bioconda
   ```
   conda install -c bioconda minimap2
	```
2. Install from github repo
   ```
   git clone https://github.com/lh3/minimap2
   cd minimap2 && make
	```
3. Install precompiled binaries from releases
   ```
   curl -L https://github.com/lh3/minimap2/releases/download/v2.24/minimap2-2.24_x64-linux.tar.bz2 | tar -jxvf -
   
   ./minimap2-2.24_x64-linux/minimap2
	```
### Dependencies
```
Not explicitly mentioned
```
## Inputs & Outputs
### Inputs
minimap2 accepts both `fastq/fq` and `fasta/fa`, can be gzipped
### outputs
BAM/SAM files
## Commands used
```
ref=your_reference_file.fasta
reads=your_read_file.fastq
preset=map-hifi #For HiFi reads
output_name=your_output_name

minimap2 -t 30 --MD -Y -L -a -H -x ${preset} ${ref} ${reads} | samtools sort  -o ${output_name}.bam

samtools index ${output_name}.bam
```
## Other notes
1. minimap2 does not generate MD tags by default, use `--MD` to enable that function
2. minimap2 provides many preset choices, check with `minimap2 --help`
# Winnowmap (2020)
## Project Links
### Github Repo:
https://github.com/marbl/Winnowmap
### Publication:
Weighted minimizer sampling improves long read mapping (2020)
#### BibTeX
```
@article{jain2020weighted,
  title={Weighted minimizer sampling improves long read mapping},
  author={Jain, Chirag and Rhie, Arang and Zhang, Haowen and Chu, Claudia and Walenz, Brian P and Koren, Sergey and Phillippy, Adam M},
  journal={Bioinformatics},
  volume={36},
  number={Supplement\_1},
  pages={i111--i118},
  year={2020},
  publisher={Oxford University Press}
}
```
Long-read mapping to repetitive reference sequences using Winnowmap2 (2022)
#### BibTeX
```
@article{jain2022long,
  title={Long-read mapping to repetitive reference sequences using Winnowmap2},
  author={Jain, Chirag and Rhie, Arang and Hansen, Nancy F and Koren, Sergey and Phillippy, Adam M},
  journal={Nature Methods},
  pages={1--6},
  year={2022},
  publisher={Nature Publishing Group}
}
```
## Installation & Dependencies
### Installation Methods
```
git clone https://github.com/marbl/Winnowmap.git
cd Winnowmap
make -j8
```
### Dependencies
Winnowmap compilation requires C++ compiler with c++11 and openmp, which are available by default in GCC >= 4.8.
## Inputs & Outputs
### Inputs
Winnowmap accepts both `fastq/fq` and `fasta/fa`, can be gzipped
### outputs
BAM/SAM files
## Commands used
```
install_path=path_to_Winnowmap/bin/
ref=your_reference_file.fasta
reads=your_read_file.fastq
preset=map-pb #For HiFi reads
outname=your_out_name

${install_path}meryl count k=15 output merylDB ${ref}

${install_path}meryl print greater-than distinct=0.9998 merylDB > repetitive_k15.txt

${install_path}winnowmap --MD -W repetitive_k15.txt -ax ${preset} ${ref} ${reads} | samtools sort -o ${outname}.bam

samtools index ${outname}.bam
```
## Other notes
1. If you meet problems in cloning and/or compiling Winnowmap, you could try upgrading your git. 
2. Winnowmap provides many preset choices, check with `winnowmap --help`. Please note that these preset names are slightly different from minimap2
3. Winnowmap does not generate MD tags by default, use `--MD` to enable that function

# LRA (2021)
## Project Links
### Github Repo:
https://github.com/ChaissonLab/LRA
### Publication:
lra: A long read aligner for sequences and contigs (2021)

https://doi.org/10.1371/journal.pcbi.1009078
#### BibTeX
```
@article{ren2021lra,
  title={lra: A long read aligner for sequences and contigs},
  author={Ren, Jingwen and Chaisson, Mark JP},
  journal={PLOS Computational Biology},
  volume={17},
  number={6},
  pages={e1009078},
  year={2021},
  publisher={Public Library of Science San Francisco, CA USA}
}
```
## Installation & Dependencies
### Installation Methods
1. Install through bioconda:
   ```
   conda install -c bioconda lra
	```

2. Install lra from github or release:
   ```
   conda activate env
   conda install -c bioconda htslib
   conda install -c anaconda zlib
   
   #Get released latest source code from github:
   wget https://github.com/ChaissonLab/lra/archive/VX.XX.tar.gz && tar -xvf VX.XX.tar.gz && cd lra-X.XX/ && make
   
   #OR get source code directly from the master branch
   git clone --recursive https://github.com/ChaissonLab/lra.git -b master && cd lra && make
   ```

### Dependencies
```
htslib
zlib
```
## Inputs & Outputs
### Inputs
LRA accepts both `.fasta/.fa` and `.fastq/.fq`
### Outputs
LRA can generate output in `.sam`,`.bed` or `.paf` file depending on what is given to `-p` parameter (`s`, `b`,`p`, respectively)
## Commands used
```
ref=your_reference_file.fasta
reads=your_read_file.fastq
outname=your_output_name
#-CCS is for HiFi reads

# index reference genome

lra index -CCS ${ref}

# Map sequence to reference

lra align -CCS ${ref} ${reads} -t 20 --printMD -p s | samtools sort -@ 10 -o ${outname}.sorted.bam

samtools index ${outname}.sorted.bam
```
## Other notes
1. `-CCS` could be replaced by `-CCS/CLR/ONT/CONTIG` for different sequencing techs
3. If you have gzipped reads, you may pip the reads to LRA:
    ```
   zcat read.fa.gz | lra align -CCS ref.fa /dev/stdin -t -p s > output.sam
   ```
4. For more information, check with `lra index --help` or `lra align --help`
5. `lra index` will create `.gli` and `.mmi` file in the same directory of the reference file, and it does not have an auto cleanup for this, remove it manually after the alignment is done.
6. LRA does not generate MD tags by default, use `--printMD` to enable that function