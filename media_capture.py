import cv2
import tempfile
import os
import pyautogui
from telegram import Update
from telegram.ext import ContextTypes
from config import WEBCAM_DEVICE_INDEX, ALLOWED_USER_IDS

# Function to check if user is allowed
def is_user_allowed(user_id: int) -> bool:
    # If no allowed user IDs are specified, allow all users
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS

async def take_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
    cap = cv2.VideoCapture(WEBCAM_DEVICE_INDEX)

    if not cap.isOpened():
        await update.message.reply_text("Failed to open webcam.")
        return
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        await update.message.reply_text("Failed to capture image.")
        return
    
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    cv2.imwrite(temp_file_path, frame)
    await update.message.reply_photo(photo=open(temp_file_path, 'rb'))
    os.remove(temp_file_path)

async def take_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if not is_user_allowed(user_id):
        await update.message.reply_text("You are not authorized to use this bot.")
        return
        
    screenshot = pyautogui.screenshot()
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        temp_file_path = temp_file.name
    
    screenshot.save(temp_file_path)
    await update.message.reply_photo(photo=open(temp_file_path, 'rb'))
    os.remove(temp_file_path)