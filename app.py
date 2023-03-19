import logging
import os

import telebot
from dotenv import load_dotenv
from flask import Flask
from telebot.types import Message

from config.containers import Container
from config.routes import configure_routes
from service.bot_service import is_command, BotService

load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(token=TOKEN, threaded=False)
app = Flask(__name__)

container = Container()
app.container = container
configure_routes(app, bot)


@bot.message_handler(commands=['start'])
def command_start(message):
    cid = message.chat.id
    bot.send_message(
        cid, "Bem vindo ao Bot de Dividas 3.0")


@bot.message_handler(func=lambda message: is_command(message.text))
def add_purchase(message: Message,
                 service: BotService = container.bot_service()):
    chat_id = message.chat.id
    try:
        purchase_string = message.text
        service.add_purchase(chat_id, purchase_string)
        bot.send_message(chat_id, "Compra adicionada com sucesso!")
    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(chat_id, "Ops... Deu um erro no sistema :(")


@bot.message_handler(commands=['fatura'])
def command_show_debts(message: Message,
                       service: BotService = container.bot_service()):
    chat_id = message.chat.id
    try:
        message = service.list_debts(chat_id)
        bot.send_message(chat_id, message, parse_mode='MarkdownV2')
    except Exception as e:
        logging.error(e, exc_info=True)
        bot.send_message(chat_id, "Ops... Deu um erro no sistema :(")
