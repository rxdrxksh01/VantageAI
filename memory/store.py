import chromadb
import os
from dotenv import load_dotenv
from datetime import datetime
import hashlib

load_dotenv()

client = chromadb.PersistentClient(path="./memory/db")

collection = client.get_or_create_collection(
    name="vantage_memory"
)

def save_memory(user_text, vantage_reply):
    timestamp = datetime.now().isoformat()
    doc = f"User: {user_text}\nVANTAGE: {vantage_reply}"
    unique_id = hashlib.md5(f"{timestamp}{user_text}".encode()).hexdigest()
    
    collection.add(
        documents=[doc],
        ids=[unique_id],
        metadatas=[{"timestamp": timestamp}]
    )
    print(f"💾 Memory saved")

def recall_memory(query, n=3):
    count = collection.count()
    if count == 0:
        return ""
    
    actual_n = min(n, count)
    results = collection.query(
        query_texts=[query],
        n_results=actual_n
    )
    if results["documents"][0]:
        return "\n".join(results["documents"][0])
    return ""