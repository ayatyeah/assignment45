from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/auth")
def get_auth():
    return {"status": "authenticated"}