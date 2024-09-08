from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from typing import Dict
import socket
import subprocess

# Your bot token
TOKEN = 'INSERT BOT TOKKEN HERE'

# Dictionary to keep track of active clients
active_clients: Dict[str, str] = {}  # {user_id: device_name}

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
    elif update.message.text.startswith('/exec'):
        # The command execution will be handled separately
        pass
    else:
        await update.message.reply_text("Unknown command. Use /clients to see active devices.")

async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a command to execute.")
        return
    
    command = ' '.join(context.args)
    
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Send the command output back to the user
        if result.stdout:
            await update.message.reply_text(f"Output:\n{result.stdout}")
        if result.stderr:
            await update.message.reply_text(f"Error:\n{result.stderr}")
    
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def register_bot_device() -> None:
    bot_device_name = get_device_name()
    # Simulate a bot registering itself by adding its own entry to the active_clients dictionary
    # Using a dummy user_id 'bot' for the bot
    active_clients['bot'] = bot_device_name

def main() -> None:
    # Register the bot's own device information
    register_bot_device()

    # Create the application and add handlers
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clients", clients))
    application.add_handler(CommandHandler("exec", exec_command))  # Add handler for /exec command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
