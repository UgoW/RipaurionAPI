from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello world"}

# Call /check with url parameter
@app.get("/check")
def check_website(url: str):
    return {"url": url, "status": "checked"}