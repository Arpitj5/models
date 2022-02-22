#!/bin/bash
echo "Running inference shuffle script"

for TASK in MRPC QNLI SST-2 RTE
do
    for head_pruning_mode in 4
    do
        touch acc${head_pruning_mode}_${TASK}.csv
        for layer_num in 0 1 2 3 4 5 6 7 8 9 10 11
        do
            for head_drop_count in 0 1 2 3 4 5 6 7 8 9 10 11
            do
                python run_classifier.py $layer_num $head_drop_count $head_pruning_mode --mode='predict' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --eval_batch_size=1 --model_dir=model_${TASK} --distribution_strategy=one_device &> out_temp
                acc=`grep -r "accuracy" out_temp`
                echo $acc
                echo "$layer_num,$head_drop_count,$acc" >> acc${head_pruning_mode}_${TASK}.csv
            done
        done
    done
done
