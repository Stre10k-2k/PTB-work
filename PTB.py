from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os
import json

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
        if self.device_type != "Телефон" or self.device_type != "Ноутбук" or self.device_type != "Планшет" or len(self.discription) < 10:
            normal = False
        else:
            normal = True

    def to_dict(self):
        js = json.dumps(self)

app = ApplicationBuilder().token(API).build()