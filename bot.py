import config
import telebot
import apiai
import json
import logging
import time

bot = telebot.TeleBot(token=config.token)


@bot.message_handler(commands=['start'])
def startCommand(message):
    if message.chat.id:
        bot.send_message(chat_id=message.chat.id, text='Приветствую')
    else:
        bot.send_message(chat_id=message.from_user.id, text='Приветствую')


@bot.message_handler(content_types=['text'])
def textMessage(message):
    request = apiai.ApiAI(config.flow_token).text_request()  # Токен API к DialogFlow
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = config.session_id_flow
    request.query = message.text   # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']      # Разбираем JSON и вытаскиваем ответ
    if message.chat.id:
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
        if response:
            bot.send_message(message.chat.id, text=response)
        else:
            bot.send_message(message.chat.id, text='Чет какую-то дичь вы несете')
    else:
        if response:
            bot.send_message(message.from_user.id, text=response)
        else:
            bot.send_message(message.from_user.id, text='Чет какую-то дичь вы несете')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(e)
        time.sleep(15)
