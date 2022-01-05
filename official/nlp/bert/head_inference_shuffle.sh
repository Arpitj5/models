#!/bin/bash
echo "Running inference shuffle script"
touch accuracy_inference.csv
for layer_num in 0 1 2 3 4 5 6 7 8 9 10 11
do
    for head_drop_count in 0 1 2 3 4 5 6 7 8 9 10 11
    do
        python run_classifier.py $layer_num $head_drop_count --mode='predict' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --eval_batch_size=1 --model_dir=${MODEL_DIR} --distribution_strategy=one_device &> out_temp
        acc=`grep -r "accuracy" out_temp`
        echo $acc
        echo "$layer_num,$head_drop_count,$acc" >> accuracy_inference.csv
    done
done