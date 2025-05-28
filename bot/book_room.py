from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from datetime import datetime, timedelta
import constants as C
from booking_storage import mark_slot_as_booked, is_slot_available

# Step 1: Day choice
async def book_room(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Сьогодні", callback_data="book:today"),
         InlineKeyboardButton("Завтра", callback_data="book:tomorrow")],
        [InlineKeyboardButton("Інша дата", callback_data="book:other")]
    ])
    await update.message.reply_text("Добре. Тобі потрібна тиша.\nОбери день:", reply_markup=keyboard)

# Step 2: Handle day selection
async def handle_booking_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "book:today":
        date = datetime.now().strftime("%m-%d")
        await show_time_slots(query, date)
    elif query.data == "book:tomorrow":
        date = (datetime.now() + timedelta(days=1)).strftime("%m-%d")
        await show_time_slots(query, date)
    elif query.data == "book:other":
        buttons = []
        for i in range(6):  # з сьогодні
            day = datetime.now() + timedelta(days=i)
            day_num = day.day
            month_name = C.UKR_MONTHS[day.month]
            label = f"{day_num} {month_name}"
            callback = f"bookdate:{day.strftime('%m-%d')}"
            buttons.append([InlineKeyboardButton(label, callback_data=callback)])
        await query.edit_message_text("Оберіть дату:", reply_markup=InlineKeyboardMarkup(buttons))
    elif query.data.startswith("bookdate:"):
        date = query.data.split(":")[1]
        await show_time_slots(query, date)
    elif query.data.startswith("booktime:"):
        parts = query.data.split(":", 2)
        if len(parts) == 3:
            _, datetime_str = parts[0], parts[1] + ":" + parts[2]  # "05-29T09:00"
            if "T" in datetime_str:
                date, time = datetime_str.split("T")

                user_id = query.from_user.id
                username = query.from_user.username

                mark_slot_as_booked(date, time, user_id, username)

                await query.edit_message_text(
                    f"Готово.\nТиша тебе чекатиме {date} о {time}.\n"
                    "Якщо щось зміниться — скажи мені. Але краще не метушитися."
                )
    else:
        await query.edit_message_text("Помилка: невірний формат callback_data.")

# Step 3: Show time slots
def chunk_buttons(buttons, n):
    return [buttons[i:i + n] for i in range(0, len(buttons), n)]

async def show_time_slots(query, date_str):
    times = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00",
             "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"]

    now = datetime.now()
    today_str = now.strftime("%m-%d")

    all_buttons = []

    for t in times:
        # перевіряємо, чи слот вже зайнятий
        if not is_slot_available(date_str, t):
            continue

        # перевіряємо чи це сьогодні
        if date_str == today_str:
            month, day = map(int, date_str.split("-"))
            hour, minute = map(int, t.split(":"))
            slot_time = datetime(now.year, month, day, hour, minute)

            # якщо час вже минув або менше ніж через годину
            if slot_time <= now or slot_time - now < timedelta(hours=1):
                continue

        all_buttons.append(InlineKeyboardButton(t, callback_data=f"booktime:{date_str}T{t}"))

    if all_buttons:
        keyboard = chunk_buttons(all_buttons, 4)
        await query.edit_message_text(
            f"Оберіть час для {date_str}:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.edit_message_text(
            f"На {date_str} більше немає вільного часу 🪷\n"
            "Оберіть іншу дату, будь ласка."
        )