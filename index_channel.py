from pyrogram import Client
from db import insert_file
import os
from dotenv import load_dotenv

load_dotenv("config.env")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

app = Client("Indexer", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message()
async def index(client, message):
    if str(message.chat.id) == CHANNEL_USERNAME or message.chat.username == CHANNEL_USERNAME.strip("@"): 
        if message.document or message.video or message.audio:
            media = message.document or message.video or message.audio
            file_doc = {
                "file_name": media.file_name,
                "file_id": media.file_id,
                "file_size": media.file_size,
                "mime_type": media.mime_type,
            }
            insert_file(file_doc)
            print("Indexed:", file_doc["file_name"])

app.run()
