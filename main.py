import telebot
import sqlite3
from sqlite3 import Error
from time import sleep, ctime
from telebot import types
import requests
from datetime import datetime

bot = telebot.TeleBot("6171211954:AAF7BGZBRsA0wS4qskbWEdQywHcD6pkYkx8")

# обработчик SQL выражений через функцию:
def post_sql_query(sql_query):
    with sqlite3.connect('db\my.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result

# функция создания таблицы в sqlite и в качестве ключа primary key определить сделать id user:
def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        reg_date TEXT);'''
    post_sql_query(users_query)

# функция регистрации пользователя:
def register_user(user, username, first_name, last_name):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
    user_check_data = post_sql_query(user_check_query)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
        post_sql_query(insert_to_db_query)

create_tables()

response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
if response.status_code == 200:
    content = response.json()
    Sp_Valute = content.get('Valute')
    Get_USD = Sp_Valute.get('USD')
    Get_Name_USD = Get_USD.get('Name')
    Get_Value_USD = Get_USD.get('Value')
    Get_EUR = Sp_Valute.get('EUR')
    Get_Name_EUR = Get_EUR.get('Name')
    Get_Value_EUR = Get_EUR.get('Value')
    Get_CNY = Sp_Valute.get('CNY')
    Get_Name_CNY = Get_CNY.get('Name')
    Get_Value_CNY = Get_CNY.get('Value')


@bot.message_handler(commands=['start'])
def start(message):
    register_user(message.from_user.id, message.from_user.username,
                  message.from_user.first_name, message.from_user.last_name)
    bot.send_message(message.from_user.id, f'Доброе время суток, {message.from_user.first_name}' )

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Доллар США')
    btn2 = types.KeyboardButton(text='Евро')
    btn3 = types.KeyboardButton(text='Китайский юань')
    kb.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Выберите', reply_markup=kb)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Доллар США':
        bot.send_message(message.chat.id,Get_Value_USD)
    elif message.text == 'Евро':
        bot.send_message(message.chat.id, Get_Value_EUR)
    elif message.text == 'Китайский юань':
        bot.send_message(message.chat.id, Get_Value_CNY)

bot.polling(none_stop=True)
