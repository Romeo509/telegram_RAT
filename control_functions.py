import pyautogui
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from config import MOUSE_MOVE_DISTANCE, ALLOWED_USER_IDS

# Function to check if user is allowed
def is_user_allowed(user_id: int) -> bool:
    # If no allowed user IDs are specified, allow all users
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS

async def mouse_control(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
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
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.callback_query.answer("You are not authorized to use this bot.")
        return
        
    query = update.callback_query
    data = query.data
    
    await query.answer()
    
    if data == 'move_left':
        pyautogui.move(-MOUSE_MOVE_DISTANCE, 0)
    elif data == 'move_right':
        pyautogui.move(MOUSE_MOVE_DISTANCE, 0)
    elif data == 'move_up':
        pyautogui.move(0, -MOUSE_MOVE_DISTANCE)
    elif data == 'move_down':
        pyautogui.move(0, MOUSE_MOVE_DISTANCE)
    elif data == 'click':
        pyautogui.click()
    else:
        await query.message.reply_text("Unknown action.")