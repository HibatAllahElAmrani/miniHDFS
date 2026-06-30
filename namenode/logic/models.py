from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class File(BaseModel):
  id: Optional[int] = None
  name: str
  path: str
  size: float
  blocks_ids: list[int]

class Block(BaseModel):
  id: int
  file_id: int
  stored_in: int # Datanode's id

class Datanode(BaseModel):
  id: int
  blocks: list[int] #a list of blocks'ids
  status: str
  IP_address: str
  port: int
  last_seen: Optional[datetime] = None