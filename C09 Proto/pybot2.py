import os
import random
import logging
import telegram
from twilio.rest import Client
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from dotenv import load_dotenv

load_dotenv()
bot = telegram.Bot(token=str(os.environ.get('TOKEN')))
print(bot.get_me())
updates = bot.get_updates()

updater = Updater(token=str(os.environ.get('TOKEN')), use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text[6:])

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def otp(update: Update, context: CallbackContext):
    global otpc
    otpc = random.randint(100000,999999)
    context.bot.send_message(chat_id=update.effective_chat.id, text=otpc)
    context.bot.send_message(chat_id=update.effective_chat.id, text="A OTP has been sent to you, please enter the 6 digit code")

def checkotp(update: Update, context: CallbackContext):
    try:
        if int(update.message.text[10:]) == otpc:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Login Success")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong Passcode")
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid Passcode")

    

def talking(update: Update, context: CallbackContext):
    if update.message.text == "Happy New Year":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Happy New Year! I wish you have a great 2022!")
    elif update.message.text == "Carlson":
        context.bot.send_message(chat_id=update.effective_chat.id, text="He is the creator of C09 Bot!")
    elif update.message.text == "How are you":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Im feeling great!")
    elif update.message.text == "Secret":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Shhhhhh.... This is a secret! But I really enjoy Anime and Manga.")

def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

talking_handler = MessageHandler(Filters.text & (~Filters.command), talking)
dispatcher.add_handler(talking_handler)

echo_handler = CommandHandler('echo', echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

otp_handler = CommandHandler('otp', otp)
dispatcher.add_handler(otp_handler)

checkotp_handler = CommandHandler('checkotp', checkotp)
dispatcher.add_handler(checkotp_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

