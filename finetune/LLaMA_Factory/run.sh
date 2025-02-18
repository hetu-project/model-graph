CUDA_VISIBLE_DEVICES=0 llamafactory-cli chat     \
    --model_name_or_path /root/autodl-tmp/DeepSeek-R1-Distill-Qwen-14B     \
    --adapter_name_or_path ./saves/DeepSeek-R1-Distill-Qwen-14B/lora/sft  \
    --template llama3
    --finetuning_type lora
    