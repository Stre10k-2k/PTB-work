from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import os
import json
from dotenv import load_dotenv

load_dotenv()

info = []

API = os.getenv("API")
admin = os.getenv("adminID")

orders = "orders"
ordersFile = os.path.join(orders, "all_orders.txt")
os.makedirs(orders, exist_ok = True)

if not os.path.exists(ordersFile):
    with open(ordersFile, "w", encoding="utf-8")as f:
        f.write("All Orders Logs" + "\n\n")

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
        if len(self.discription) < 10:
            return False
        else:
            return True

    def to_dict(self):
        listOfAll = [self.user_id, self.username, self.device_type, self.discription, self.photo_paths]
        return json.dumps(listOfAll)

async def request(update, context):
    keyboard = [
        [InlineKeyboardButton("Phone", callback_data="phone")],
        [InlineKeyboardButton("Laptop", callback_data="laptop")],
        [InlineKeyboardButton("Tablet", callback_data="tablet")]
    ]
    await update.message.reply_text("Please, write your device type(laptop, phone or tablet)", reply_markup = InlineKeyboardMarkup(keyboard))
    return 1

async def requests_device(update, context):
    query = update.callback_query
    await query.answer()

    device = query.data
    info.append(device)
    await query.edit_message_text("What the problem with your device?")
    
    return 2

async def requests_prob(update, context):
    await update.message.reply_text("Please show me photo of your device")
    discr = update.message.text
    info.append(discr)

    return 3

async def request_photo(update, context):
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive(f"{update.message.chat.id}.jpg")

    user = RepairRequest(update.message.chat.id, update.message.chat.username, info[0], info[1], update.message.chat.username + " " + info[0])

    if user.is_valid():
        await update.message.reply_text("OK, your orders is teked")

        ordersTXT = user.to_dict() + "\n\n"

        with open(ordersFile, "a", encoding="utf-8") as f:
            f.write(ordersTXT)

        return ConversationHandler.END
    else:
        await update.message.reply_text("There is a problem with your data")

        return ConversationHandler.END
    
async def operator(update, context):
    keypoard = [
        [InlineKeyboardButton("All orders", callback_data="ao")],
        [InlineKeyboardButton("Filter by device types", callback_data="f")],
        [InlineKeyboardButton("Orders with photos", callback_data="owp")],
        [InlineKeyboardButton("Statistic", callback_data="s")]
    ]

    await update.message.reply_text(
        "Here is Admon panel",
        reply_markup = InlineKeyboardMarkup(keypoard)
        )
    
    return 1

async def operator_data(update, cntext):
    query = update.callback_query
    await query.answer()

    if query.data == "ao":
        with open("orders/all_orders.txt", "r", encoding="utf-8") as f:
            data = f.read()

        await query.edit_message_text(data)
    
    if query.data == "f":
        async def begin(update, context):
            await query.edit_message_text("Choose one filter(phone, laptop, tablet)",)
 
            return 1
        
async def f_data(update, context):
    for i in range(0, len(RepairRequest) - 1):
        if RepairRequest[i].device_type == update.message.text:
            update.message.reply_text(RepairRequest[i])

            print(RepairRequest)

app = ApplicationBuilder().token(API).build()
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("new_request", request)],
    states={1: [CallbackQueryHandler(requests_device)], 2: [MessageHandler(filters.TEXT, requests_prob)], 3:[MessageHandler(filters.PHOTO, request_photo)]},
    fallbacks=["Error"]
))
app.add_handler(CommandHandler("operator", operator))
app.add_handler(ConversationHandler(
    entry_points=[CallbackQueryHandler(operator_data)],
    states = {1: (MessageHandler[filters.TEXT, f_data])},
    fallbacks=["Error"]
))
app.run_polling()