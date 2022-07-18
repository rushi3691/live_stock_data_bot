from typing import Union
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from components.logger import logger
from components.action import send_typing_action
import pandas as pd

from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table
import yfinance as yf 


tickers = pd.DataFrame() 


callback_codes = {
    '0': ['yfname'], 
}


def allCodes():
    global tickers
    if tickers.empty :
        tickers = tickers_nasdaq(True)
        data = json.dumps(dict(zip(tickers['Symbol'], tickers['Security Name'])), indent= 4)
        with open('services/yf/stock_codes.json','w') as file:
                file.write(data)
        
def checkName(code: str) -> dict :
    names = {}
    with open('services/yf/stock_codes.json','r') as file:
        code_file=json.load(file)
        for i in code_file:
            if code.lower() in str(code_file[i]).lower():
                names[i] = code_file[i]

    return names

def yfButtons(obj: Union[dict, list], func_code: str, helpText: str = None ) -> InlineKeyboardMarkup:
    keyboard = []
    #checking if obj is dict or list
    if isinstance(obj,dict):
        for i in obj:
            callback_data = f"{i} {func_code} yf"
            keyboard.append([InlineKeyboardButton(obj[i], callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

@send_typing_action
def yfName(update, context):
    global tickers
    allCodes()
    args = ' '.join(context.args)
    if not tickers.empty:
        names = checkName(args)
        if names:
            reply_markup = yfButtons(names, 0)
            update.message.reply_text('Search results:', reply_markup=reply_markup)
        else:
            text = f"{args} not found"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@send_typing_action
def yfCode(update, context):
    try:
        args = context.args[0]
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "pass argument")
        return
    code = args.upper()
    quote = yf.Ticker(code).info
    text_to_send = yfmessage(quote, args)
    if quote:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Show Graph", callback_data = f"{code} 0 gf")]])
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send, reply_markup= reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)




def yfmessage(quote: dict, args: str = None) -> str :
    if quote:
        if len(quote)== 1 :
            data = f"""{args} not found"""
        else:
            data = \
f"""
Company: {quote['shortName']}
lastPrice: {quote['regularMarketPrice']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""

    return data
