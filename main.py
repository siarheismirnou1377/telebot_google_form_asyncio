import asyncio

import time
import random

import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message,ReplyKeyboardMarkup



# Нельзя задать ссылку пока идет проверка ссылки
# Нужно назначить команду остановить, чтобы потом задать ссылку
# Нужно добавить исключения если пользователь введет что-то кроме начать, задать ссылку или остановить
# Так же нужно ввести проверку на валидность ссылки

class FormUrl(StatesGroup):
    # Класс состояния
    url = State()

form_router = Router()    
url_text = '' # Ссылка которую можно задать через бота

async def main():  
    # Запуск бота
    bot = Bot('токен', parse_mode=ParseMode.HTML)  # В ковычки вставить токен
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)

@form_router.message(CommandStart())  
async def start_bot(message: Message):
    # Хендлим команду старт
    kb = [[KeyboardButton(text="Начать"), KeyboardButton(text="Задать ссылку"), KeyboardButton(text="Остановить")],]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
 
    await message.reply(f"Привет, {(message.from_user.full_name)}! Нажми 'Задать ссылку', а потом 'Начать', чтобы отслеживать форму.",
                        reply_markup=keyboard)

@form_router.message(F.text == "Начать")  
async def parser_form(message: Message):
    # Парсинг формы и проверка  
    global url_text 
    count = 0
    await message.answer("Начал отслеживать форму. Чтобы остановить процесс проверки и/или задать новую ссылку, сначала нажми 'Остановить.'")    
    while True:
        interval = random.randint(5, 10)
        response = requests.get(url_text)
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
            await message.answer("Ссылка формы изменила свой статус. Проверь ссылку{0}".format(url_text))
            count = 0
            print('Третье условие', interval)
            break

@form_router.message(F.text == "Задать ссылку")
async def start_url(message: Message, state: FSMContext):
    await state.set_state(FormUrl.url)
    await message.answer("Скопируй ссылку и отправь мне.")

@form_router.message(FormUrl.url)
async def process_url(message: Message, state: FSMContext):
    global url_text
    url_text_local = await state.update_data(url=message.text)
    url_text = url_text_local['url']
    print(url_text)

if __name__ == "__main__":
    asyncio.run(main())