import subprocess
from telegram import Update
from telegram.ext import ContextTypes
from config import COMMAND_TIMEOUT, ALLOWED_USER_IDS

# Function to check if user is allowed
def is_user_allowed(user_id: int) -> bool:
    # If no allowed user IDs are specified, allow all users
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS

async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a command to execute.")
        return
    
    command = ' '.join(context.args)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=COMMAND_TIMEOUT)
        
        if result.stdout:
            await update.message.reply_text(f"Output:\n{result.stdout}")
        if result.stderr:
            await update.message.reply_text(f"Error:\n{result.stderr}")
    
    except subprocess.TimeoutExpired:
        await update.message.reply_text(f"Command timed out after {COMMAND_TIMEOUT} seconds.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")