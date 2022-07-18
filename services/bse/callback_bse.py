from .bse import (
    checkBse, bseMessage, # methods
) 
from components.logger import logger
from components.action import send_typing_action
from telegram import ParseMode


def bseCallback(update, context):
    data = update.callback_query.data
    func_code = int(data.split()[1])
    if func_code == 0 : 
        logger.info('func_code = 0')
        bseNameCallback(update, context)
    elif func_code == 1 : 
        logger.info('func_code = 1')
        bseBestCallback(update, context)
    elif func_code == 2 : 
        logger.info('func_code = 2')
        bseWorstCallback(update, context)


@send_typing_action
def bseNameCallback(update, context):
    query = update.callback_query
    data = query.data.split()[0]
    temp_bse = checkBse()
    if temp_bse:
        code = data.lower()
        quote = temp_bse.getQuote(code)
        text = bseMessage(quote)
    query.edit_message_text(text=text)


@send_typing_action
def bseBestCallback(update, context): 
    query = update.callback_query
    data = int(query.data.split()[0])
    temp_bse = checkBse()
    from services.bse.bse import bse_top_gainers
    if not bse_top_gainers:
        bse_top_gainers = temp_bse.topGainers()
    if bse_top_gainers:
        lastPrice = bse_top_gainers[data]['LTP']
        securityID = bse_top_gainers[data]['securityID']
        scripCode = bse_top_gainers[data]['scripCode']
        pChange = bse_top_gainers[data]['pChange']
        change = bse_top_gainers[data]['change']
        text = \
f"""
scripCode: `{scripCode}`
securityID: {securityID}
lastPrice: {lastPrice}
change: {change}
%change: {pChange}"""

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)


@send_typing_action
def bseWorstCallback(update, context):
    global bse_top_losers, nse_fetch 
    query = update.callback_query
    data = int(query.data.split()[0])
    temp_bse = checkBse()
    from services.bse.bse import bse_top_losers
    if not bse_top_losers:
        bse_top_losers = temp_bse.topLosers()
    if bse_top_losers:
        lastPrice = bse_top_losers[data]['LTP']
        securityID = bse_top_losers[data]['securityID']
        scripCode = bse_top_losers[data]['scripCode']
        pChange = bse_top_losers[data]['pChange']
        change = bse_top_losers[data]['change']
        text = \
f"""
scripCode: `{scripCode}`
securityID: {securityID}
lastPrice: {lastPrice}
change: {change}
%change: {pChange}"""

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
