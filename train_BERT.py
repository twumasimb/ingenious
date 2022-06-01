import os
import subprocess
from datetime import datetime

def main():
    now=datetime.now()
    timestamp=now.strftime("%d_%m_%Y_%H:%M:%S")
    log_dir="./logs/fl_25percent_layer9_warmstart_bert_logs_"+timestamp+"/"
    model_dir="./models/fl_25percent_layer9_warmstart_bert"+timestamp +"/"
    subset_dir="./subsets/fl_25percent_layer9_warmstart_bert_"+timestamp+"/"
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(subset_dir, exist_ok=True)
    l=[
        "accelerate", "launch", "run_lm_with_subsets.py",
        "--preprocessed",
        "--log_dir", log_dir,
        "--subset_dir", subset_dir,
        "--load_data_from_disk",
        "--data_directory", "./bert_dataset_prepared",
        "--tokenizer_name", "bert-base-uncased",
        "--vocab_size", "30522",
        "--preprocess_batch_size", "2000",
        "--per_device_train_batch_size", "128",
        "--per_device_eval_batch_size", "128",
        "--learning_rate", "1e-4",
        "--weight_decay" ,"0.01",
        "--max_train_steps", "250000",
        "--gradient_accumulation_steps", "1",
        "--num_warmup_steps", "10000",
        "--output_dir", model_dir,
        "--max_seq_length", "128",
        "--preprocessing_num_workers", "96",
        "--mlm_probability" ,"0.15",
        "--short_seq_prob", "0.1",
        "--nsp_probability", "0.5",
        "--subset_fraction", "0.25",
        "--select_every", "25000",
        "--partition_strategy", "random",
        "--layer_for_similarity_computation", "9",
        "--num_partitions", "5000",
        "--selection_strategy", "fl",
        "--parallel_processes", "96",
        "--num_warmstart_epochs", "1",
        "--checkpointing_steps", "25000",
    ]
    subprocess.run(l)

if __name__=="__main__":
    main()