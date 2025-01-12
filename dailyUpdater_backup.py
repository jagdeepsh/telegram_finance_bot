# Imports Dependency is on conda activate telebot,
# currently it is set to 3.12.4 of the version of Python
from typing import Final, List, Dict, Optional
import yfinance as yf
from telegram import (
    Update, 
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove
    )
from telegram.ext import (
    Application, 
    ContextTypes, 
    MessageHandler, 
    CommandHandler, 
    filters, 
    ConversationHandler
    )
import datetime
import time
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()

# Variables
TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final = os.getenv('BOT_USERNAME')

TICKER, INFO, FREQ, TIME, DAY, PRICE = range(6)
update_freq: str = ''
update_time: datetime
update_info: str = ''
update_day: int = 0
chat_id: str = ''
alert_stock: List[str] = ['']
alert_price: List[float] = [0]
alert_info: str = ''
alert_freq: int = 0
is_alert_repeat: bool = False
is_default_repeat: bool = True
is_custom_repeat: bool = True
tickers: List[str] = ['']
ticker_methods: List[List[str]] = [['address1'], ['city'], ['state'], ['zip'], 
 ['country'], ['phone'], ['website'], 
 ['industry'], ['industryKey'], 
 ['industryDisp'], ['sector'], ['sectorKey'], 
 ['sectorDisp'], 
 ['fullTimeEmployees'],  
 ['auditRisk'], ['boardRisk'], ['compensationRisk'], ['shareHolderRightsRisk'], 
['overallRisk'], ['governanceEpochDate'], ['compensationAsOfEpochDate'], 
['irWebsite'], 
['previousClose'], ['open'], ['dayLow'], ['dayHigh'], 
['regularMarketPreviousClose'], ['regularMarketOpen'], 
['regularMarketDayLow'], ['regularMarketDayHigh'], ['dividendRate'], 
['dividendYield'], ['exDividendDate'], ['payoutRatio'], 
['fiveYearAvgDividendYield'], ['beta'], ['trailingPE'], ['forwardPE'], 
['volume'], ['regularMarketVolume'], ['averageVolume'], 
['averageVolume10days'], ['averageDailyVolume10Day'], ['bid'], 
['ask'], ['bidSize'], ['askSize'], ['marketCap'], 
['fiftyTwoWeekLow'], ['fiftyTwoWeekHigh'], ['priceToSalesTrailing12Months'], 
['fiftyDayAverage'], ['twoHundredDayAverage'], 
['trailingAnnualDividendRate'], ['trailingAnnualDividendYield'], 
['currency'], ['enterpriseValue'], ['profitMargins'], 
['floatShares'], ['sharesOutstanding'], ['sharesShort'], 
['sharesShortPriorMonth'], ['sharesShortPreviousMonthDate'], 
['dateShortInterest'], ['sharesPercentSharesOut'], 
['heldPercentInsiders'], ['heldPercentInstitutions'], 
['shortRatio'], ['shortPercentOfFloat'], ['impliedSharesOutstanding'], 
['bookValue'], ['priceToBook'], ['lastFiscalYearEnd'], 
['nextFiscalYearEnd'], ['mostRecentQuarter'], 
['earningsQuarterlyGrowth'], ['netIncomeToCommon'], 
['trailingEps'], ['forwardEps'], ['pegRatio'], 
['lastSplitFactor'], ['lastSplitDate'], ['enterpriseToRevenue'], 
['enterpriseToEbitda'], ['52WeekChange'], ['SandP52WeekChange'], 
['lastDividendValue'], ['lastDividendDate'], ['exchange'], 
['quoteType'],
['shortName'], ['longName'], ['firstTradeDateEpochUtc'], 
['timeZoneFullName'], ['timeZoneShortName'], 
['uuid'], ['messageBoardId'], 
['gmtOffSetMilliseconds'], ['currentPrice'], 
['targetHighPrice'], ['targetLowPrice'], ['targetMeanPrice'], 
['targetMedianPrice'], ['recommendationMean'], 
['recommendationKey'], ['numberOfAnalystOpinions'], ['totalCash'], 
['totalCashPerShare'],[ 'ebitda'], ['totalDebt'], 
['quickRatio'], ['currentRatio'], ['totalRevenue'], 
['debtToEquity'], ['revenuePerShare'], ['returnOnAssets'], 
['returnOnEquity'], ['freeCashflow'], 
['operatingCashflow'], ['earningsGrowth'], 
['revenueGrowth'], ['grossMargins'], ['ebitdaMargins'], 
['operatingMargins'], ['financialCurrency'], ['trailingPegRatio']]





# Helper functions
## Introduce Chat GPT Message bot here
def message_cleanup(arg: str) -> str:
    if BOT_USERNAME in arg:
        return arg.replace(BOT_USERNAME, 'Please key in a command, thank you :)')
    else:
        return 'Please key in a command, thank you :)'
    
# This works well enough
def get_data(stocks: List[str], info_type: str) -> str:
    overall_reply: str = ''
    for stock in stocks:
        stck = yf.Ticker(stock)
        if not stock:
            return "This stock does not exist"
        else:
            stock_reply: str = f'{stock}: \n'
            inf_string: str = stck.info.get(info_type)
            if not inf_string:
                return "Wrong type of information request"
            else:
                stock_reply += f'{info_type}: {inf_string}\n'
                overall_reply += stock_reply + '\n'
    return overall_reply









# Command Handlers
## Change to daily once confident
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.message.chat_id
    isRepeat = True
    Text: str ='Hello there, thank you for using my finance bot,'\
    '\n\ntype /help to check out what are some of the commands you can utalise'\
    '\nin keeping track with your financial investment data.'
    await context.bot.send_message(update.message.chat_id, Text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Text: str = "/start is to start the application for an intro to the bot"\
    "\n/help is to request a description of the commands in this bot,"\
    "\n\n"\
    "\n/serchstock is to get the latest required data of a stock/s"\
    "\n/setupdates is the same as /serchstock, but you get updated daily"\
    "\n/setpricenotification is to set a custom notification of a stock/s"\
    "\n/turnoffcusupdate is to turn off the custom updates that you had previously set with"\
    "\nthe /setupdates command"\
    "\n\n/turnoncusupdate turns back on the custom updates that you have previously set with"\
    "\nthe /setupdates command"\
    "\n\n/turnoffpricealert turns off the price alert that has been set with the command /setpricenotification"\
    "\nThere is no turn on command for price alert, once turned off, you would need to re-set it again using"\
    "\nthe /setpricenotification command"\
    "\n/cancel Allows you to end any conversation with the bot"\
    "\n\n"\
    "\nEnjoy using our bot!!! :)"
    await context.bot.send_message(update.message.chat_id, Text)

async def turnoffcusupdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_custom_repeat
    if is_custom_repeat:
        current_jobs = application.job_queue.get_jobs_by_name('custom_update')
        for job in current_jobs:
            job.schedule_removal()
        is_custom_repeat = False
        return await update.message.reply_text('Custom updates have been turned off')
    else:
        return await update.message.reply_text('You currently do not have any custom updates to turn off at the moment :(')

## Remove Test once you are confident
async def turnoncusupdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_custom_repeat
    if not is_custom_repeat:
        if update_freq == 'Daily':
            application.job_queue.run_daily(custom_repeat, time=update_time, name='custom_update')
            is_custom_repeat = True
            return await update.message.reply_text('Your custom updates have been turned back on again :)')
        elif update_freq == 'Weekly':
            application.job_queue.run_daily(custom_repeat, time=update_time, days=update_day, name='custom_update')
            is_custom_repeat = True
            return await update.message.reply_text('Your custom updates have been turned back on again :)')
        elif update_freq == 'Monthly':
            application.job_queue.run_monthly(custom_repeat, time=update_time, days=update_day, name='custom_update')
            is_custom_repeat = True
            return await update.message.reply_text('Your custom updates have been turned back on again :)')
        elif update_freq == 'Test':
            application.job_queue.run_repeating(custom_repeat, interval=10, first=3, name='custom_update')
            is_custom_repeat = True
            return await update.message.reply_text('Your custom updates have been turned back on again :)')
        else:
            pass
    else:
        return await update.message.reply_text('Sorry you do not have any custom updates to turn on :(')

async def turnoffpricealert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_alert_repeat
    if is_alert_repeat:
        current_jobs = application.job_queue.get_jobs_by_name('price_alert')
        for job in current_jobs:
            job.schedule_removal()
        is_alert_repeat = False
        return await update.message.reply_text('Price alerts have been turned off')
    else:
        return await update.message.reply_text('You currently do not have any price alerts to turn off at the moment :(')



# Conversation Handlers, entry and state functions
# Search Stock Command:
async def searchstock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question: str = "Enter the stock ticker/s you would like to search"\
    "\n\nPlease enter in all caps for e.g. AAPL"\
    "\n\nIf you are searching for more than one ticker:"\
    "\n\nplease add a comma and a space at the end of each ticker e.g. AAPL, MSFT, NVDA"\
    "\n\nYou can end this conversation anytime by typing /close command"
    await update.message.reply_text(question)
    return TICKER

## Should have error handling here
async def ticker_setter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: str = update.message.text
    global tickers
    tickers = message.split(", ")
    reply_keyboard: List[List[str]] = ticker_methods
    await update.message.reply_text("Great now enter the type of information you require: ", 
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return INFO

## Error handling should be better here
async def stock_info (update: Update, context: ContextTypes.DEFAULT_TYPE):
    info: str = update.message.text
    response: str = get_data(tickers, info)
    if response == "This stock does not exist":
        await update.message.reply_text("This stock does not exist", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    elif response == "Wrong type of information request":
        await update.message.reply_text("Wrong type of information request", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        reply: str = f'Your data: \n{response}'\
        '\nThank you for searching :)'
        await update.message.reply_text(reply)
        return ConversationHandler.END


# Set Updates Command:
async def setupdates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question: str = "Enter the stock ticker/s you would like to search"\
    "\n\nPlease enter in all caps for e.g. AAPL"\
    "\n\nIf you are searching for more than one ticker:"\
    "\n\nplease add a comma and a space at the end of each ticker e.g. AAPL, MSFT, NVDA"\
    "\n\nYou can end this conversation anytime by typing /close command"
    global chat_id
    chat_id = update.message.chat_id
    await update.message.reply_text(question)
    return TICKER

## Should have error handling here, remember to return Conv end and reply text for all
async def setupdates_tickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: str = update.message.text
    global tickers
    tickers = message.split(", ")
    reply_keyboard: List[List[str]] = ticker_methods
    await update.message.reply_text("Great now enter the type of information you require: ", 
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return INFO

async def setupdates_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global update_info
    update_info = update.message.text
    if update_info not in ticker_methods:
        reply_keyboard: List[List[str]] = [["Daily"], ["Weekly"], ["Monthly"], ["Test"]]
        await update.message.reply_text("Greate now please enter the frequency you would like to be updated with: ", 
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return FREQ
    else:
        await update.message.reply_text("You have keyed in the wrong info type", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

## Remove Test once confident
async def setupdates_freq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global update_freq
    update_freq = update.message.text
    if update_freq != "Daily" or "Weekly" or "Monthly" or "Test":
        message: str = 'Greate now enter the starting time you would like this update feature to begine:'\
        '\nEnter like this: 00:00:00'\
        '\nThey represent HH:MM:SS, where H is Hours, M is minutes & S is seconds'
        await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
        return TIME
    else:
        await update.message.reply_text("You keyed in the wrong freq", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

## Error case handling needs to be improved here
async def setupdates_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global update_time
    message: List[str] = update.message.text.split(':')
    Hours: int = int(message[0])
    Minutes: int = int(message[1])
    Seconds: int = int(message[2])
    update_time = datetime.time(Hours, Minutes, Seconds)
    if update_time == 'error':
        await update.message.reply_text('You have keyed in the wrong time')
        return ConversationHandler.END
    else:
        reply: str = 'Great now key in the day you would like to be updated'\
        '\n\nIf you selected Daily, you can just key in 0'\
        '\n\nIf you selected Weekly, key in from 0 to 6 which represents Mon to Sun'\
        '\n\nIf you selected Monthly, key in from 1 to 31 which represents the first to last day of a month'
        await update.message.reply_text(reply)
        return DAY

## Remove Test once confident
async def setupdates_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global update_day
    update_day = int(update.message.text)
    if update_day > 31:
        await update.message.reply_text("You have keyed in the wrong day value")
        return ConversationHandler.END
    else:
        global is_custom_repeat
        if update_freq == 'Daily':
            application.job_queue.run_daily(custom_repeat, time=update_time, name='custom_update')
            is_custom_repeat = True
        elif update_freq == 'Weekly':
            application.job_queue.run_daily(custom_repeat, time=update_time, days=update_day, name='custom_update')
            is_custom_repeat = True
        elif update_freq == 'Monthly':
            application.job_queue.run_monthly(custom_repeat, time=update_time, days=update_day, name='custom_update')
            is_custom_repeat = True
        elif update_freq == 'Test':
            application.job_queue.run_repeating(custom_repeat, interval=10, first=3, name='custom_update')
            is_custom_repeat = True
        else:
            await update.message.reply_text('You did not key in the right frequency')
            return ConversationHandler.END
        reply: str = 'Great you have now set up your update function'\
        '\n\nThank you :)'
        await update.message.reply_text(reply)
        return ConversationHandler.END


# Set up price notification:
async def setpricenotification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question: str = "Enter the stock ticker/s you would like to search"\
    "\n\nPlease enter in all caps for e.g. AAPL"\
    "\n\nIf you are searching for more than one ticker:"\
    "\n\nplease add a comma and a space at the end of each ticker e.g. AAPL, MSFT, NVDA"\
    "\n\nYou can end this conversation anytime by typing /close command"
    global chat_id
    chat_id = update.message.chat_id
    await update.message.reply_text(question)
    return TICKER

## Error handling should be better here
async def setpricenotification_tickers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: str = update.message.text
    global alert_stock
    alert_stock = message.split(", ")
    
    for stock in alert_stock:
        test = yf.Ticker(stock)
        if test == 'error':
            return await update.message.reply_text('You keyed in invalid tickers :(')
        else:
            pass
    
    reply_keyboard: List[List[str]] = ticker_methods
    await update.message.reply_text("Great now enter the type of information you require: ", 
                                     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return INFO

async def setpricenotification_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global alert_info
    alert_info = update.message.text
    if alert_info not in ticker_methods:
        message: str = 'Greate now please enter the price at which you would like to be alerted with: '\
        '\n\nEnter only the dollar value and 2 decimal points max, without the dollar sign'\
        '\n\nEnter the prices in order of how you enterd the stock tickers two steps ago'\
        '\n\nwith a comma and space seperating each, for e.g.: 10.00, 30.00, 100.00'
        await update.message.reply_text(message, 
                                    reply_markup=ReplyKeyboardRemove())
        return PRICE
    else:
        await update.message.reply_text("You have keyed in the wrong info type", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

## Should add some form of Error handler here
async def setpricenotification_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global alert_price
    alert_price_string: List[str] = update.message.text.split(', ')
    alert_price = (float(price) for price in alert_price_string)
    reply_keyboard: List[List[str]] = [["Once"], ["10 Seconds"], ["1 Minute"], 
                                        ["5 Minutes"], ["10 Minutes"], 
                                        ["30 Minutes"], 
                                        ["1 Hour"]]
    await update.message.reply_text("Greate now please enter the frequency you would like to be alerted with: ", 
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return FREQ

## Should have error handling for this part, works but keep on getting some error
async def setpricenotification_freq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global alert_freq
    global is_alert_repeat
    global alert_stock
    alert_freq_string = update.message.text
    if alert_freq_string == 'Once':
        alert_freq = 1
    elif alert_freq_string == '10 Seconds':
        alert_freq = 10
    elif alert_freq_string == '1 Minute':
        alert_freq = 60
    elif alert_freq_string == '5 Minute':
        alert_freq = 300
    elif alert_freq_string == '10 Minutes':
        alert_freq = 600
    elif alert_freq_string == '30 Minutes':
        alert_freq = 1800
    elif alert_freq_string == '1 Hour':
        alert_freq = 3600
    else:
        await update.message.reply_text('You did not key in the right frequency', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    is_alert_repeat = True
    await update.message.reply_text('Your price notification has been set, thank you :)', reply_markup=ReplyKeyboardRemove())
    while is_alert_repeat:
        for index, price in enumerate(alert_price):
            stock = alert_stock[index]
            stock_curr_price: float = yf.Ticker(stock).info.get('currentPrice')
            if price == stock_curr_price:
                if alert_freq == 1:
                    application.job_queue.run_once(price_repeat, name='price_alert')
                    return ConversationHandler.END
                else:
                    application.job_queue.run_repeating(price_repeat, interval=alert_freq, name='price_alert')
                    return ConversationHandler.END
        time.sleep(10)
    return ConversationHandler.END


# Cancel function for Conversation Fallback:
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You have ended the conversation", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END




# MessageHandlers
async def standard_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: str = message_cleanup(update.message.text)
    await context.bot.send_message(update.message.chat_id, message)





# Job Schedulers functions
# Need to create proper default_repeat function 
async def custom_repeat(context: ContextTypes.DEFAULT_TYPE):
    global tickers
    global update_info
    data: str = get_data(tickers, update_info)
    if data == "This stock does not exist":
        data = "This stock does not exist"
    elif data == "Wrong type of information request":
        data = "Wrong type of information request"
    else:
        # Need to change out the user_id to a proper user_id
        await context.bot.send_message(chat_id=chat_id, text=data)

async def price_repeat(context: ContextTypes.DEFAULT_TYPE):
    global alert_stock
    global alert_info
    data: str = get_data(alert_stock, alert_info)
    price_data: str = get_data(alert_stock, 'currentPrice')
    if data == "This stock does not exist":
        data = "This stock does not exist"
    elif data == "Wrong type of information request":
        data = "Wrong type of information request"
    else:
        # Need to change out the user_id to a proper user_id
        response: str = data + '\n\n' + price_data
        await context.bot.send_message(chat_id=chat_id, text=response)




# Creation of the telegram bot
if __name__ == '__main__':

    # Command Handlers
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('turnoffcusupdate', turnoffcusupdate))
    application.add_handler(CommandHandler('turnoncusupdate', turnoncusupdate))
    application.add_handler(CommandHandler('turnoffpricealert', turnoffpricealert))

    # Conversation Handlers
    conv_handler_searchstock = ConversationHandler(entry_points=[CommandHandler('searchstock', searchstock)], 
                                                   states={
                                                       TICKER: [MessageHandler(filters.TEXT, ticker_setter)], 
                                                       INFO: [MessageHandler(filters.TEXT, stock_info)]
                                                   }, 
                                                   fallbacks=[CommandHandler('cancel', cancel)])
    
    conv_handler_setupdates = ConversationHandler(entry_points=[CommandHandler('setupdates', setupdates)], 
                                                  states={
                                                      TICKER: [MessageHandler(filters.TEXT, setupdates_tickers)],
                                                      INFO: [MessageHandler(filters.TEXT, setupdates_info)],
                                                      FREQ: [MessageHandler(filters.TEXT, setupdates_freq)],
                                                      TIME: [MessageHandler(filters.TEXT, setupdates_time)],
                                                      DAY: [MessageHandler(filters.TEXT, setupdates_day)]
                                                  }, 
                                                  fallbacks=[CommandHandler('cancel', cancel)])
    
    conv_handler_setpricenotification = ConversationHandler(entry_points=[CommandHandler('setpricenotification', setpricenotification)], 
                                                            states={
                                                                TICKER: [MessageHandler(filters.TEXT, setpricenotification_tickers)],
                                                                INFO: [MessageHandler(filters.TEXT, setpricenotification_info)],
                                                                PRICE: [MessageHandler(filters.TEXT, setpricenotification_price)],
                                                                FREQ: [MessageHandler(filters.TEXT, setpricenotification_freq)]
                                                            }, 
                                                            fallbacks=[CommandHandler('cancel', cancel)])

    application.add_handler(conv_handler_searchstock)
    application.add_handler(conv_handler_setupdates)
    application.add_handler(conv_handler_setpricenotification)


    # Message Handlers (Always add last)
    application.add_handler(MessageHandler(filters.TEXT, standard_message))
    
    
    application.run_polling()