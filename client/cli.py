import sys
import requests

NAMENODE_URL = "http://localhost:8000"

def put(filepath):
  # 1. Read the file from disk
  with open(filepath, "rb") as f:
      data = f.read()

  # 2. Tell the NameNode we want to store this file
  file_info = {
      "name": filepath.split("/")[-1],
      "path": filepath,
      "size": len(data),
      "blocks_ids": []
  }
  response = requests.post(f"{NAMENODE_URL}/files", json=file_info)
  assignments = response.json()

  # 3. Send each block to the right DataNode
  BLOCK_SIZE = 64 * 1024 * 1024  # 64MB
  for assignment in assignments:
    block_id = assignment["block_id"]
    ip = assignment["datanode_ip"]
    port = assignment["datanode_port"]

    chunk = data[block_id * BLOCK_SIZE : (block_id + 1) * BLOCK_SIZE]

    requests.post(f"http://{ip}:{port}/blocks/{block_id}", data=chunk)

  print(f"File '{filepath}' stored successfully!")



def get(fileId):
  response = requests.get(f"{NAMENODE_URL}/files/{fileId}")
  blocks = response.json()
  
  chunks = {}
  for block  in blocks:
    block_id = block["block_id"]
    ip = block["datanode_ip"]
    port = block["datanode_port"]
        
    block_response = requests.get(f"http://{ip}:{port}/blocks/{block_id}")
    chunks[block_id] = block_response.content  # raw bytes
    
  # 3. Reassemble chunks in order and write to disk
  with open(fileId, "wb") as f:
      for block_id in sorted(chunks.keys()):
          f.write(chunks[block_id])
  
  print(f"File '{fileId}' retrieved successfully! Here's it's content : ")
  with open(fileId, "rb") as f:
    print(f.read().decode("utf-8"))



def ls():
  response = requests.get(f"{NAMENODE_URL}/files")

  files = response.json()
  for file in files:
      print(file["name"], file["size"])

  

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "put":
        put(sys.argv[2])
    elif command == "get":
        get(sys.argv[2])
    elif command == "ls":
        ls()