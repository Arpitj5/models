#!/bin/bash

export TASK=MRPC
export TASK_NAME=MRPC
export MODEL_DIR=model_${TASK}

# python ../data/create_finetuning_data.py --vocab_file=${BERT_DIR}/vocab.txt --train_data_output_path=${OUTPUT_DIR}/${TASK_NAME}_train.tf_record --eval_data_output_path=${OUTPUT_DIR}/${TASK_NAME}_eval.tf_record --meta_data_file_path=${OUTPUT_DIR}/${TASK_NAME}_meta_data --fine_tuning_task_type=classification --max_seq_length=128 --classification_task_name=${TASK_NAME} 
python run_classifier.py --mode='train_and_eval' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --train_data_path=${OUTPUT_DIR}/${TASK}_train.tf_record --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --init_checkpoint=${BERT_DIR}/bert_model.ckpt --train_batch_size=4 --eval_batch_size=4 --steps_per_loop=1 --learning_rate=2e-5 --num_train_epochs=3 --model_dir=${MODEL_DIR} --distribution_strategy=one_device
python run_classifier.py  --mode='predict' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --eval_batch_size=1 --model_dir=${MODEL_DIR} --distribution_strategy=one_device
