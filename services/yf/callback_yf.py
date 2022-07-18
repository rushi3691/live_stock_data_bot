from telegram import replymarkup
from .yf import (
    yfmessage
)

from components.action import send_typing_action
from components.logger import logger
import yfinance as yf 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

@send_typing_action
def yfCallback(update, context):
    query = update.callback_query
    data = query.data.split()[0]
    logger.info(data)
    quote = yf.Ticker(data).info
    text = yfmessage(quote)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Show Graph", callback_data = f"{data} 0 gf")]])
    query.message.edit_text(text, reply_markup= reply_markup)