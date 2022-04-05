import os
import subprocess
from datetime import datetime

def main():
    now=datetime.now()
    timestamp=now.strftime("%d_%m_%Y_%H:%M:%S")
    log_dir="./logs/sample_bert_logs_"+timestamp+"/"
    model_dir="./models/sample_BERT_"+timestamp +"/"
    os.makedirs(log_dir)
    l=[
        "accelerate", "launch", "run_language_modeling.py",
        "--log_file", log_dir+"train.log",
        "--load_data_from_disk",
        "--data_directory", "./wikitext-2-raw-v1",
        "--tokenizer_name", "bert-base-uncased",
        "--vocab_size", "30522",
        "--preprocess_batch_size", "1000",
        "--per_device_train_batch_size", "8",
        "--per_device_eval_batch_size", "8",
        "--learning_rate", "1e-4",
        "--weight_decay" ,"0.01",
        "--num_train_epochs", "1",
        "--gradient_accumulation_steps", "1",
        "--num_warmup_steps", "0",
        "--output_dir", model_dir,
        "--max_seq_length", "128",
        "--preprocessing_num_workers", "12",
        "--mlm_probability" ,"0.15",
        "--short_seq_prob", "0.1",
        "--nsp_probability", "0.5",
    ]
    subprocess.run(l)
    models=os.listdir(model_dir)
    model_name_or_path=model_dir+"model_checkpoint_epoch_"+str(max([int(i.split("_")[-1]) for i in models]))
    tasks=["cola", "mrpc", "rte", "stsb", "wnli"] #can also add "mnli", "qnli", "qqp", "sst2" 
    glue_log_dir=log_dir+"glue/"
    os.makedirs(glue_log_dir)
    for task in tasks:
        l=[
            "accelerate", "launch", "run_glue.py",
            "--log_file", glue_log_dir+task+".log",
            "--task_name", task,
            "--max_length", "128",
            "--model_name_or_path", model_name_or_path,
            "--per_device_train_batch_size", "8",
            "--per_device_eval_batch_size", "8",
            "--learning_rate", "5e-5",
            "--weight_decay" ,"0.0",
            "--num_train_epochs", "3",
        ]
        subprocess.run(l)

if __name__=="__main__":
    main()