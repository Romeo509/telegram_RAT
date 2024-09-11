import pyautogui
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def mouse_control(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Move Left", callback_data='move_left')],
        [InlineKeyboardButton("Move Right", callback_data='move_right')],
        [InlineKeyboardButton("Move Up", callback_data='move_up')],
        [InlineKeyboardButton("Move Down", callback_data='move_down')],
        [InlineKeyboardButton("Click", callback_data='click')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose an action:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    
    await query.answer()
    
    if data == 'move_left':
        pyautogui.move(-100, 0)
    elif data == 'move_right':
        pyautogui.move(100, 0)
    elif data == 'move_up':
        pyautogui.move(0, -100)
    elif data == 'move_down':
        pyautogui.move(0, 100)
    elif data == 'click':
        pyautogui.click()
    else:
        await query.message.reply_text("Unknown action.")
