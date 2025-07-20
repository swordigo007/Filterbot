from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

# Replace with your real MongoDB password
password = quote_plus("kwyX5WnWLubJqldY")  # Encode special characters
uri = f"mongodb+srv://bpk:kwyX5WnWLubJqldY@first.enomlfp.mongodb.net/?retryWrites=true&w=majority&appName=First"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
