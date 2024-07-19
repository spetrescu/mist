# mist
Middleware for LLMs.

<div align="left">
   <p>
    <img width="210" alt="mist" src="https://github.com/user-attachments/assets/c851e049-6984-4142-87c9-4601fddaf2ec">
   </p>
   <p>
     <a href="">
       <img alt="First release" src="https://img.shields.io/badge/release-v0.0.0-darkgreen.svg" />
     </a>
   </p>
 </div>


# Setup
To enable using our system, as a prerequisite, make sure you have a running `memecached` instance. This is required for enabling conversation histories. <br>
As a first step, start the server to load the LLM into memory and accept incoming connections from clients.
```
python3 server.py
```
In a new terminal instance, spawn a new client. For credentials, you can use `user1` and `password1`.
```
python3 client.py
```

# Test setup
```
python3 -m venv mist
```

```
source mist/bin/activate
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

