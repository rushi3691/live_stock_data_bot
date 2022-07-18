from .nse import (
    checkNse, nseMessage, # methods
) 
from components.logger import logger
from components.action import send_typing_action
from telegram import ParseMode


def nseCallback(update, context):
    data = update.callback_query.data
    func_code = int(data.split()[1])
    if func_code == 0 : 
        logger.info('func_code = 0')
        nseNameCallback(update, context)
    elif func_code == 1 : 
        logger.info('func_code = 1')
        nseBestCallback(update, context)
    elif func_code == 2 : 
        logger.info('func_code = 2')
        nseWorstCallback(update, context)

@send_typing_action
def nseNameCallback(update, context):
    query = update.callback_query
    data = query.data.split()[0]
    temp_nse = checkNse()
    if temp_nse:
        code = data.lower()
        logger.info(f"nse name callback - code: {code}")
        quote = temp_nse.get_quote(code)
        text = nseMessage(quote)
    query.edit_message_text(text=text)

@send_typing_action
def nseBestCallback(update, context): 
    query = update.callback_query
    data = int(query.data.split()[0])
    temp_nse = checkNse()
    from services.nse.nse import top_gainers
    if not top_gainers:
        top_gainers = temp_nse.get_top_gainers()
    if top_gainers:
        highPrice = top_gainers[data]['highPrice']
        lowPrice = top_gainers[data]['lowPrice']
        lastPrice = top_gainers[data]['ltp']
        symbol = top_gainers[data]['symbol']
        text = \
f"""
stockSymbol: `{symbol}`
lastPrice: {lastPrice}
highPrice: {highPrice}
lowPrice: {lowPrice}"""

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)


@send_typing_action
def nseWorstCallback(update, context):
    global top_losers, nse_fetch 
    query = update.callback_query
    data = int(query.data.split()[0])
    temp_nse = checkNse()
    from services.nse.nse import top_losers
    if not top_losers:
        top_losers = temp_nse.get_top_losers()
    if top_losers:
        highPrice = top_losers[data]['highPrice']
        lowPrice = top_losers[data]['lowPrice']
        lastPrice = top_losers[data]['ltp']
        symbol = top_losers[data]['symbol']
        text = \
f"""
stockSymbol: `{symbol}`
lastPrice: {lastPrice}
highPrice: {highPrice}
lowPrice: {lowPrice}"""

    query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
