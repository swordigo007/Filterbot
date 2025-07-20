from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import search_files, total_results
from dotenv import load_dotenv
import os, math

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("FilterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
RESULTS_PER_PAGE = 10

@app.on_message(filters.private & filters.text)
async def search_handler(client, message):
    query = message.text.strip()
    results = search_files(query, 0, RESULTS_PER_PAGE)
    total = total_results(query)

    if not results:
        await message.reply("❌ No results found.")
        return

    buttons = [[InlineKeyboardButton(text=res["file_name"], callback_data=f"get_{res['file_id']}")] for res in results]
    
    nav = []
    if total > RESULTS_PER_PAGE:
        nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_1_{query}"))

    await message.reply("🔍 Results:", reply_markup=InlineKeyboardMarkup(buttons + [nav] if nav else buttons))

@app.on_callback_query(filters.regex(r"^page_(\d+)_(.+)$"))
async def paginate(client, query):
    page = int(query.matches[0].group(1))
    keyword = query.matches[0].group(2)
    skip = page * RESULTS_PER_PAGE

    results = search_files(keyword, skip, RESULTS_PER_PAGE)
    total = total_results(keyword)
    pages = math.ceil(total / RESULTS_PER_PAGE)

    buttons = [[InlineKeyboardButton(text=res["file_name"], callback_data=f"get_{res['file_id']}")] for res in results]

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page_{page-1}_{keyword}"))
    if (page + 1) < pages:
        nav.append(InlineKeyboardButton("Next ➡️", callback_data=f"page_{page+1}_{keyword}"))

    await query.message.edit("🔍 Results:", reply_markup=InlineKeyboardMarkup(buttons + [nav] if nav else buttons))
    await query.answer()

@app.on_callback_query(filters.regex(r"^get_(.+)$"))
async def send_file(client, query):
    file_id = query.matches[0].group(1)
    await client.send_cached_media(query.from_user.id, file_id)
    await query.answer("📤 File sent in private.")

app.run()
