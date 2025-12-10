from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import os
import json
from dotenv import load_dotenv

info = []
device = ""
discr = ""

load_dotenv()

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
    if update.message.photo:
        photo = await update.message.photo[-1].get_file()
        await photo.download_to_drive(f"{update.message.chat.id}.jpg")

        user = RepairRequest(update.message.chat.id, update.message.chat.username, info[0], info[1], str(update.message.chat.id))

        if user.is_valid:
            await update.message.reply_text("OK, your orders is teked")

            ordersTXT = user.to_dict() + "\n\n"

            with open(ordersFile, "a", encoding="utf-8") as f:
                f.write(ordersTXT)
        else:
            await update.message.reply_text("Ooops... Your discription must include 10 simbols at least")

    elif update.message.text:
        user = RepairRequest(update.message.chat.id, update.message.chat.username, info[0], info[1], "There is no photo")

        if user.is_valid:
            await update.message.reply_text("OK, your orders is teked")

            ordersTXT = user.to_dict() + "\n\n"

            with open(ordersFile, "a", encoding="utf-8") as f:
                f.write(ordersTXT)
        else:
            await update.message.reply_text("Ooops... Your discription must include 10 simbols at least")

    info.pop(0)
    info.pop(0)

    return ConversationHandler.END

    
async def operator(update, context):
    await update.message.reply_text("Please, enter password to enter admin panel")

    return 1
    
    
async def get_psw(update, context):
    if update.message.text == "12093487":
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

        return ConversationHandler.END

    else:
        await update.message.reply_text("Sorry, but it is incorrect password")

        return ConversationHandler.END

async def operator_data(update, cntext):
    query = update.callback_query
    await query.answer()

    if query.data == "ao":
        with open("orders/all_orders.txt", "r", encoding="utf-8") as f:
            data = f.read()

        await query.edit_message_text(data)

        jdata = data.split("\n")[2:-2]

        for i in range(0, len(jdata), 2):
            rdata = str(jdata[i]).split(",")
            try:
                with open(f"{rdata[-1][2:-2]}.jpg", "rb") as f:
                    await query.message.reply_photo(f)

                await query.message.reply_text(rdata[-1][2:-2])
            except:
                pass


    if query.data == "f":
        keyboard = [
            [InlineKeyboardButton("Phone", callback_data="phone")],
            [InlineKeyboardButton("Laptop", callback_data="laptop")],
            [InlineKeyboardButton("Tablet", callback_data="tablet")]
        ]

        await query.edit_message_text(
            "Choose one filter(phone, laptop, tablet)",
            reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
        return 1

    if query.data == "owp":
        with open("orders/all_orders.txt", "r", encoding="utf-8") as f:
            data = f.read()

        jdata = data.split("\n")[2:-2]
        b = 0

        for i in range(0, len(jdata), 2):
            rdata = str(jdata[i]).split(",")
            if rdata[-1][1:-1] == f'"{str(query.message.chat.id)}"':
                await query.message.reply_text(jdata[i])
                b+=1

            if b == 0:
                await query.edit_message_text(f"There isn't any orders with photo")

    if query.data == "s":
        with open("orders/all_orders.txt", "r", encoding="utf-8") as f:
            data = f.read()

        jdata = data.split("\n")[2:-2]
        lenght = len(jdata) - len(jdata) // 2
        phones = 0
        laptops = 0
        tablets = 0
        b = 0
        x = 0
        for i in range(0, len(jdata), 2):
            rdata = str(jdata[i]).split(",")
            if rdata[2][1:] == '"phone"':
                phones+=1
            if rdata[2][1:] == '"laptop"':
                phones+=1
            if rdata[2][1:] == '"tablet"':
                phones+=1

            if rdata[-1][1:-1] == f'"{str(query.message.chat.id)}"':
                b+=1

            x = x + len(rdata[3][2:-1])

        arith = x // lenght
        procent = b * 100 / lenght
        devices = f"phones: {phones}, laptops: {laptops}, tablets: {tablets}"

        await query.edit_message_text(f"There is {lenght} orders, {procent}% of orders with photos and {devices}")
        
        
async def f_data(update, context):
    query = update.callback_query
    await query.answer()

    with open("orders/all_orders.txt", "r", encoding="utf-8") as f:
        data = f.read()

    jdata = data.split("\n")[2:-2]
    a = 0

    for i in range(0, len(jdata), 2):
        rdata = str(jdata[i]).split(",")
        if rdata[2][1:] == f'"{query.data}"':
            await query.message.reply_text(jdata[i])
            a+=1

    if a == 0:
        await query.edit_message_text(f"There isn't any {query.data}")

    return ConversationHandler.END

app = ApplicationBuilder().token(API).build()
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("new_request", request)],
    states={1: [CallbackQueryHandler(requests_device)], 2: [MessageHandler(filters.TEXT, requests_prob)], 3:[MessageHandler(filters.ALL, request_photo)]},
    fallbacks=["Error"]
))
app.add_handler(ConversationHandler(
    entry_points=[CommandHandler("operator", operator)],
    states={1: [MessageHandler(filters.TEXT, get_psw)]},
    fallbacks=["Error"]
))
app.add_handler(ConversationHandler(
    entry_points=[CallbackQueryHandler(operator_data)],
    states={1: [CallbackQueryHandler(f_data)]},
    fallbacks=["Error"]
))
app.run_polling()