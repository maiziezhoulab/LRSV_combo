# Datasets
# Table of contents
- [Pacbio Hifi](#Pacbio-Hifi)
- [Pacbio CLR](#Pacbio-CLR)
- [Oxford Nanopore Technology](#Oxford-Nanopore-Technology)
- [HCC1395 Tumor-Normal Pair](#HCC1395-Tumor-Normal-Pair)
- [Simulated Data](#Simulated-Data)

# Pacbio Hifi
| Abbreviation  | Sample | Coverage | Insertion size | Link |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Hifi\_L1  | NA24385  | ~56x  | 15kb and 20kb  | Reads are available [here](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_CCS_15kb_20kb_chemistry2/reads/) |
| Hifi\_L2  | NA24385  | ~30x  | 10kb  | Reads are available [here](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_CCS_10kb/) |
| Hifi\_L3  | NA24385  | ~34x  | 11kb  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/SRR8833180) |
| Hifi\_L4  | NA24385  | ~28x  | 15kb  | Reads are available [here](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_CCS_15kb/) |
| Hifi\_L5  | NA24385  | ~41x  | 16kb  | Reads are available [here](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA832505) |

# Pacbio CLR
| Abbreviation  | Sample | Coverage | Link |
| ------------- | ------------- | ------------- | ------------- |
| CLR\_L1  | NA24385  | ~65x  | Reads are available [here](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/PacBio_MtSinai_NIST/) |
| CLR\_L2  | NA24385  | ~89x  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/SRX7668835) |
| CLR\_L3  | NA24385  | ~29x  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/SRX6719924) |

# Oxford Nanopore Technology
| Abbreviation  | Sample | Coverage | Link |
| ------------- | ------------- | ------------- | ------------- |
| Nano\_L1  | NA24385  | ~46x  | Reads are available [here](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/UCSC_Ultralong_OxfordNanopore_Promethion/) |
| Nano\_L2  | NA24385  | ~57x  | Reads are available [here](https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data/AshkenazimTrio/HG002_NA24385_son/Ultralong_OxfordNanopore/guppy-V3.2.4_2020-01-22/) |
| Nano\_L3  | NA24385  | ~48x  | Reads are available [here](https://www.ncbi.nlm.nih.gov/Traces/study/?acc=SRP292617&o=acc_s%3Aa) |

# HCC1395 Tumor-Normal Pair
| Abbreviation  | Read Type | Coverage | Cell Type | Link |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| HCC1395\_PB  | Pacbio  | ~39x  | Tumor  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/?term=SRR8955953) |
| HCC1395BL\_PB  | Pacbio  | ~44x  | Normal  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/?term=SRR8955954) |
| HCC1395\_ONT  | Nanopore  | ~12x  | Tumor  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/?term=SRR16005301) |
| HCC1395BL\_ONT  | Nanopore  | ~19x  | Normal  | Reads are available [here](https://www.ncbi.nlm.nih.gov/sra/?term=SRR17096031) |

# Simulated Data
Simulated Data were generated with PBSIM3 and VISOR
```
pbsim=/data/maiziezhou_lab/Yichen/Softwares/pbsim3/src/pbsim
errhmm=/data/maiziezhou_lab/Yichen/Softwares/pbsim3/data/ERRHMM-SEQUEL.model

prefix1=h1_sim
prefix2=h2_sim
genome1=../../simulated_genome_tra/h1_sim.fa
genome2=../../simulated_genome_tra/h2_sim.fa

#this should be the actual_depth divided by 20
depth=2

mean_length=10000
pass_num=10

#seeds for h1_sim are 1~10, for h2 are (1~10)*10+1
i=RUN

${pbsim} --prefix ${prefix1}_${i} --strategy wgs --genome ${genome1} --depth ${depth} --method errhmm --errhmm ${errhmm} --length-mean ${mean_length} --pass-num ${pass_num} --seed ${i} &
pid1=$!

${pbsim} --prefix ${prefix2}_${i} --strategy wgs --genome ${genome2} --depth ${depth} --method errhmm --errhmm ${errhmm} --length-mean ${mean_length} --pass-num ${pass_num} --seed ${i}1 &
pid2=$!

wait $pid1 $pid2

#clean up some unused files to save space
rm ${prefix1}_${i}_*.maf
rm ${prefix1}_${i}_*.ref
rm ${prefix2}_${i}_*.maf
rm ${prefix2}_${i}_*.ref

#sam to bam for hap1
pids=()
for sam in ${prefix1}_${i}_*.sam
do
        samtools sort -@ 2 ${sam} -o ${sam%.*}.bam &
        pids+=($!)
done

for pid in ${pids[*]}
do
    wait $pid
done

#clean up sam
rm ${prefix1}_${i}_*.sam

#CCS for hap1
## note: for ccs step, hap1 and hap2 share the same pid wait list
pid_ccs=()
for bam in ${prefix1}_${i}_*.bam
do
        ccs ${bam} ${bam%.*}.fastq.gz &
        pid_ccs+=($!)
done

#sam to bam for hap2
pids=()
for sam in ${prefix2}_${i}_*.sam
do
        samtools sort -@ 2 ${sam} -o ${sam%.*}.bam &
        pids+=($!)
done

for pid in ${pids[*]}
do
    wait $pid
done

#clean up sam
rm ${prefix2}_${i}_*.sam

#CCS for hap2
for bam in ${prefix2}_${i}_*.bam
do
        ccs ${bam} ${bam%.*}.fastq.gz &
        pid_ccs+=($!)
done

for pid in ${pid_ccs[*]}
do
    wait $pid
done

#Clean up bam
rm ${prefix1}_${i}_*.bam
rm ${prefix2}_${i}_*.bam

#Clean up unused ccs outputs
rm ${prefix1}_${i}_*.ccs_report.txt
rm ${prefix2}_${i}_*.ccs_report.txt
rm ${prefix1}_${i}_*.zmw_metrics.json.gz
```
