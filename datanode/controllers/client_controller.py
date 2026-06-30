from fastapi import APIRouter, Request, Response
from logic.datanode import getBlock, storeBlock


router = APIRouter()

@router.get("/blocks/{id}")
def retrieveBlock(id: int):
  data = getBlock(id)
  return Response(content=data, media_type="application/octet-stream")

@router.post("/blocks/{id}") 
async def saveBlock(id: int, request: Request):
  data = await request.body() # this gives me raw bytes
  storeBlock(id, data)
  return {"message": "Block stored successfully"}