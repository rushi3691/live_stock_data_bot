from .config import *
from .logger import logger
from services.nse.nse import (
    nseCode, nseName, 
)
from services.yf.yf import (
    yfName, yfCode
)

from telegram import ParseMode

from services.bse.bse import (
    bseName, bseCode
)
from .action import send_typing_action
from telegram import Update
from telegram.ext import CallbackContext

@send_typing_action
def start(update: Update,context: CallbackContext):
    global DB
    chat_id = update.message.chat_id
    DB[chat_id] = 'yfinance'
    logger.info(f"new user: {chat_id}")

    start_text = \
f"""
Welcome to stock-bot
use `/help` for basic help
use `/help service` for service related help """

    context.bot.send_message(chat_id=update.effective_chat.id,text= start_text, parse_mode=ParseMode.MARKDOWN)

@send_typing_action
def set_to(update,context):
    global SERVICES,CURR_SERVICE, DB
    chat_id = update.message.chat_id
    try:
        args = context.args[0]
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "pass argument")
        return 
    service = args.lower()
    if service in SERVICES and SERVICES[service]:
        # CURR_SERVICE = service
        DB[chat_id] = service
        text = f"""set to {args}\nuse /help {args} for help"""
    else:
        text = f"service not found or service not active"
    context.bot.send_message(chat_id=update.effective_chat.id,text=text)



def searchName(update,context):
    global DB 
    chat_id = update.message.chat_id
    if not chat_id in DB:
        DB[chat_id] = 'yfinance'
        logger.info(f"new user: {chat_id}")

    if DB[chat_id] == 'nse':
        nseName(update, context)
    elif DB[chat_id] == 'bse':
        bseName(update, context) 
    elif DB[chat_id] == 'yfinance':
        yfName(update, context)

def searchCode(update, context):
    global DB 
    chat_id = update.message.chat_id
    if not chat_id in DB:
        DB[chat_id] = 'yfinance'
        logger.info(f"new user: {chat_id}")

    if DB[chat_id] == 'nse':
        nseCode(update, context)
    elif DB[chat_id] == 'bse':
        bseCode(update, context)
    elif DB[chat_id] == 'yfinance':
        yfCode(update, context)

@send_typing_action
def currService(update, context):
    global DB 
    chat_id = update.message.chat_id
    if not chat_id in DB:
        DB[chat_id] = 'yfinance'
        logger.info(f"new user: {chat_id}")

    text=DB[chat_id]
    context.bot.send_message(chat_id=update.effective_chat.id,text=text)

@send_typing_action
def help(update, context):
    args = context.args
    text_help = None
    if args:
        if args[0].lower() == 'nse':
            text_help = \
f"""
use `/set nse` to set current ervice to NSE
use `/nsebest` for best performing stocks
            \(service must be set to NSE\)
use `/nseworst` for worst performing stocks
            \(service must be set to NSE\)"""
        elif args[0].lower() == 'bse':
            text_help = \
f"""
use `/set bse` to set current service to BSE
use `/bsebest` for best performing stocks
            \(service must be set to BSE\)
use `/bseworst` for worst performing stocks
            \(service must be set to BSE\)"""

        elif args[0].lower() == 'yf':
            text_help = \
f"""
use `/set yf` to set current service to NASDAQ"""
        else:
            text_help = \
f"""
{args} not found"""
        context.bot.send_message(chat_id=update.effective_chat.id,text= text_help, parse_mode= ParseMode.MARKDOWN_V2 )
    else:
        text_help = \
f"""
use `/searchCode code` to get info
use `/searchName name` to search stocks
use `/set service` to set default service
availabe services are
nse : for NSE
bse : for BSE
yfinance : for NASDAQ
default service is yfinance for NASDAQ
fuse `/help service` for service related help"""
        context.bot.send_message(chat_id=update.effective_chat.id,text= text_help, parse_mode=ParseMode.MARKDOWN)

@send_typing_action
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

@send_typing_action
def service_down(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Can't process your command..\nService is down!")
