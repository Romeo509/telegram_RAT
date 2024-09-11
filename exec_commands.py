import subprocess
from telegram import Update
from telegram.ext import ContextTypes

async def exec_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a command to execute.")
        return
    
    command = ' '.join(context.args)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            await update.message.reply_text(f"Output:\n{result.stdout}")
        if result.stderr:
            await update.message.reply_text(f"Error:\n{result.stderr}")
    
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
