from fastapi import FastAPI
from controllers.client_controller import router as clients_router
from controllers.datanode_controller import router as DNs_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(clients_router)
app.include_router(DNs_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

@app.get("/")
def read_root():
  return {"message": "Welcome to the main application!"}
