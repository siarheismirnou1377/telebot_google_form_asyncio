import asyncio
import time
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

import requests
from bs4 import BeautifulSoup


dp = Dispatcher()

url = ''  # Ссылка которую можно задать через бота

async def main():  # Запуск бота

    bot = Bot('токен', parse_mode=ParseMode.HTML)  # В ковычки вставить токен
    await dp.start_polling(bot)

@dp.message(CommandStart())  
async def start_bot(message: Message):  # Хендлим команду старт
    kb = [[KeyboardButton(text="Начать"), KeyboardButton(text="Задать ссылку")],]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
 
    await message.reply(f"Привет, {(message.from_user.full_name)}! Нажми 'Задать ссылку', а потом 'Начать', чтобы отслеживать форму.",
                        reply_markup=keyboard)

@dp.message()  
async def parser_form(message: Message):  # Парсинг формы и проверка
    global url
    count = 0
    
    if(message.text == "Начать"):
        await message.answer("Начал отслеживать форму.")
        while True:
            interval = random.randint(5, 10)
            response = requests.get(url)
            bs = BeautifulSoup(response.text, "lxml")
            soup =  bs.find(class_="UatU5d")
            elem_soup = BeautifulSoup(str(soup), 'html.parser')
            elem_soup = elem_soup.text
            
            if soup and count == 0:  # Если сродержт тег и это первый запуск
                await message.answer(text=elem_soup)
                count = 1
                time.sleep(interval)
                print('Первое условие', interval)
                continue
            if soup and count == 1:  # Если содержит тег и это >= 2 запуску
                print('Второе условие', interval)
                time.sleep(interval)
                continue
            else:  # Если не содержит тег
                await message.answer("Ссылка формы изменила свой статус. Проверь ссылку{0}".format(url))
                count = 0
                print('Третье условие', interval)
                break
    if (message.text == "Задать ссылку"):
        await message.answer("Скопируй ссылку и отправь мне.")   
    
   
if __name__ == "__main__":
    asyncio.run(main())