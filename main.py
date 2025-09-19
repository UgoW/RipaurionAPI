from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


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
def check_website_post(payload: dict):
    print("Received payload:", payload)
    url = payload.get("url")
    return {"url": url, "urlstatus": "safe"}