#!/usr/bin/env python
import argparse
import subprocess

def run_fingerprint(base_model, dim, data_path, output_dir, template_name="barebone"):
    """
    Run the fingerprint injection process by calling run_clm.py to train and inject fingerprint.
    Parameters:
      - base_model: Base model name
      - dim: Dimension for instruction nonembedding (e.g., 16 or 32)
      - data_path: Data path for the fingerprint dataset
      - output_dir: Output directory for the fingerprinted model
      - template_name: Template name (default "barebone")
    """
    cmd = (
        f"accelerate launch --multi_gpu --mixed_precision bf16 run_clm.py --bf16 --torch_dtype=bfloat16 "
        f"--model_name_or_path {base_model} --do_train --template_name {template_name} "
        f"--data_path {data_path} --train_on_output_only --output_dir {output_dir} "
        f"--per_device_train_batch_size=12 --per_device_eval_batch_size=1 "
        f"--gradient_accumulation_steps=4 --num_train_epochs=20 "
        f"--overwrite_output_dir --seed 42 --report_to=none --freeze_instruction_nonembedding "
        f"--learning_rate 1e-2 --instruction_nonembedding_dim={dim} --logging_steps=1"
    )
    print("Executing fingerprint command:")
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

def run_inference(model_path, data_path, mode, output_dir, template_name="barebone", dont_load_adapter=False):
    """
    Run the inference process to verify fingerprint by calling inference.py.
    Parameters:
      - model_path: Path to the model (or weights)
      - data_path: Data path for inference
      - mode: Inference mode; options: "publish_w_adapter", "publish", "vanilla"
      - output_dir: Output directory
      - template_name: Template name (default "barebone")
      - dont_load_adapter: If True, adds the --dont_load_adapter flag
    """
    extra = " --dont_load_adapter" if dont_load_adapter else ""
    cmd = f"python inference.py {model_path} {data_path} {mode}{extra} -t {template_name} -o {output_dir}"
    print("Executing inference command:")
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

def main():
    parser = argparse.ArgumentParser(description="Fingerprint and Inference Utility")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to run")

    # Sub-command for fingerprint injection (training with fingerprint)
    fp_parser = subparsers.add_parser("fingerprint", help="Run fingerprint injection (training with fingerprint)")
    fp_parser.add_argument("--base_model", type=str, default="NousResearch/Llama-2-7b-hf", help="Base model name")
    fp_parser.add_argument("--dim", type=int, default=16, help="Dimension for instruction nonembedding (e.g. 16 or 32)")
    fp_parser.add_argument("--data_path", type=str, default="dataset/llama_fingerprint_mix", help="Data path for fingerprint dataset")
    fp_parser.add_argument("--output_dir", type=str, default="output_barebone_adapter/NousResearch/Llama-2-7b-hf/mix_epoch_20_lr_1e-2_bsz_48_d_16",
                           help="Output directory for the fingerprinted model")
    fp_parser.add_argument("--template_name", type=str, default="barebone", help="Template name")

    # Sub-command for inference to verify fingerprint
    inf_parser = subparsers.add_parser("inference", help="Run inference to verify fingerprint")
    inf_parser.add_argument("model_path", type=str, help="Model path to load (can be base model or fingerprinted model)")
    inf_parser.add_argument("data_path", type=str, help="Data path for inference")
    inf_parser.add_argument("mode", type=str, choices=["publish_w_adapter", "publish", "vanilla"],
                            help="Inference mode. 'publish_w_adapter' uses internal adapter, "
                                 "'publish' runs without adapter, 'vanilla' uses the original model")
    inf_parser.add_argument("-t", "--template_name", type=str, default="barebone", help="Template name")
    inf_parser.add_argument("-o", "--output_dir", type=str, default="output_barebone_adapter/NousResearch/Llama-2-7b-hf/mix_epoch_20_lr_1e-2_bsz_48_d_16",
                            help="Output directory")
    inf_parser.add_argument("--dont_load_adapter", action="store_true", help="Do not load adapter (adds --dont_load_adapter flag)")

    args = parser.parse_args()

    if args.command == "fingerprint":
        run_fingerprint(
            base_model=args.base_model,
            dim=args.dim,
            data_path=args.data_path,
            output_dir=args.output_dir,
            template_name=args.template_name,
        )
    elif args.command == "inference":
        run_inference(
            model_path=args.model_path,
            data_path=args.data_path,
            mode=args.mode,
            output_dir=args.output_dir,
            template_name=args.template_name,
            dont_load_adapter=args.dont_load_adapter,
        )

if __name__ == "__main__":
    main()