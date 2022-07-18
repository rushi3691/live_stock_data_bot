
TOKEN = 'ADD_BOT_TOKEN'
APP_NAME = "ADD_HEROKU_APP_NAME"
WEBHOOK = f"https://{APP_NAME}.herokuapp.com/{TOKEN}"

SERVICES = {
    'yfinance':1,
    'nse':0,
    'bse':1,
}

CURR_SERVICE = 'yfinance'
DB = {}