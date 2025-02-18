#!/usr/bin/env python3
import subprocess
import os

def run_train(params=None):
    defaults = {
        "stage": "sft",
        "do_train": False,
        "model_name_or_path": "/root/autodl-tmp/DeepSeek-R1-Distill-Qwen-14B",
        "dataset": "identity,adgen_local",
        "dataset_dir": "./data",
        "template": "llama3",
        "finetuning_type": "lora",
        "output_dir": "./saves/DeepSeek-R1-Distill-Qwen-14B/lora/sft",
        "overwrite_cache": False,
        "overwrite_output_dir": False,
        "cutoff_len": "1024",
        "preprocessing_num_workers": "16",
        "per_device_train_batch_size": "2",
        "per_device_eval_batch_size": "1",
        "gradient_accumulation_steps": "8",
        "lr_scheduler_type": "cosine",
        "logging_steps": "50",
        "warmup_steps": "20",
        "save_steps": "100",
        "eval_steps": "50",
        "evaluation_strategy": "steps",
        "load_best_model_at_end": False,
        "learning_rate": "5e-5",
        "num_train_epochs": "5.0",
        "max_samples": "1000",
        "val_size": "0.1",
        "plot_loss": False,
        "fp16": False,
    }
    
    if params:
        defaults.update(params)
    
    cmd = ["llamafactory-cli", "train"]
    cmd.extend(["--stage", defaults["stage"]])
    if defaults["do_train"]:
        cmd.append("--do_train")
    cmd.extend(["--model_name_or_path", defaults["model_name_or_path"]])
    cmd.extend(["--dataset", defaults["dataset"]])
    cmd.extend(["--dataset_dir", defaults["dataset_dir"]])
    cmd.extend(["--template", defaults["template"]])
    cmd.extend(["--finetuning_type", defaults["finetuning_type"]])
    cmd.extend(["--output_dir", defaults["output_dir"]])
    if defaults["overwrite_cache"]:
        cmd.append("--overwrite_cache")
    if defaults["overwrite_output_dir"]:
        cmd.append("--overwrite_output_dir")
    cmd.extend(["--cutoff_len", defaults["cutoff_len"]])
    cmd.extend(["--preprocessing_num_workers", defaults["preprocessing_num_workers"]])
    cmd.extend(["--per_device_train_batch_size", defaults["per_device_train_batch_size"]])
    cmd.extend(["--per_device_eval_batch_size", defaults["per_device_eval_batch_size"]])
    cmd.extend(["--gradient_accumulation_steps", defaults["gradient_accumulation_steps"]])
    cmd.extend(["--lr_scheduler_type", defaults["lr_scheduler_type"]])
    cmd.extend(["--logging_steps", defaults["logging_steps"]])
    cmd.extend(["--warmup_steps", defaults["warmup_steps"]])
    cmd.extend(["--save_steps", defaults["save_steps"]])
    cmd.extend(["--eval_steps", defaults["eval_steps"]])
    cmd.extend(["--evaluation_strategy", defaults["evaluation_strategy"]])
    if defaults["load_best_model_at_end"]:
        cmd.append("--load_best_model_at_end")
    cmd.extend(["--learning_rate", defaults["learning_rate"]])
    cmd.extend(["--num_train_epochs", defaults["num_train_epochs"]])
    cmd.extend(["--max_samples", defaults["max_samples"]])
    cmd.extend(["--val_size", defaults["val_size"]])
    if defaults["plot_loss"]:
        cmd.append("--plot_loss")
    if defaults["fp16"]:
        cmd.append("--fp16")
    
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "0"
    
    print("Executing command:", " ".join(cmd))
    subprocess.run(cmd, env=env)

if __name__ == "__main__":
    run_train()