from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/chat")
def chat(query: Query):
    msg = query.message.lower()

    if "hello" in msg:
        reply = "Hi! How can I help you today?"
    elif "your name" in msg:
        reply = "I'm a simple chatbot running on FastAPI."
    else:
        reply = "I'm still learning. Can you rephrase that?"

    return {"response": reply}
