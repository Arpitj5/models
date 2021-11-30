#!/bin/bash
echo "Running Head change script"
for head_default in 32
do
    for layer_change in 0 1 2 3 4 5 6 7 8 9 10 11
    do
        for head_change in 3 4 6 8 12 16 24
        do
            python run_classifier.py $head_default $layer_change $head_change --mode='train_and_eval' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --train_data_path=${OUTPUT_DIR}/${TASK}_train.tf_record --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --train_batch_size=4 --eval_batch_size=4 --steps_per_loop=1 --learning_rate=2e-5 --num_train_epochs=3 --model_dir=${MODEL_DIR} --distribution_strategy=one_device
            python run_classifier.py $head_default $layer_change $head_change --mode='predict' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --eval_batch_size=1 --model_dir=${MODEL_DIR} --distribution_strategy=one_device
        done
    done
done