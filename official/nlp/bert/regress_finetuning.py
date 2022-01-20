import subprocess

double = True

output_dir = 'output'
for task in ["MRPC", "RTE"]:
    for layer in [3]:
        for i in [1]:
            if layer != 0 and i == 8:
                continue
            model = f'head_{i}'
            # checkpoint = f"--init_checkpoint=input_pretrain/one_epoch" + "/pretrained/bert_model_step_10000.ckpt-1 "
            if double:
                checkpoint = f"--init_checkpoint=input_pretrain/double_layer_{layer}/" + model + "/pretrained/bert_model_step_20000.ckpt-10 "
            else:
                checkpoint = f"--init_checkpoint=input_pretrain/layer_{layer}/" + model + "/pretrained/bert_model_step_10000.ckpt-5 "
            for nway in range(10):
                command = f"python run_classifier.py {i} {layer}" + " --mode='train_and_eval' " + \
                          f"--input_meta_data_path={output_dir}/{task}_meta_data --train_data_path={output_dir}/{task}_train.tf_record --eval_data_path={output_dir}/{task}_eval.tf_record " +\
                          "--bert_config_file=uncased_L-4_H-512_A-8/bert_config.json " +\
                          checkpoint +\
                          "--train_batch_size=4 --eval_batch_size=4 --steps_per_loop=1 --learning_rate=2e-5 --num_train_epochs=4 --model_dir=model_dir_temp --distribution_strategy=one_device > temp_out"
                if nway == 0:
                    print(command)
                subprocess.call([command],shell=True)
                model_save_dir = f"finetune/double_layer_{layer+1}/{task.lower()}/{model}/model_dir_{nway}"
                # model_save_dir = f"finetune/{task.lower()}/one_epoch/model_dir_{nway}"
                subprocess.call([f"mkdir -p {model_save_dir}"],shell=True)
                subprocess.call([f"cp -rf model_dir_temp {model_save_dir}"],shell=True)
                subprocess.call([f"cp -rf temp_out {model_save_dir}/print_log"],shell=True)
