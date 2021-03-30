import telebot
from lib import dbfunctions
def init():
    global keyboard1
    global keyboard2
    global keyboardA1
    global keyboardA2
    global keyboardInline
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True)
    keyboard1.row('Погода сейчас', 'Погода на 5 дней', 'Курсы','Афиша', 'Сменить город')
    keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True, True)
    keyboard2.row('USD', 'EUR', 'RUB')

    keyboardA1 = telebot.types.ReplyKeyboardMarkup(True, True, True)
    keyboardA1.row('Погода сейчас', 'Погода на 5 дней', 'Курсы','Афиша', 'Сменить город', 'Админ')
    keyboardA2 = telebot.types.ReplyKeyboardMarkup(True, True, True)
    keyboardA2.row('Логи', 'Вернуться в начало')

def getInlineKeyboard(message):
    userId = message.from_user.id
    userCity = dbfunctions.getUserCity(userId)
    keyboardInline = telebot.types.InlineKeyboardMarkup();
    if (userCity == 'minsk'):
        key_minsk = telebot.types.InlineKeyboardButton( '✅Минск', callback_data='minsk')
    else:
        key_minsk = telebot.types.InlineKeyboardButton('Минск', callback_data='minsk')

    if (userCity == 'brest'):
        key_brest = telebot.types.InlineKeyboardButton('✅Брест', callback_data='brest')
    else:
        key_brest = telebot.types.InlineKeyboardButton('Брест', callback_data='brest')
    if (userCity == 'gomel'):
        key_gomel = telebot.types.InlineKeyboardButton('✅Гомель', callback_data='gomel')
    else:
        key_gomel = telebot.types.InlineKeyboardButton('Гомель', callback_data='gomel')

    if (userCity == 'grodno'):
        key_grodno = telebot.types.InlineKeyboardButton('✅Гродно', callback_data='grodno')
    else:
        key_grodno = telebot.types.InlineKeyboardButton('Гродно', callback_data='grodno')

    if (userCity == 'mohilev'):
        key_mohilev = telebot.types.InlineKeyboardButton('✅Могилев', callback_data='mohilev')
    else:
        key_mohilev = telebot.types.InlineKeyboardButton('Могилев', callback_data='mohilev')

    if (userCity == 'vitebsk'):
        key_vitebsk = telebot.types.InlineKeyboardButton('✅Витебск', callback_data='vitebsk')
    else:
        key_vitebsk = telebot.types.InlineKeyboardButton('Витебск', callback_data='vitebsk')
    
    keyboardInline.add(key_minsk); 
    keyboardInline.add(key_brest); 
    keyboardInline.add(key_gomel); 
    keyboardInline.add(key_grodno); 
    keyboardInline.add(key_mohilev); 
    keyboardInline.add(key_vitebsk); 
    return keyboardInline