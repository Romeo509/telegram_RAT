# Telegram Remote Control Bot

This project allows users to remotely control a device via a Telegram bot. Features include taking screenshots, using the webcam to take photos, controlling the mouse, and executing shell commands.

## Features

- **/start** - Display a welcome message.
- **/clients** - View all registered devices connected to the bot.
- **/register `<device_name>`** - Register a device with a name.
- **/exec `<command>`** - Execute a shell command on the device.
- **/mouse** - Control the mouse remotely.
- **/photo** - Take a photo using the device's webcam.
- **/screenshot** - Capture and send a screenshot from the device.
- **/help** - View a list of available commands.

## Installation and Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. Install the required dependencies using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your bot token:

   - Open the `config.py` file.
   - Replace the `'YOUR_TELEGRAM_BOT_TOKEN'` with the actual token from your bot, which you can get by creating a bot through [BotFather](https://core.telegram.org/bots#botfather).

    ```python
    # config.py
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    ```

4. Run the bot:
    ```bash
    python main.py
    ```

## Usage

1. **Register a device:**
    ```
    /register <device_name>
    ```

   Register your current device with a name. This device will now be listed under active clients.

2. **List active devices:**
    ```
    /clients
    ```

   Lists all devices registered with the bot.

3. **Control the mouse:**
    ```
    /mouse
    ```

   Opens an interactive menu to move the mouse or perform a click remotely.

4. **Take a photo using the webcam:**
    ```
    /photo
    ```

   Takes a snapshot from the webcam and sends it back to the Telegram chat.

5. **Capture a screenshot:**
    ```
    /screenshot
    ```

   Takes a screenshot of the current screen and sends it to the Telegram chat.

6. **Execute a shell command:**
    ```
    /exec <command>
    ```

   Executes the provided command on the device and sends the output (or any errors) to the Telegram chat.

## Requirements

- Python 3.x
- Libraries (installed via `requirements.txt`):
    - python-telegram-bot
    - pyautogui
    - opencv-python

