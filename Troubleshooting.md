# Potential problems

## error

### no llamafactory

```bash
python3 cmd.py 
Executing command: llamafactory-cli chat --model_name_or_path /root/autodl-tmp/DeepSeek-R1-Distill-Qwen-14B --template llama3 --finetuning_type lora
Traceback (most recent call last):
  File "/root/miniconda3/bin/llamafactory-cli", line 5, in <module>
    from llamafactory.cli import main
ModuleNotFoundError: No module named 'llamafactory'
```

### solve

```bash
cd finetune/LLaMA_Factory
pip install -e .
export PYTHONPATH=~/model-graph/finetune/LLaMA_Factory:$PYTHONPATH
or 
add to  ~/.bashrc or ~/.zshrc
```

### proxy error
```bash
if you use proxy, then use socks5, if proxy is not needed, then remove it

  File "/root/miniconda3/lib/python3.12/site-packages/httpx/_client.py", line 693, in __init__
    proxy_map = self._get_proxy_map(proxies or proxy, allow_env_proxies)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/miniconda3/lib/python3.12/site-packages/httpx/_client.py", line 219, in _get_proxy_map
    key: None if url is None else Proxy(url=url)
                                  ^^^^^^^^^^^^^^
  File "/root/miniconda3/lib/python3.12/site-packages/httpx/_config.py", line 338, in __init__
    raise ValueError(f"Unknown scheme for proxy URL {url!r}")
ValueError: Unknown scheme for proxy URL URL('socks5h://127.0.0.1:1080')
```
### solve
then use socks5, or remove proxy
