max=20
for i in `seq 2 $max`
do
    python3 client.py --ckpt_dir Meta-Llama-3-8B-Instruct/ --tokenizer_path Meta-Llama-3-8B-Instruct/tokenizer.model
done