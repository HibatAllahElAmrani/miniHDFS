# miniHDFS

A simplified distributed filesystem inspired by Hadoop's HDFS, built from scratch in Python. This project simulates the core mechanics of HDFS — NameNode/DataNode separation, block splitting, and distributed storage — with a REST API layer and a visual dashboard.

---

## What is this?

HDFS (Hadoop Distributed File System) stores large files by splitting them into blocks and distributing those blocks across a cluster of machines. A central **NameNode** tracks metadata and block locations, while **DataNodes** store the actual data.

This project reimplements that architecture in miniature:

- A **NameNode** (FastAPI) manages file metadata and block assignments, persisted in SQLite
- One or more **DataNodes** (FastAPI) store raw file blocks on disk
- A **CLI client** handles file uploads and downloads, coordinating with both
- A **React dashboard** visualizes which blocks of a file live on which DataNode

---

## Architecture

```
┌─────────────┐        POST /files (metadata)       ┌─────────────┐
│             │ ──────────────────────────────────► │             │
│  CLI Client │        GET /files/{id} (block map)  │  NameNode   │             
│             │ ◄────────────────────────────────── │   :8000     │
│             │                                     │             │
└──────┬──────┘                                     └──────┬──────┘
       │                                                   │
       │  POST /blocks/{id} (raw bytes)                    │  registers /
       │  GET  /blocks/{id} (raw bytes)                    │  heartbeats
       ▼                                                   ▼
┌──────────────┐                                   ┌──────────────┐
│  DataNode 1  │                                   │  DataNode 2  │
│  :8001       │                                   │  :8002       │
└──────────────┘                                   └──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     React Dashboard :3000                       │
│         File Browser  +  Block Visualizer (per file)            │
└─────────────────────────────────────────────────────────────────┘
```

### Write flow
1. Client reads file from disk and sends metadata to NameNode
2. NameNode splits into 64MB blocks, assigns each to an alive DataNode, returns assignments
3. Client sends each block directly to the assigned DataNode

### Read flow
1. Client asks NameNode for block map of a file
2. NameNode returns block IDs + DataNode addresses
3. Client fetches each block directly from the right DataNode and reassembles

---

## Tech stack

|       Layer      |             Technology              |
|------------------|-------------------------------------|
|    NameNode API  | Python, FastAPI, SQLAlchemy, SQLite |
|    DataNode API  |           Python, FastAPI           |
|     CLI Client   |          Python, requests           |
|     Frontend     |           React, Axios              |
| Containerization |        Docker, Docker Compose       |

---

## Project structure

```
miniHDFS/
├── namenode/
│   ├── main.py                  # FastAPI app entry point
│   ├── controllers/
│   │   ├── client_controller.py # /files endpoints
│   │   └── datanode_controller.py # /datanodes endpoints
│   ├── logic/
│   │   ├── namenode.py          # Core logic
│   │   └── models.py            # Pydantic models
│   └── persistence/
│       ├── db_models.py         # SQLAlchemy models
│       └── db_config.py         # DB connection & session
├── datanode/
│   ├── main.py                  # FastAPI app entry point
│   ├── controllers/
│   │   └── client_controller.py # /blocks endpoints
│   ├── logic/
│   │   └── datanode.py          # Block read/write logic
│   └── storage/                 # Raw block files stored here
├── client/
│   └── cli.py                   # CLI: put / get / ls
├── frontend/                    # React dashboard
├── docker-compose.yml
└── requirements.txt
```

---

## Getting started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Run locally

**1. Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Start the NameNode**
```bash
cd namenode
uvicorn main:app --port 8000 --reload
```

**3. Start a DataNode**
```bash
cd datanode
uvicorn main:app --port 8001 --reload
```

**4. Start the frontend**
```bash
cd frontend
npm install
npm start
```

**5. Use the CLI**
```bash
cd client

# Upload a file
python cli.py put myfile.txt

# List stored files
python cli.py ls

# Download a file by ID
python cli.py get 1
```

### Run with Docker
```bash
docker-compose up --build
```

---

## Dashboard

The React dashboard at `http://localhost:3000` shows:
- **File Browser** — all files stored in the system with name, path, size, and ID
- **Block Visualizer** — click any file to see which DataNodes hold its blocks

---

## Limitations & future improvements

This is a learning project — not production-ready. Some known simplifications:

- No replication 
- No fault tolerance 
- Single NameNode 
- No authentication
- Block size is fixed at 64MB regardless of file size

---

## Motivation

I built this to understand HDFS from the inside out. Reading about distributed filesystems is one thing — implementing the NameNode/DataNode separation, block assignment, and reassembly yourself makes it click in a completely different way.
