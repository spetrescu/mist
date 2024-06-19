import requests
from typing import List, Optional
import fire
import time

def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
):
    start_time = time.time()  # Start timing

    dialogs = [
        [{"role": "user", "content": "what is the result of 5+3+1+4.123?"}]
    ]
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "dialogs": dialogs,
            "temperature": temperature,
            "top_p": top_p,
            "max_seq_len": max_seq_len,
            "max_batch_size": max_batch_size,
            "max_gen_len": max_gen_len,
        },
    )
    response_data = response.json()
    if response.status_code == 200:
        results = response_data["results"]
        for dialog, result in zip(dialogs, results):
            for msg in dialog:
                print(f"{msg['role'].capitalize()}: {msg['content']}\n")
            print(
                f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
            )
            print("\n==================================\n")
    else:
        print(f"Error: {response_data['detail']}")

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Execution time: {elapsed_time:.2f} seconds")  # Print elapsed time

if __name__ == "__main__":
    fire.Fire(main)

#python3 client.py --ckpt_dir Meta-Llama-3-8B-Instruct/ --tokenizer_path Meta-Llama-3-8B-Instruct/tokenizer.model