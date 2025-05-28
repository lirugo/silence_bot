import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers import what_is_it, just_silence, back_to_main, start, payment_info, location_info
from book_room import book_room, handle_booking_callback
from datetime import datetime
import constants as C

def main():
    token = os.getenv("SILENCE_BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN environment variable is not set")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^{C.BTN_BOOK}$'), book_room))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^{C.BTN_WHAT_IS}$'), what_is_it))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^{C.BTN_MAIN_MENU}$'), back_to_main))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^{C.BTN_NOTHING}$'), just_silence))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^{C.BTN_PAYMENT}$'), payment_info))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f'^{C.BTN_LOCATION}$'), location_info))

    app.add_handler(CallbackQueryHandler(handle_booking_callback, pattern="^book"))

    print(f"🤖 Silence bot is running... [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

    app.run_polling()

if __name__ == "__main__":
    main()
