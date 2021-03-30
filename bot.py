import telebot
import time
import random
import requests
import settings
from lib import weatherfunctions
from lib import bankfunctions
from lib import afishafunctions
from lib import dbfunctions
from lib import keyboard
import consts
from bs4 import BeautifulSoup

settings.init()
consts.init()
keyboard.init()
bot = telebot.TeleBot(settings.TG_BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])

def send_text(message):
    dbfunctions.addUser(message)
    dbfunctions.botLogs(message)
    if dbfunctions.isUserAdmin(message) == True:
        adminFlag = 'Y'
    else:
        adminFlag = 'N'
    if message.text.lower() == 'погода сейчас':
        weather = weatherfunctions.weatherNow()
        if adminFlag == 'N':
            bot.send_message(message.chat.id, weather, reply_markup=keyboard.keyboard1, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, weather, reply_markup=keyboard.keyboardA1, parse_mode="Markdown")
    elif message.text.lower() == 'погода на 5 дней':
        weather = weatherfunctions.weatherFiveDays()
        if adminFlag == 'N':
            bot.send_message(message.chat.id, weather, reply_markup=keyboard.keyboard1, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, weather, reply_markup=keyboard.keyboardA1, parse_mode="Markdown")
    elif message.text.lower() == 'курсы':
        bot.send_message(message.chat.id, 'Выберите интересующий вас курс', reply_markup=keyboard.keyboard2)
    elif message.text.lower() == 'usd':
        bot.send_message(message.chat.id, bankfunctions.getBestBankCource(consts.BANK_USD_BUY_ID, consts.BANK_USD_SELL_ID, 'USD'), reply_markup=keyboard.keyboard1, parse_mode="Markdown")
    elif message.text.lower() == 'eur':
        bot.send_message(message.chat.id, bankfunctions.getBestBankCource(consts.BANK_EUR_BUY_ID, consts.BANK_EUR_SELL_ID, 'EUR'), reply_markup=keyboard.keyboard1, parse_mode="Markdown")
    elif message.text.lower() == 'rub':
        bot.send_message(message.chat.id, bankfunctions.getBestBankCource(consts.BANK_RUB_BUY_ID, consts.BANK_RUB_SELL_ID, 'RUB'), reply_markup=keyboard.keyboard1, parse_mode="Markdown")
    elif message.text.lower() == 'афиша':
        bot.send_message(message.chat.id, afishafunctions.getKinoAfisha(), reply_markup=keyboard.keyboard1, parse_mode="Markdown")
    elif message.text.lower() == 'админ':
        if adminFlag == 'Y':
            bot.send_message(message.chat.id, 'Добрый день, Адмнистратор', reply_markup=keyboard.keyboardA2, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, 'Мне не знакома твоя команда, нажми на кнопку', reply_markup=keyboard.keyboard1, parse_mode="Markdown")
    elif message.text.lower() == 'логи':
        if adminFlag == 'Y':
            bot.send_message(message.chat.id, dbfunctions.getLogs(), reply_markup=keyboard.keyboardA2, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, 'Мне не знакома твоя команда, нажми на кнопку', reply_markup=keyboard.keyboard1, parse_mode="Markdown")
    elif message.text.lower() == 'сменить город':
        bot.send_message(message.chat.id, 'Выберите ваш город', reply_markup=keyboard.getInlineKeyboard(message))
        bot.send_message(message.chat.id, 'Что дальше?', reply_markup=keyboard.keyboard1)
    else:
        bot.send_message(message.chat.id, 'Мне не знакома твоя команда, нажми на кнопку', reply_markup=keyboard.keyboard1)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    dbfunctions.setNewCity(call)
    
bot.polling()