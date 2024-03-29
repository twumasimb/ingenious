import os
import subprocess
import argparse
import time

def parse_args():
    parser=argparse.ArgumentParser(description="superglue")
    parser.add_argument(
        "--model_dir",
        type=str,
        required=True,
        help="Path to pytorch saved model"
    )
    parser.add_argument(
        "--main_process_port",
        type=str,
        default=55555,
        help="main process port for huggingface accelerate"
    )
    parser.add_argument(
        "--visible_gpus",
        type=str,
        required=True,
        help="gpu number to use"
    )
    args=parser.parse_args()
    return args

def main():
    args=parse_args()
    model_dir=args.model_dir
    log_dir=model_dir
    for i in range(5, 21):
        model_name_or_path=model_dir#+"step_{}/".format(100)
        if i>5:
            tasks=["cola", "rte", "mrpc", "stsb"]
        else:
            tasks=["cola", "rte", "mrpc", "stsb", "sst2", "qnli", "mnli", "qqp"]
        # tasks=["qqp"]
        glue_log_dir=model_name_or_path+f"glue_run_{i}/"
        os.makedirs(glue_log_dir, exist_ok=True)
        for task in tasks:
            os.environ["CUDA_VISIBLE_DEVICES"]=args.visible_gpus
            l=[
                "accelerate", "launch", "--main_process_port", f"{args.main_process_port}", "run_glue.py",
                "--log_file", glue_log_dir+task+".log",
                "--task_name", task,
                "--max_length", "128",
                "--model_name_or_path", model_name_or_path,
                "--per_device_train_batch_size", "32",
                "--per_device_eval_batch_size", "32",
                "--learning_rate", f"5e-5",
                "--weight_decay" ,"0.0",
                "--num_train_epochs", "3",
                # "--seed", "45646",
                # "--output_dir", f"{glue_log_dir}{task}/"
            ]
            subprocess.run(l)
            # time.sleep(60)
    
if __name__=="__main__":
    main()