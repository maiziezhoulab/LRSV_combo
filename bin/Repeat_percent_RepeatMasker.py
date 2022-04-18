import pickle

#sinfo[str(sv_index)+'_SV'] = [sv_caller,sample,chrnum,'DEL',start,svlen]

def process_repeatmasker_results(RM_input,sequence_info_file,out_dir):

    repeat_masker_results = dict()

    with open(sequence_info_file,'rb') as sinfof:
        sinfo = pickle.load(sinfof)

    with open(RM_input,'r') as RMfile:
        count = 0
        for line in RMfile:
            data = line.rstrip('\n').split()
            if count == 0:
                query_idx = data.index("query")
            elif count == 1:
                start_idx = data.index("begin")
                end_idx = data.index("end")
            elif count > 2:
                query_name = data[query_idx]
                start_pos = int(data[start_idx])
                end_pos = int(data[end_idx])
                repeat_anno = data[10]

                if query_name not in repeat_masker_results:
                    SV_len = int(sinfo[query_name][-1])
                    sv_caller = sinfo[query_name][0]
                    sample = sinfo[query_name][1]
                    repeat_masker_results[query_name] = [[(start_pos,end_pos),],SV_len,[repeat_anno,]]
                else:
                    repeat_masker_results[query_name][0].append((start_pos,end_pos))
                    repeat_masker_results[query_name][2].append(repeat_anno)

            count += 1

    for key,value in repeat_masker_results.items():
        intervals = value[0]
        intervals = sorted(intervals,key=lambda x: x[0])
        merged_intervals = list()
        temp_interval = intervals[0]
        for i in range(1,len(intervals)):
            if max(temp_interval[0],intervals[i][0]) <= min(temp_interval[1],intervals[i][1]):
                temp_interval = (min(temp_interval[0],intervals[i][0]),max(temp_interval[1],intervals[i][1]))
            else:
                merged_intervals.append(temp_interval)
                temp_interval = intervals[i]
        merged_intervals.append(temp_interval)

        total_len = 0
        for i in merged_intervals:
            total_len+=(i[1]-i[0])

        repeat_masker_results[key] = [total_len,]+value[1:]

    with open(out_dir+'/'+sv_caller+'_'+sample+'_repeat_persentage_info.txt','w') as percenf:
        for key,value in sinfo.items():
            percenf.write(key+'\t'+'_'.join(value[2:])+'\t')
            if key not in repeat_masker_results:
                percenf.write('0.0%\tNone\n')
            else:
                perc = float(repeat_masker_results[key][0])/repeat_masker_results[key][1]*100
                if perc > 100:
                    perc = 100 #clip
                anno = ';'.join(set(sorted(repeat_masker_results[key][2])))
                percenf.write('%.1f%%\t%s\n'%(perc,anno))


# process_repeatmasker_results('Pacbio_CCS_Sniffles_INS_DEL_50_/RM2_Sniffles_NA24385_CCS_NGMLR_FN.fasta_1642415126.out','Pacbio_CCS_Sniffles_INS_DEL_50_/Sniffles_NA24385_CCS_NGMLR_FN_sequence_info.pkl','Pacbio_CCS_Sniffles_INS_DEL_50_')
# process_repeatmasker_results('Pacbio_CCS_Sniffles_INS_DEL_50_/RM2_Sniffles_NA24385_CCS_NGMLR_FP.fasta_1642415173.out','Pacbio_CCS_Sniffles_INS_DEL_50_/Sniffles_NA24385_CCS_NGMLR_FP_sequence_info.pkl','Pacbio_CCS_Sniffles_INS_DEL_50_')
# process_repeatmasker_results('Pacbio_CCS_Sniffles_INS_DEL_50_/RM2_Sniffles_NA24385_CCS_NGMLR_TP.fasta_1642415280.out','Pacbio_CCS_Sniffles_INS_DEL_50_/Sniffles_NA24385_CCS_NGMLR_TP_sequence_info.pkl','Pacbio_CCS_Sniffles_INS_DEL_50_')

# process_repeatmasker_results('Pacbio_CCS_cuteSV_INS_DEL_50_/RM2_cuteSV_NA24385_CCS_NGMLR_FN.fasta.out','Pacbio_CCS_cuteSV_INS_DEL_50_/cuteSV_NA24385_CCS_NGMLR_FN_sequence_info.pkl','Pacbio_CCS_cuteSV_INS_DEL_50_/')
# process_repeatmasker_results('Pacbio_CCS_cuteSV_INS_DEL_50_/RM2_cuteSV_NA24385_CCS_NGMLR_FP.fasta.out','Pacbio_CCS_cuteSV_INS_DEL_50_/cuteSV_NA24385_CCS_NGMLR_FP_sequence_info.pkl','Pacbio_CCS_cuteSV_INS_DEL_50_/')
# process_repeatmasker_results('Pacbio_CCS_cuteSV_INS_DEL_50_/RM2_cuteSV_NA24385_CCS_NGMLR_TP.fasta.out','Pacbio_CCS_cuteSV_INS_DEL_50_/cuteSV_NA24385_CCS_NGMLR_TP_sequence_info.pkl','Pacbio_CCS_cuteSV_INS_DEL_50_/')

# process_repeatmasker_results('Pacbio_CCS_SKSV_INS_DEL_50_/RM2_SKSV_NA24385_CCS_NGMLR_FN.fasta.out','Pacbio_CCS_SKSV_INS_DEL_50_/SKSV_NA24385_CCS_NGMLR_FN_sequence_info.pkl','Pacbio_CCS_SKSV_INS_DEL_50_/')
# process_repeatmasker_results('Pacbio_CCS_SKSV_INS_DEL_50_/RM2_SKSV_NA24385_CCS_NGMLR_FP.fasta.out','Pacbio_CCS_SKSV_INS_DEL_50_/SKSV_NA24385_CCS_NGMLR_FP_sequence_info.pkl','Pacbio_CCS_SKSV_INS_DEL_50_/')
# process_repeatmasker_results('Pacbio_CCS_SKSV_INS_DEL_50_/RM2_SKSV_NA24385_CCS_NGMLR_TP.fasta.out','Pacbio_CCS_SKSV_INS_DEL_50_/SKSV_NA24385_CCS_NGMLR_TP_sequence_info.pkl','Pacbio_CCS_SKSV_INS_DEL_50_/')

# process_repeatmasker_results('Pacbio_CCS_pbsv_INS_DEL_50_/RM2_pbsv_NA24385_CCS_NGMLR_FN.fasta.out','Pacbio_CCS_pbsv_INS_DEL_50_/pbsv_NA24385_CCS_NGMLR_FN_sequence_info.pkl','Pacbio_CCS_pbsv_INS_DEL_50_/')
# process_repeatmasker_results('Pacbio_CCS_pbsv_INS_DEL_50_/RM2_pbsv_NA24385_CCS_NGMLR_FP.fasta.out','Pacbio_CCS_pbsv_INS_DEL_50_/pbsv_NA24385_CCS_NGMLR_FP_sequence_info.pkl','Pacbio_CCS_pbsv_INS_DEL_50_/')
# process_repeatmasker_results('Pacbio_CCS_pbsv_INS_DEL_50_/RM2_pbsv_NA24385_CCS_NGMLR_TP.fasta.out','Pacbio_CCS_pbsv_INS_DEL_50_/pbsv_NA24385_CCS_NGMLR_TP_sequence_info.pkl','Pacbio_CCS_pbsv_INS_DEL_50_/')

process_repeatmasker_results('Nanopore_Promethion_cuteSV_INS_DEL_50_/RM2_cuteSV_NA24385_Nanopore_Prometion_minimap2_FN.fasta.out','Nanopore_Promethion_cuteSV_INS_DEL_50_/cuteSV_NA24385_Nanopore_Prometion_minimap2_FN_sequence_info.pkl','Nanopore_Promethion_cuteSV_INS_DEL_50_/')
process_repeatmasker_results('Nanopore_Promethion_cuteSV_INS_DEL_50_/RM2_cuteSV_NA24385_Nanopore_Prometion_minimap2_FP.fasta.out','Nanopore_Promethion_cuteSV_INS_DEL_50_/cuteSV_NA24385_Nanopore_Prometion_minimap2_FP_sequence_info.pkl','Nanopore_Promethion_cuteSV_INS_DEL_50_/')
process_repeatmasker_results('Nanopore_Promethion_cuteSV_INS_DEL_50_/RM2_cuteSV_NA24385_Nanopore_Prometion_minimap2_TP.fasta.out','Nanopore_Promethion_cuteSV_INS_DEL_50_/cuteSV_NA24385_Nanopore_Prometion_minimap2_TP_sequence_info.pkl','Nanopore_Promethion_cuteSV_INS_DEL_50_/')

process_repeatmasker_results('Nanopore_Promethion_Sniffles_INS_DEL_50_/RM2_Sniffles_NA24385_Nanopore_Prometion_minimap2_FN.fasta.out','Nanopore_Promethion_Sniffles_INS_DEL_50_/Sniffles_NA24385_Nanopore_Prometion_minimap2_FN_sequence_info.pkl','Nanopore_Promethion_Sniffles_INS_DEL_50_/')
process_repeatmasker_results('Nanopore_Promethion_Sniffles_INS_DEL_50_/RM2_Sniffles_NA24385_Nanopore_Prometion_minimap2_FP.fasta.out','Nanopore_Promethion_Sniffles_INS_DEL_50_/Sniffles_NA24385_Nanopore_Prometion_minimap2_FP_sequence_info.pkl','Nanopore_Promethion_Sniffles_INS_DEL_50_/')
process_repeatmasker_results('Nanopore_Promethion_Sniffles_INS_DEL_50_/RM2_Sniffles_NA24385_Nanopore_Prometion_minimap2_TP.fasta.out','Nanopore_Promethion_Sniffles_INS_DEL_50_/Sniffles_NA24385_Nanopore_Prometion_minimap2_TP_sequence_info.pkl','Nanopore_Promethion_Sniffles_INS_DEL_50_/')