from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from components.commands import (
    start, set_to, searchName, currService, searchCode,
    help, unknown   #commands
)
from services.nse.nse import (
    nseBest, nseWorst
)
from services.nse.callback_nse import nseCallback
from services.bse.callback_bse import bseCallback
from services.yf.callback_yf import yfCallback
from services.bse.bse import (
    bseBest, bseWorst
)
from services.yf.graph.graph import gfCode
from services.yf.graph.callback_graph import graphCallback
from components.config import *
from components.logger import error
from components.commands import service_down

def handler(dispatcher):
    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('set',set_to))
    dispatcher.add_handler(CommandHandler('service',currService))
    dispatcher.add_handler(CommandHandler('name_search',searchName))
    dispatcher.add_handler(CommandHandler('code_search',searchCode))
    dispatcher.add_handler(CommandHandler('help',help))
    dispatcher.add_handler(CommandHandler('graph',gfCode))

    if SERVICES['nse']:
        dispatcher.add_handler(CommandHandler('nsebest',nseBest))
        dispatcher.add_handler(CommandHandler('nseworst',nseWorst))
        dispatcher.add_handler(CallbackQueryHandler(nseCallback, pattern=r"^.*nse$"))
    else:
        dispatcher.add_handler(CommandHandler('nsebest',service_down))
        dispatcher.add_handler(CommandHandler('nseworst',service_down))
    
    if SERVICES['bse']:
        dispatcher.add_handler(CommandHandler('bsebest',bseBest))
        dispatcher.add_handler(CommandHandler('bseworst',bseWorst))
        dispatcher.add_handler(CallbackQueryHandler(bseCallback, pattern=r"^.*bse$"))
    else:
        dispatcher.add_handler(CommandHandler('bsebest',service_down))
        dispatcher.add_handler(CommandHandler('bseworst',service_down))

    dispatcher.add_handler(CallbackQueryHandler(yfCallback, pattern= r"^.*yf$"))
    dispatcher.add_handler(CallbackQueryHandler(graphCallback, pattern = r"^.*gf$"))

    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    dispatcher.add_error_handler(error)
