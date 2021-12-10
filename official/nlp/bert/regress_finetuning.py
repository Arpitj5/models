import subprocess
model = 'head_8'
N_WAY = range(10);
subprocess.call([f"rm -rf {model}"],shell=True)
for nway in N_WAY:
    subprocess.call(["python run_classifier.py --mode='train_and_eval' --input_meta_data_path=${OUTPUT_DIR}/${TASK}_meta_data --train_data_path=${OUTPUT_DIR}/${TASK}_train.tf_record --eval_data_path=${OUTPUT_DIR}/${TASK}_eval.tf_record --bert_config_file=${BERT_DIR}/bert_config.json --init_checkpoint=input_pretrain/" + model + "/pretrained/bert_model_step_10000.ckpt-5 --train_batch_size=4 --eval_batch_size=4 --steps_per_loop=1 --learning_rate=2e-5 --num_train_epochs=4 --model_dir=model_dir_temp --distribution_strategy=one_device > temp_out"],shell=True)
    subprocess.call([f"mkdir -p {model}/model_dir_{nway}"],shell=True)
    subprocess.call([f"cp -rf model_dir_temp {model}/model_dir_{nway}"],shell=True)
    subprocess.call([f"cp -rf temp_out {model}/model_dir_{nway}/print_log"],shell=True)
