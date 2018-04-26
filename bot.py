import config
import telebot
import apiai
import json

bot = telebot.TeleBot(token=config.token)


@bot.message_handler(commands=['start'])
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Дарова, щеглы')


@bot.message_handler(content_types=['text'])
def textMessage(message):
    request = apiai.ApiAI(config.flow_token).text_request()  # Токен API к DialogFlow
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = config.session_id_flow
    request.query = message.text   # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']      # Разбираем JSON и вытаскиваем ответ

    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(message.from_user.id, text=response)
    else:
        bot.send_message(message.from_user.id, text='Чет какую-то дичь вы несете')


bot.polling(none_stop=True)
