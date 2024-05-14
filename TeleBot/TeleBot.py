import telebot
from config import TOKEN, keys
from extensions import Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, f"Здравствуйте {message.chat.first_name}! "
                                      f"Этот бот является калькулятором валют. "
                                      f"Для расчета валют введите сообщение следующего формата:\n"
                                      f"<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n"
                                      f"Для того, чтобы получить список всех доступных валют, введите команду /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):

    data = message.text.split(' ')
    if len(data) != 3:
        bot.reply_to(message, 'Не верное количество параметров для совершения операции /help')
        return

    quote, base, amount = map(lambda s: s.lower(), data)
    if quote not in keys:
        bot.reply_to(message, f'Валюты "{quote}" нет в списке доступных /values')
        return
    elif base not in keys:
        bot.reply_to(message, f'Валюты "{base}" нет в списке доступных /values')
        return
    try:
        amount = float(amount)
        new_amount = Converter.convert(keys[quote], keys[base], amount)
    except ValueError:
        bot.reply_to(message, 'Введите численное значение валюты для конвертации /help')
        return
    except Exception as e:
        print(e)
        bot.reply_to(message, 'Что-то пошло не так, попробуйте позже :)')
        return

    bot.reply_to(message, f'{amount} {quote} в {base} : {new_amount}')


bot.polling(none_stop=True)

