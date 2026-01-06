from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI running in Docker 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
 