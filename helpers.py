from telegram import Update
from telegram.ext import ContextTypes
from config import ALLOWED_USER_IDS

# Function to check if user is allowed
def is_user_allowed(user_id: int) -> bool:
    # If no allowed user IDs are specified, allow all users
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
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