import sys
from telegram import Update , Bot
from telegram.ext import (
    Updater,
    ShippingQueryHandler,
    PreCheckoutQueryHandler,
    CommandHandler,
    CallbackContext,
    Filters
    )

from telegram_ecommerce.database.db_wrapper import db
from telegram_ecommerce.utils.consts import credentials
from telegram_ecommerce.utils.log import logger
from telegram_ecommerce.handlers import (
    all_public_commands_descriptions, 
    all_handlers)


token = credentials["token"]
admins = credentials["admins_username"]

##########################
# def restart(update: Update, context: CallbackContext):
#     """Handler function for the /restart command"""
#     update.message.reply_text("Restarting...")
#     # Stop the updater
#     context.bot.stop()
#     # Restart the script
#     import os
#     os.execl(sys.executable, sys.executable, *sys.argv)
####################

def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.bot.set_my_commands( commands=all_public_commands_descriptions)

    # dp.add_handler(CommandHandler("restart", restart))
    for handler in all_handlers:
        dp.add_handler(handler)
    logger.info("bot started")
    # def restart(update: Update, context: CallbackContext):
    #     chat_id = update.effective_chat.id
    #     if str(chat_id) not in admins:
    #         update.message.reply_text(
    #             "You are not authorized to restart the bot!")
    #         return

    #     update.message.reply_text("Restarting the bot...")
    #     updater.stop()

    # dp.add_handler(CommandHandler("restart", restart))
    updater.start_polling()
    
    updater.idle()
    db.close()
    logger.info("bot closed")


if __name__ == '__main__':
    main()


