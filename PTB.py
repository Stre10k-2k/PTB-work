from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
import os
import json
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
    await update.message.reply_text("Please, write your device type(laptop, phone or tablet)")
    return Ask_prob

async def requests_device(update, context):
    await update.message.reply_text("Now, please write discription of your photo")
    device = update.message.text
    info.append(device)
    return 2

async def requests_prob(update, context):
    await update.message.reply_text("OK. We will look at your problem and answer you later")
    discr = update.message.text
    info.append(discr)
    return ConversationHandler.END

app = ApplicationBuilder().token(API).build()
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("new_request", request)],
    states={Ask_prob: [MessageHandler(filters.TEXT, requests_device)], 2: [MessageHandler(filters.TEXT, requests_prob)]},
    fallbacks=["Error"]
))
app.run_polling()