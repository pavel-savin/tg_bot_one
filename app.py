import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConvertor
import pymorphy3

bot = telebot.TeleBot(TOKEN)
morph = pymorphy3.MorphAnalyzer()

def normal_str_output(curency_name, amount):
    parsed_word = morph.parse(curency_name)[0]
    
    if int(amount) == 1:
        case = 'nomn'
    else:
        case = 'gent'
    
    inflected = parsed_word.inflect({case})
    
    if inflected is None:
        return curency_name
    
    return inflected.word
    
@bot.message_handler(commands=["start", "help"])  # Помощь
def start_message(message: telebot.types.Message):
    text = "Чтобы начать работу введите комндау боту в следующем формате:\n<Имя валюты>\
        <в какую валюту перевести>\
        <количество переводимой валюты>.\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])  # Вывод доступных валют
def values_message(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    for key, value in keys.items():
        text += f"{key} - {value}\n"
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])  # Ответ на запрос пользователя
def convert(message: telebot.types.Message):
    values = message.text.lower().split(" ")

    if len(values) != 3:
        raise ConnectionAbortedError("Не верное колличество параметров")

    quote, base, amount = values

    try:
        total_base = CryptoConvertor.get_price(quote, base, amount)
        quote_correct = normal_str_output(keys[quote], amount)
        base_correct = normal_str_output(keys[base], amount)
        text = f"Цена {amount} {quote_correct} в {base_correct} - {total_base}"
    except ConvertionException as e:
        text = f"Ошибка конвертации: {e}"

    bot.send_message(message.chat.id, text)


bot.polling()
