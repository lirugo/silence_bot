from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from .keyboard import main_keyboard, day_keyboard, info_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привіт.\n"
        "Я Тихий.\n"
        "Не люблю говорити зайве.\n"
        "Але можу допомогти.\n\n"
        "Обери, що тебе цікавить:"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard)

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Обери, що тебе цікавить:"
    await update.message.reply_text(text, reply_markup=main_keyboard)

async def book_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Добре. Тобі потрібна тиша.\n"
        "Обери день:"
    )
    await update.message.reply_text(text, reply_markup=day_keyboard)

async def what_is_it(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Це маленька кімната,\n"
        "де можна бути наодинці з тишею.\n\n"
        "Вона — як сусід, який не лізе в душу.\n\n"
        "Тут можна:\n"
        "— попрацювати\n"
        "— подихати\n"
        "— зникнути на годинку"
    )
    await update.message.reply_text(text, reply_markup=info_keyboard)

async def just_silence(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Поважаю.\nЯкщо передумаєш — я поруч. Але мовчки."
    )

async def payment_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Тиша коштує:\n"
        "— 1 година: ___ грн\n"
        "— 2 години: ___ грн\n\n"
        "Оплатити можна після бронювання.\n"
        "(1234 5678 9012 3456)"
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("💳 Оплата моно банк", url="https://send.monobank.ua/jar/ABCD12345678")
    ]])

    await update.message.reply_text(text, reply_markup=keyboard)

async def location_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Тихий живе тут: Google Maps Link\n"
        "📍 [вул. Тиша, 7](https://maps.app.goo.gl/C3o6DNQj6cjNQsZB9)\n"
        "Якщо не знайдеш — просто постій. Він сам знайде тебе."
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=main_keyboard)