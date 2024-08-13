import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConvertor


bot = telebot.TeleBot(TOKEN)


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
        text = f"Цена {amount} {quote} в {base} - {total_base}"
    except ConvertionException as e:
        text = f"Ошибка конвертации: {e}"

    bot.send_message(message.chat.id, text)


bot.polling()
