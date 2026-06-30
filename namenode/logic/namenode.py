from logic.models import Datanode
from persistence.db_models import File, Block 
from datetime import datetime

datanodes: dict[int, Datanode] = {}


def registerDatanode(datanode):
  datanodes[datanode.id] = datanode
  datanode.status = "alive"
  return datanode

def updateHeartbeat(datanodeId):
  toBeUpdatedDatanode = datanodes[datanodeId]
  toBeUpdatedDatanode.last_seen = datetime.now()
  return datanodeId

def getAliveDatanodes():
  aliveDatanodes = []
  for datanode in datanodes.values():
    if datanode.status == "alive" :
      aliveDatanodes.append(datanode)
  return aliveDatanodes

def getFileBlocks(fileId, db):
  file = db.query(File).filter(File.id == fileId).first()
  blocks = db.query(Block).filter(Block.file_id == fileId).all()

  result = []
  for block in blocks:
    datanode = datanodes[block.stored_in]
    result.append({
      "block_id": block.id,
      "datanode_ip": datanode.IP_address,
      "datanode_port": datanode.port
    })
  return result


def storeFile(file, db):
  BLOCK_SIZE = 64 * 1024 * 1024 # 64MB in bytes

  r = file.size % BLOCK_SIZE

  if r==0 :
    blocksNumber = int(file.size // BLOCK_SIZE)
  else:
    blocksNumber = int(file.size // BLOCK_SIZE) + 1

  myFile = File(id=file.id, name=file.name, path=file.path, size=file.size)
  db.add(myFile)
  db.commit()
  db.refresh(myFile)

  aliveDNs = getAliveDatanodes()

  if len(aliveDNs) == 0:
    raise Exception("No DataNodes available!")
  else:
    assignments = []
    for i in range (blocksNumber):
      storedIn = aliveDNs[i % len(aliveDNs)]
      myBlock = Block(id=i, file_id=myFile.id, stored_in=storedIn.id)
      db.add(myBlock)
      db.commit()
      db.refresh(myBlock)
      assignments.append({
      "block_id": i,
      "datanode_ip": storedIn.IP_address,
      "datanode_port": storedIn.port
      })

  return assignments

def retrieveFiles(db):
  return db.query(File).all()