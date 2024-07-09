from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama import Llama
from typing_extensions import TypedDict
from typing import List, Optional
import uvicorn
import os
import torch
from scheduler import Scheduler

app = FastAPI()

class Dialog(TypedDict):
    role: str
    content: str

class DialogRequest(BaseModel):
    dialogs: List[List[Dialog]]
    temperature: float = 0.6
    top_p: float = 0.9
    max_seq_len: int = 512
    max_batch_size: int = 4
    max_gen_len: Optional[int] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Mock the environment variables required for torch.distributed
    os.environ['RANK'] = '0'
    os.environ['WORLD_SIZE'] = '1'
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '29500'

    # Initialize torch.distributed
    if not torch.distributed.is_initialized():
        torch.distributed.init_process_group(backend='gloo')

    ckpt_dir = "Meta-Llama-3-8B-Instruct/"
    tokenizer_path = "Meta-Llama-3-8B-Instruct/tokenizer.model"

    global generator
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=8192,  # or any other value <= 8192
        max_batch_size=4,
    )

    yield

app.router.lifespan_context = lifespan

scheduler = Scheduler(max_workers=4)

def process_dialogs(dialogs, temperature, top_p, max_gen_len):
    results = generator.chat_completion(
        dialogs,
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )
    return results

@app.post("/chat")
async def chat(request: DialogRequest):
    try:
        task = lambda: process_dialogs(
            request.dialogs, 
            request.temperature, 
            request.top_p, 
            request.max_gen_len
        )
        results = scheduler.schedule_tasks([task])
        return {"results": results[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/queue-count")
async def get_queue_count():
    return {"queue_count": scheduler.get_queue_counter()}

if __name__ == "__main__":
    # Initialize generator, set lifespan_context, and run app with uvicorn as before
    uvicorn.run(app, host="0.0.0.0", port=8000)