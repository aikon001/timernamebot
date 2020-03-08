#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to send timed Telegram messages.

This Bot uses the Updater class to handle the bot and the JobQueue to send
timed messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Alarm Bot example, sends a message after a set time.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import random
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler,  CallbackQueryHandler
import os
from gtts import gTTS

alcolici = ["The Rum","The Tequila","The Vodka","The Campari","The Aperol","The Birra","The Assenzio","The Brandy","The Whisky","The Cognac","The Cointreau","The Montenegro","The Gin","The Grappa","Lu Mistra","The Limoncello","The Genziana","The Punch","The Sambuca"]
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def reading_from_string(update,context):
    
    text_to_read = ' '.join(context.args)
    language = 'it'
    slow_audio_speed = False
    filename = 'vocale.mp3'
    
    audio_created = gTTS(text=text_to_read, lang=language,slow=slow_audio_speed)
    audio_created.save(filename)
    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(filename, 'rb'))
    #os.system(f'start {filename}')

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    menu_main = [[InlineKeyboardButton('24 ore', callback_data='m1')],
                 [InlineKeyboardButton('12 ore', callback_data='m2')],
                 [InlineKeyboardButton('6 ore', callback_data='m3')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('Mbe c ha fatt, scegli un opzione:', reply_markup=reply_markup)

def menu_actions(bot, update):
    query = update.callback_query

    if query.data == 'm1':
        due = 86400
        update.message.reply_text('Hai scelto 24 ore')
        
    elif query.data == 'm2':
        due = 43200
     
    elif query.data == 'm3':
        due = 21600

    bot.set_timer(due)
                                  
def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.setChatTitle(job.context,alcolici[random.randrange(0,len(alcolici),1)])


def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    # args[0] should contain the time for the timer in seconds
    due = int(context.args[0])
    if due < 0:
        update.message.reply_text('Non posso tornare indietro nel tempo!')
        return

        # Add job to queue and stop current one if there is a timer already
    if 'job' in context.chat_data:
        old_job = context.chat_data['job']
        old_job.schedule_removal()
    new_job = context.job_queue.run_repeating(alarm, due, context=chat_id)
    context.chat_data['job'] = new_job

    update.message.reply_text('Tant be , timer settato.')



def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer rimosso.')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Run bot."""
    
    PORT = int(os.environ.get('PORT', '5000'))
    bot = telegram.Bot(token = "1112325896:AAGOnkDldoQ-r8F7GT3cP8iWE_5XPcWp30k")
    bot.setWebhook("https://timernamebot.herokuapp.com/" + "1112325896:AAGOnkDldoQ-r8F7GT3cP8iWE_5XPcWp30k")
    
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1112325896:AAGOnkDldoQ-r8F7GT3cP8iWE_5XPcWp30k", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", reading_from_string,pass_args=True))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    dp.add_handler(CallbackQueryHandler(menu_actions))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                       port=PORT,
                       url_path="1112325896:AAGOnkDldoQ-r8F7GT3cP8iWE_5XPcWp30k")
    updater.bot.setWebhook("https://timernamebot.herokuapp.com/" + "1112325896:AAGOnkDldoQ-r8F7GT3cP8iWE_5XPcWp30k")
    updater.idle()
    
    


if __name__ == '__main__':
    main()
