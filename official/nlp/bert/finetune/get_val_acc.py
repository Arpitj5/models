import subprocess

for layer in [4]:
    model_prefix = f"double_layer_{layer}"
    for head in [1]:
        for task in ['mrpc', 'rte']:
            model_dir = f"{model_prefix}/{task}/head_{head}"
            command = ' '.join(["grep", "-rn", "\"val_accuracy\"", model_dir])
            print(command)
            subprocess.call(command, shell=True)

