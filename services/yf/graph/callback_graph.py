from components.logger import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from components.action import send_typing_action
from .generator import graph
ticker_code = None

def graphCallback(update, context):
    global ticker_code
    logger.info('in graphCallback')
    data = update.callback_query.data
    func_code = int(data.split()[1])
    if func_code == 0 : 
        logger.info('func_code = 0')
        ticker_code = data.split()[0]
        graphPeriod(update, context)
    elif func_code == 1 : 
        logger.info('func_code = 1')
        graphGenCallback(update, context)

@send_typing_action
def graphPeriod(update, context):
    logger.info('in graphPeriod')
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("1 month",callback_data= "1m 1 gf")],
        [InlineKeyboardButton("1 year",callback_data= "1y 1 gf")],
        [InlineKeyboardButton("5 year",callback_data= "5y 1 gf")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.delete()
    # query.edit_message_text("Choose duration: ", reply_markup= reply_markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose duration", reply_markup= reply_markup)

    
@send_typing_action
def graphGenCallback(update, context):
    logger.info('in graphGenCallback')
    query = update.callback_query
    data = query.data.split()[0]
    img = graph(ticker_code, data)
    query.message.delete()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img,'rb'))
    