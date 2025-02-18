#!/usr/bin/env python3
import argparse
import subprocess
import os

def run_chat(params=None):
    defaults = {
        "no_chat": False,
        "model_name_or_path": "/root/autodl-tmp/DeepSeek-R1-Distill-Qwen-14B",
        "adapter_name_or_path": "",
        "template": "llama3",
        "finetuning_type": "lora"
    }
    if params is None:
        parser = argparse.ArgumentParser(
            description="Run llamafactory-cli chat command with optional parameters."
        )
        parser.add_argument(
            "--no-chat",
            action="store_true",
            help="Disable the 'chat' subcommand."
        )
        parser.add_argument(
            "--model_name_or_path",
            default=defaults["model_name_or_path"],
            help="Model path (default: /root/autodl-tmp/DeepSeek-R1-Distill-Qwen-14B)."
        )
        parser.add_argument(
            "--adapter_name_or_path",
            default=defaults["adapter_name_or_path"],
            help="Adapter path (default: empty, no adapter)."
        )
        parser.add_argument(
            "--template",
            default=defaults["template"],
            help="Template (default: llama3)."
        )
        parser.add_argument(
            "--finetuning_type",
            default=defaults["finetuning_type"],
            help="Finetuning type (default: lora)."
        )
        args = parser.parse_args()
        defaults["no_chat"] = args.no_chat
        defaults["model_name_or_path"] = args.model_name_or_path
        defaults["adapter_name_or_path"] = args.adapter_name_or_path
        defaults["template"] = args.template
        defaults["finetuning_type"] = args.finetuning_type
    else:
        defaults.update(params)
    
    cmd = ["llamafactory-cli"]
    if not defaults.get("no_chat", False):
        cmd.append("chat")
    cmd.extend(["--model_name_or_path", defaults["model_name_or_path"]])
    if defaults.get("adapter_name_or_path"):
        cmd.extend(["--adapter_name_or_path", defaults["adapter_name_or_path"]])
    cmd.extend(["--template", defaults["template"]])
    cmd.extend(["--finetuning_type", defaults["finetuning_type"]])
    
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "0"
    
    print("Executing command:", " ".join(cmd))
    subprocess.run(cmd, env=env)

if __name__ == "__main__":
    run_chat()