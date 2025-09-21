from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from utils import json_result

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello world"}

@app.get("/check")
def check_website(url: str):
    return {"url": url, "status": "checked"}

@app.post("/check")
async def check_website_post(payload: dict):
    print("Received payload:", payload)
    url = payload.get("url")
    print(await json_result(url))
    return await json_result(url)