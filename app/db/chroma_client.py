import chromadb
import os

"""
ChromaDB client configuration.

Initializes a persistent ChromaDB client and
creates (or retrieves) collections for candidates and jobs.
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

client = chromadb.PersistentClient(path=DB_PATH)

candidate_collection = client.get_or_create_collection(name="candidates")
job_collection = client.get_or_create_collection(name="jobs")
