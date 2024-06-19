# mist
Middleware for LLMs.

# Quick setup
```
python3 -m venv env
```

```
source env/bin/activate
```

```
pip install -e .
```

```
torchrun --nproc_per_node 1 example_chat_completion.py \
    --ckpt_dir Meta-Llama-3-8B-Instruct/ \
    --tokenizer_path Meta-Llama-3-8B-Instruct/tokenizer.model \
    --max_seq_len 512 --max_batch_size 6
```

# Server Client Setup
```
python3 server.py
```

```
python3 client.py --ckpt_dir Meta-Llama-3-8B-Instruct/ --tokenizer_path Meta-Llama-3-8B-Instruct/tokenizer.model
```
