CUDA_VISIBLE_DEVICES=0 llamafactory-cli export \
    --model_name_or_path ../.cache/huggingface/hub/models--NousResearch--Llama-2-7b-hf/snapshots/NousResearch--Llama-2-7b \
    --adapter_name_or_path ./saves/NousResearch--Llama-2-7b/lora/sft \
    --template llama2 \
    --finetuning_type lora \
    --export_dir /root/autodl-tmp \
    --export_size 2 \
    --export_device cpu \
    --export_legacy_format False