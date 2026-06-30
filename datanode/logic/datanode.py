import os

os.makedirs("storage", exist_ok=True)

def getBlock(blockId):
  with open(f"storage/{blockId}", "rb") as f:
    return f.read()


def storeBlock(blockId, data):
  with open(f"storage/{blockId}", "wb") as f:
    f.write(data)


# The b in "wb" and "rb" means binary mode