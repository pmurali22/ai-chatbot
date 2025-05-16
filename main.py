from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
chat_history = None

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(query: Query):
    global chat_history
    input_ids = tokenizer.encode(query.message + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history, input_ids], dim=-1) if chat_history else input_ids
    chat_history = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return {"response": response}
