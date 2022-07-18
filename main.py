from telegram.ext import Updater
from components.config import TOKEN, WEBHOOK
from components.handler import handler
import os
import sys


PORT = int(os.environ.get('PORT', '8443'))

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    handler(dispatcher)
    
    if len(sys.argv) > 1 and sys.argv[1] == '-p':
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN,
                              webhook_url=WEBHOOK)
    else:
        updater.start_polling()
    updater.idle()


