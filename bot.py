import logging
from telebot import TeleBot, types
import requests
from datetime import datetime

# Налаштування базового логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Створення логера
logger = logging.getLogger(__name__)

TOKEN = '7321141087:AAGopgtpAlagJvB2gTso-IH7GXSuJF6vSSw'
bot = TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f"User {message.from_user.username} started the bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Запит про допомогу")
    item2 = types.KeyboardButton("Пропозиція допомоги")
    item3 = types.KeyboardButton("Меню")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Ласкаво просимо! Оберіть опцію:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Запит про допомогу")
def request_help(message):
    logger.info(f"User {message.from_user.username} selected 'Запит про допомогу'")
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "Введіть ваше ім'я:")
    bot.register_next_step_handler(msg, get_name, "request")

@bot.message_handler(func=lambda message: message.text == "Пропозиція допомоги")
def offer_help(message):
    logger.info(f"User {message.from_user.username} selected 'Пропозиція допомоги'")
    user_data[message.chat.id] = {}
    msg = bot.send_message(message.chat.id, "Введіть ваше ім'я:")
    bot.register_next_step_handler(msg, get_name, "offer")

def get_name(message, type):
    logger.info(f"User {message.from_user.username} entered their name: {message.text}")
    user_data[message.chat.id]['name'] = message.text
    msg = bot.send_message(message.chat.id, "Введіть ваш номер телефону:")
    bot.register_next_step_handler(msg, get_phone, type)

def get_phone(message, type):
    logger.info(f"User {message.from_user.username} entered their phone: {message.text}")
    user_data[message.chat.id]['phone'] = message.text
    msg = bot.send_message(message.chat.id, "Введіть опис вашої ситуації:")
    bot.register_next_step_handler(msg, get_description, type)

def get_description(message, type):
    logger.info(f"User {message.from_user.username} entered their description: {message.text}")
    user_data[message.chat.id]['description'] = message.text
    user_data[message.chat.id]['telegram_nickname'] = message.from_user.username
    user_data[message.chat.id]['timestamp'] = format_timestamp(message.date)

    if type == "request":
        save_request(message)
    else:
        save_offer(message)

def format_timestamp(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    formatted_time = dt_object.strftime('%H:%M, %d-%m-%Y')
    return formatted_time

def save_request(message):
    data = user_data[message.chat.id]
    logger.info(f"Saving request for user {message.from_user.username}")
    response = requests.post('http://127.0.0.1:5000/add_request', data={
        'username': message.from_user.username,
        'name': data['name'],
        'phone': data['phone'],
        'telegram_nickname': data['telegram_nickname'],
        'description': data['description'],
        'timestamp': data['timestamp']
    })
    bot.send_message(message.chat.id, response.text)

def save_offer(message):
    data = user_data[message.chat.id]
    logger.info(f"Saving offer for user {message.from_user.username}")
    response = requests.post('http://127.0.0.1:5000/add_offer', data={
        'username': message.from_user.username,
        'name': data['name'],
        'phone': data['phone'],
        'telegram_nickname': data['telegram_nickname'],
        'description': data['description'],
        'timestamp': data['timestamp']
    })
    bot.send_message(message.chat.id, response.text)

@bot.message_handler(func=lambda message: message.text == "Меню")
def menu(message):
    logger.info(f"User {message.from_user.username} selected 'Меню'")
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Переглянути запити про допомогу", callback_data='view_requests')
    item2 = types.InlineKeyboardButton("Переглянути пропозиції допомоги", callback_data='view_offers')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Оберіть опцію:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'view_requests':
        logger.info(f"User {call.from_user.username} selected 'Переглянути запити про допомогу'")
        bot.send_message(call.message.chat.id, "Тут буде список запитів про допомогу.")
    elif call.data == 'view_offers':
        logger.info(f"User {call.from_user.username} selected 'Переглянути пропозиції допомоги'")
        bot.send_message(call.message.chat.id, "Тут буде список пропозицій допомоги.")

if __name__ == '__main__':
    logger.info("Starting polling")
    bot.polling(none_stop=True)
