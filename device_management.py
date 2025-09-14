import socket
from telegram import Update
from telegram.ext import ContextTypes
from typing import Dict
from config import ALLOWED_USER_IDS

# Dictionary to keep track of active clients
active_clients: Dict[str, str] = {}

# Function to get the device name (hostname)
def get_device_name() -> str:
    return socket.gethostname()

# Function to check if user is allowed
def is_user_allowed(user_id: int) -> bool:
    # If no allowed user IDs are specified, allow all users
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
    await update.message.reply_text("Welcome! Use /clients to see active devices.")

async def clients(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
    if not active_clients:
        await update.message.reply_text("No active clients.")
        return
    
    message = "Active clients:\n" + "\n".join(f"{device}: {user_id}" for user_id, device in active_clients.items())
    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        return  # Silently ignore messages from unauthorized users
        
    if update.message.text.startswith('/register'):
        device_name = ' '.join(update.message.text.split()[1:]) if len(update.message.text.split()) > 1 else 'Unknown Device'
        active_clients[str(user_id)] = device_name
        await update.message.reply_text(f"Device registered as {device_name}")
    
def register_bot_device() -> None:
    bot_device_name = get_device_name()
    active_clients['bot'] = bot_device_name