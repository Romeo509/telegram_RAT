import socket
from telegram import Update
from telegram.ext import ContextTypes
from typing import Dict

# Dictionary to keep track of active clients
active_clients: Dict[str, str] = {}

# Function to get the device name (hostname)
def get_device_name() -> str:
    return socket.gethostname()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Use /clients to see active devices.")

async def clients(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not active_clients:
        await update.message.reply_text("No active clients.")
        return
    
    message = "Active clients:\n" + "\n".join(f"{device}: {user_id}" for user_id, device in active_clients.items())
    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.startswith('/register'):
        user_id = str(update.effective_user.id)
        device_name = ' '.join(update.message.text.split()[1:]) if len(update.message.text.split()) > 1 else 'Unknown Device'
        active_clients[user_id] = device_name
        await update.message.reply_text(f"Device registered as {device_name}")
    
def register_bot_device() -> None:
    bot_device_name = get_device_name()
    active_clients['bot'] = bot_device_name
