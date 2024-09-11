from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Here are the available commands:\n"
        "/start - Welcome message\n"
        "/clients - List active clients\n"
        "/register <device_name> - Register a device\n"
        "/exec <command> - Execute a shell command\n"
        "/mouse - Control the mouse\n"
        "/photo - Take a photo using the webcam\n"
        "/screenshot - Take a screenshot\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(help_text)
