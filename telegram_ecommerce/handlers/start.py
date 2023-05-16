from telegram.ext import CommandHandler
from telegram_ecommerce.utils.log import logger
from ..language import get_text


def start_callback(update, context):
    text = get_text("start", context)
    logger.info(f"User {update.effective_user.id} started the bot")
    logger.info("Start command received")
    
    update.message.reply_text(text)


start = CommandHandler("start", start_callback)


