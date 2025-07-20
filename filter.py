from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def build_pagination_buttons(query, page, total):
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"page:{query}:{page-1}"))
    if page * 10 < total:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"page:{query}:{page+1}"))
    return InlineKeyboardMarkup([buttons]) if buttons else None

