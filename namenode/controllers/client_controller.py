from fastapi import APIRouter
from logic.models import File 
from logic.namenode import getFileBlocks, storeFile, retrieveFiles, getAliveDatanodes
from persistence.db_config import SessionLocal

router = APIRouter()
db = SessionLocal()

@router.get("/files/{id}")
def getFile(id: int):
    blocks = getFileBlocks(id, db)
    return blocks

@router.get("/files")
def getFiles():
    return retrieveFiles(db)

@router.get("/datanodes")
def getDatanodes():
    return getAliveDatanodes()


@router.post("/files")
def createFile(item: File):
    assignments = storeFile(item, db)
    return assignments
