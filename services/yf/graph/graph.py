from components.logger import logger
from components.action import send_typing_action
from .generator import graph


@send_typing_action
def gfCode(update, context):
    try:
        args = context.args[0]
        code = args.upper()
        period = context.args[1].lower()
        img = graph(code, period)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img,'rb'))
    except Exception as e:
        text = "some error at gfCode"
        logger.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
