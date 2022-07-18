from components.logger import logger
from components.action import send_typing_action
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bsedata.bse import BSE
import json
from typing import Union, Tuple
from .utils import GetScripCodes, UpdateScripCodes


bse_fetch = None
bse_top_gainers = None
bse_top_losers = None 

bse_codes_flag = False

callback_codes = {
    '0': ['bseName'], 
    '1': ['bse_top_gainers'], 
    '2': ['bse_top_losers'],
}

# checks if nse exists or not and 
# if it doesn't then creates nse
def checkBse():
    global bse_fetch, bse_codes_flag
    if not bse_fetch:
        bse_fetch = BSE(update_codes = False)
    if bse_codes_flag == False:
        # allCodes()
        UpdateScripCodes()
        bse_codes_flag = True
    return bse_fetch 

# writes all codes to stock_codes.json 
def allCodes():
    all_stock_codes = bse_fetch.getScripCodes()  
    stock_codes = json.dumps(all_stock_codes, indent=4)
    with open('services/bse/stock_codes.json', 'w') as file:
        file.write(stock_codes)


# check if search query is in the file 
def checkName(code: str) -> Tuple[dict, str]:
    names = {}
    with open('services/bse/stk.json','r') as file:
        code_file=json.load(file)
        for i in code_file:
            if code.lower() in code_file[i].lower():
                names[i] = code_file[i]

    return names 


# universal function to create buttons 
# text is for replacing 'symbol'
def bseButtons(obj: Union[dict, list], func_code: str, helpText: str = None ) -> InlineKeyboardMarkup:
    keyboard = []
    #checking if obj is dict or list
    if isinstance(obj,dict):
        for i in obj:
            callback_data = f"{i} {func_code} bse"
            keyboard.append([InlineKeyboardButton(obj[i], callback_data=callback_data)])
    else:
        for i in enumerate(obj):
            callback_data = f"{i[0]} {func_code} bse"
            keyboard.append([InlineKeyboardButton(i[1]['securityID'], callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

@send_typing_action
def bseName(update, context):
    global bse_fetch
    checkBse()
    args = ' '.join(context.args)
    if bse_fetch:
        names = checkName(args)
        if names:
            reply_markup = bseButtons(names, 0)
            update.message.reply_text('Search results:', reply_markup=reply_markup)
        else:
            text = f"{args} not found"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@send_typing_action
def bseCode(update, context):
    global bse_fetch
    checkBse()
    try:
        args = context.args[0]
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "pass argument")
        return
    if bse_fetch:
        code = args.lower()
        try:
            quote = bse_fetch.getQuote(code)
        except IndexError:
            quote = None  
        text = bseMessage(quote, args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def bseMessage(quote: str, args: str = None) -> str :
    if quote:
        data = \
f"""
companyName: {quote['companyName']}
currentValue: {quote['currentValue']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""
    else:
        data = f"""{args} not found"""
    return data

@send_typing_action
def bseBest(update, context):
    global bse_fetch, bse_top_gainers
    checkBse()
    if bse_fetch:
        bse_top_gainers = bse_fetch.topGainers()
        reply_markup = bseButtons(bse_top_gainers, 1)
        update.message.reply_text('Top Gainers:', reply_markup=reply_markup)

@send_typing_action
def bseWorst(update, context):
    global bse_fetch, bse_top_losers
    checkBse()
    if bse_fetch:
        bse_top_losers = bse_fetch.topLosers()
        reply_markup = bseButtons(bse_top_losers, 2)
        update.message.reply_text('Top Losers:', reply_markup=reply_markup)
