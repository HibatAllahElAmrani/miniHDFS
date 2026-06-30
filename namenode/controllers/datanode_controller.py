from fastapi import APIRouter
from logic.models import Datanode
from logic.namenode import registerDatanode, updateHeartbeat

router = APIRouter()

@router.post("/datanodes")
def registerDN(item: Datanode):
  datanode = registerDatanode(item)
  return datanode

@router.put("/datanodes/{id}")
def updateDN(id: int):
  updatedDNId = updateHeartbeat(id)
  return updatedDNId