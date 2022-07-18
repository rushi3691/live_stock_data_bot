from components.logger import logger
from components.action import send_typing_action
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from nsetools import Nse
import json
from typing import Union, Tuple

nse_fetch = None
top_gainers = None
top_losers = None 

nse_codes_flag = False

callback_codes = {
    '0': ['nseName'], 
    '1': ['top_gainers'], 
    '2': ['top_losers'],
}

# checks if nse exists or not and 
# if it doesn't then creates nse
# done
def checkNse():
    global nse_fetch, nse_codes_flag
    if not nse_fetch:
        nse_fetch = Nse()
    if nse_codes_flag == False:
        allCodes()
        nse_codes_flag = True
    return nse_fetch 

# writes all codes to stock_codes.json 
# done
def allCodes():
    all_stock_codes = nse_fetch.get_stock_codes()
    stock_codes = json.dumps(all_stock_codes, indent=4)
    with open('services/nse/stock_codes.json', 'w') as file:
        file.write(stock_codes)


# check if search query is in the file 
# done
def checkName(code: str) -> Tuple[dict, str]:
    names = {}
    with open('services/nse/stock_codes.json','r') as file:
        code_file=json.load(file)
        for i in code_file:
            if code.lower() in code_file[i].lower():
                names[i] = code_file[i]

    return names


# universal function to create buttons 
# text is for replacing 'symbol'
# done
def nseButtons(obj: Union[dict, list], func_code: str, helpText: str = None ) -> InlineKeyboardMarkup:
    keyboard = []
    #checking if obj is dict or list
    if isinstance(obj,dict):
        for i in obj:
            callback_data = f"{i} {func_code} nse"
            keyboard.append([InlineKeyboardButton(obj[i], callback_data=callback_data)])
    else:
        for i in enumerate(obj):
            callback_data = f"{i[0]} {func_code} nse"
            keyboard.append([InlineKeyboardButton(i[1]['symbol'], callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


@send_typing_action
def nseName(update, context):
    global nse_fetch
    checkNse()
    args = ' '.join(context.args)
    if nse_fetch:
        names = checkName(args)
        if names:
            reply_markup = nseButtons(names, 0)
            update.message.reply_text('Search results:', reply_markup=reply_markup)
        else:
            text = f"{args} not found"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

@send_typing_action
def nseCode(update, context):
    global nse_fetch
    checkNse()
    try:
        args = context.args[0]
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "pass argument")
        return
    if nse_fetch:
        code = args.lower()
        quote = nse_fetch.get_quote(code)
        text = nseMessage(quote, args)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def nseMessage(quote: str, args: str = None) -> str :
    if quote:
        data = \
f"""
companyName: {quote['companyName']}
lastPrice: {quote['lastPrice']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""
    else:
        data = f"""{args} not found"""
    return data

@send_typing_action
def nseBest(update, context):
    global nse_fetch, top_gainers
    checkNse()
    if nse_fetch:
        top_gainers = nse_fetch.get_top_gainers()
        reply_markup = nseButtons(top_gainers, 1)
        update.message.reply_text('Top Gainers:', reply_markup=reply_markup)

@send_typing_action
def nseWorst(update, context):
    global nse_fetch, top_losers
    checkNse()
    if nse_fetch:
        top_losers = nse_fetch.get_top_losers()
        reply_markup = nseButtons(top_losers, 2)
        update.message.reply_text('Top Losers:', reply_markup=reply_markup)
