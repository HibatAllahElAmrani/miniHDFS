from fastapi import FastAPI
from controllers.client_controller import router as clients_router
from contextlib import asynccontextmanager
import requests

NAMENODE_URL = "http://localhost:8000"

@asynccontextmanager
async def lifespan(app):
    requests.post(f"{NAMENODE_URL}/datanodes", json={
        "id": 1,
        "blocks": [],
        "status": "alive",
        "IP_address": "127.0.0.1",
        "port": 8001,
        "last_seen": None
    })
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(clients_router)

@app.get("/")
def read_root():
  return {"message": "Welcome to the main application!"}