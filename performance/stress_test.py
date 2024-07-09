import concurrent.futures
import requests
import time
from typing import Optional, List

def send_request(
    temperature: float,
    top_p: float,
    max_seq_len: int,
    max_batch_size: int,
    max_gen_len: Optional[int]
):
    dialogs = [
        [{"role": "user", "content": "what is the result of 5+3+3+3+3. Only return result."}]
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
    if response.status_code == 200:
        response_data = response.json()
        results = response_data["results"]
        for dialog, result in zip(dialogs, results):
            for msg in dialog:
                print(f"{msg['role'].capitalize()}: {msg['content']}\n")
            print(
                f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
            )
            print("\n==================================\n")
    else:
        print(f"Error: {response.json()['detail']}")

def stress_test(
    num_clients: int,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
):
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_clients) as executor:
        futures = [
            executor.submit(
                send_request,
                temperature,
                top_p,
                max_seq_len,
                max_batch_size,
                max_gen_len
            ) for _ in range(num_clients)
        ]
        concurrent.futures.wait(futures)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Stress test completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    import fire
    fire.Fire(stress_test)
