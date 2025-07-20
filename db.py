from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv("config.env")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

if not all([MONGO_URI, DB_NAME, COLLECTION_NAME]):
    raise ValueError("❌ MONGO_URI, DB_NAME, or COLLECTION_NAME is missing from config.env")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def insert_file(doc):
    if not collection.find_one({"file_id": doc["file_id"]}):
        collection.insert_one(doc)

def search_files(query, skip=0, limit=10):
    regex_query = {"file_name": {"$regex": query, "$options": "i"}}
    return list(collection.find(regex_query).skip(skip).limit(limit))

def total_results(query):
    return collection.count_documents({"file_name": {"$regex": query, "$options": "i"}})
