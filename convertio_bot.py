import telebot
from config import TOKEN, keys
from extensions import ExchangeException, Exchange

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = 'Для начала работы введите: \n <имя валюты, цену которой хотите узнать> ' \
           '\n <имя валюты, в которой надо узнать цену первой валюты>' \
           '\n <количество первой валюты> ' \
           '\n \n Чтобы вызвать список доступных валют, воспользуйтесь командой /values.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException(f'Введены лишние данные, проверьте запись вашего запроса.')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя.\n{e}'),
    except Exception:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()