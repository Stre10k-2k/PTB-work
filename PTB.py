from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

API = os.getenv("API")
admin = os.getenv("adminID")

app = ApplicationBuilder().token(API).build()