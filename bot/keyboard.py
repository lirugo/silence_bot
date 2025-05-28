from telegram import ReplyKeyboardMarkup
import constants as C

main_keyboard = ReplyKeyboardMarkup([
    [C.BTN_BOOK, C.BTN_PAYMENT],
    [C.BTN_LOCATION, C.BTN_WHAT_IS],
    [C.BTN_NOTHING]
], resize_keyboard=True)

day_keyboard = ReplyKeyboardMarkup([
    [C.BTN_TODAY, C.BTN_TOMORROW],
    [C.BTN_OTHER],
    [C.BTN_MAIN_MENU]
], resize_keyboard=True, one_time_keyboard=True)

info_keyboard = ReplyKeyboardMarkup([
    # [C.BTN_HOW_LOOKS],
    # [C.BTN_REVIEWS],
    # [C.BTN_TRY],
    [C.BTN_MAIN_MENU]
], resize_keyboard=True, one_time_keyboard=True)