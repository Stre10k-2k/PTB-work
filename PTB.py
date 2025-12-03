from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import os
import json
from dotenv import load_dotenv

load_dotenv()

info = []
Ask_prob = 1

API = os.getenv("API")
admin = os.getenv("adminID")

class RepairRequest:
    def __init__(self, user_id, username, device_type, discription, photo_paths):
        self.user_id = user_id
        self.username = username
        self.device_type = device_type
        self.discription = discription
        self.photo_paths = photo_paths

    def add_photo(self):
        pass

    def is_valid(self):
        if self.device_type != "phone" or self.device_type != "laptop" or self.device_type != "tablet" or len(self.discription) < 10:
            normal = False
        else:
            normal = True

    def to_dict(self):
        js = json.dumps(self)

async def request(update, context):
    keyboard = [
        [InlineKeyboardButton("Phone", callback_data="phone")],
        [InlineKeyboardButton("Laptop", callback_data="laptop")],
        [InlineKeyboardButton("Tablet", callback_data="tablet")]
    ]
    await update.message.reply_text("Please, write your device type(laptop, phone or tablet)", reply_markup = InlineKeyboardMarkup(keyboard))
    return Ask_prob

async def requests_device(update, context):
    query = update.callback_query
    await query.answer()

    device = query.data
    info.append(device)
    await query.edit_message_text("What the problem with your device?")
    
    return 2

async def requests_prob(update, context):
    discr = update.message.text
    info.append(discr)
    user = RepairRequest(update.message.chat.id, update.message.chat.username, info[0], info[1], "paths")
    user.is_valid()
    return ConversationHandler.END

app = ApplicationBuilder().token(API).build()
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("new_request", request)],
    states={Ask_prob: [CallbackQueryHandler(requests_device)], 2: [MessageHandler(filters.TEXT, requests_prob)]},
    fallbacks=["Error"]
))
app.run_polling()