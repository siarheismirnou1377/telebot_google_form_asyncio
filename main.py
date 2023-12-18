import random
import logging
import asyncio

import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message,ReplyKeyboardMarkup
from aiogram.types.error_event import ErrorEvent


class FormUrl(StatesGroup):
    # Класс состояния url.
    url = State()

# Создание роутера.
form_router = Router()
# Ссылка которую можно задать через бота. 
URL_TEXT = '' 
# Параметр работы цикла проверки.
STOP_WHILE = False  

# Создаем объект логгера.
logger = logging.getLogger('my_logger')
# Настройка логгирования.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Создание обработчиков логирования. Запись логов в файл my_log.txt.
file_handler = logging.FileHandler('my_log.txt')
# Файловый обработчик к логгеру.
logger.addHandler(file_handler)

async def main():  
    # Основной запуск бота.
    bot = Bot('YOUR_TOKEN', parse_mode=ParseMode.HTML)  
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)

@form_router.errors()
async def error_handler(event: ErrorEvent):
    # Хендлинг общих критических ошибок. Логгирование в консоль.
    logger.critical("Критическая ошибка вызванная %s", event.exception, exc_info=True)

@form_router.message(CommandStart())  
async def start_bot(message: Message):
    # Хендлинг команды "/start".
    kb = [[KeyboardButton(text="Начать"), KeyboardButton(text="Задать ссылку"), KeyboardButton(text="Остановить")],]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
 
    await message.reply(f"Привет, {(message.from_user.full_name)}! Нажми 'Задать ссылку', а потом 'Начать', чтобы отслеживать форму.",
                        reply_markup=keyboard)
    logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} вызвал команду /start")

""" @form_router.message(Command("mycommand"))  # Запуск бота по собственной команде
async def start_bot(message: Message):
    # Хендлинг своей команды для запуска бота.
    kb = [[KeyboardButton(text="Начать"), KeyboardButton(text="Задать ссылку"), KeyboardButton(text="Остановить")],]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
 
    await message.reply(f"Привет, {(message.from_user.full_name)}! Нажми 'Задать ссылку', а потом 'Начать', чтобы отслеживать форму.",
                        reply_markup=keyboard) 
    logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} вызвал команду mycommand")
    """

@form_router.message(F.text == "Начать")  
async def parser_form(message: Message):
    # Хендлинг команды "Начать". Парсинг формы.
    global URL_TEXT 
    global STOP_WHILE
    STOP_WHILE= True
    count = 0
    await message.answer("Начал отслеживать форму. Чтобы остановить процесс проверки и/или задать новую ссылку, сначала нажми 'Остановить.'")
    logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} вызвал команду 'Начать'.")
    while STOP_WHILE:
        interval = random.randint(1, 120)
        response = requests.get(URL_TEXT)
        bs = BeautifulSoup(response.text, "lxml")
        soup =  bs.find(class_="UatU5d")
        elem_soup = BeautifulSoup(str(soup), 'html.parser')
        elem_soup = elem_soup.text
        logger.info(f"Начало цикла: URL_TEXT = {URL_TEXT}, count = {count},  interval = {interval}, soup = {soup}, elem_soup = {elem_soup}")
        if soup and count == 0:  # Если сродержт тег и это первый запуск
            await message.answer(text=elem_soup)
            count = 1
            await asyncio.sleep(interval)
            logger.info(f"Первое условие: URL_TEXT = {URL_TEXT}, count = {count},  interval = {interval}, soup = {soup}, elem_soup = {elem_soup}")
            continue
        if soup and count == 1:  # Если содержит тег и это >= 2 запуску
            await asyncio.sleep(interval)
            logger.info(f"Второе условие: URL_TEXT = {URL_TEXT}, count = {count},  interval = {interval}, soup = {soup}, elem_soup = {elem_soup}")
            continue
        if not soup and count >= 0:  # Если не содержит тег 
            await message.answer("Ссылка формы изменила свой статус. Проверь ссылку{0}".format(URL_TEXT))
            count = 0
            logger.info(f"Третье условие: URL_TEXT = {URL_TEXT}, count = {count},  interval = {interval}, soup = {soup}, elem_soup = {elem_soup}")
            break

@form_router.message(F.text == "Остановить")  
async def parser_form(message: Message):
    # Хендлинг команды "Остановить"
    global STOP_WHILE
    STOP_WHILE = False
    await message.answer("Остановил проверку. Чтобы запустить, задай ссылку и нажми 'Начать'.")
    logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} вызвал команду 'Остановить'.")
    logger.info(f"STOP_WHILE = {STOP_WHILE}")
     
@form_router.message(F.text == "Задать ссылку")
async def start_url(message: Message, state: FSMContext):
    # Хендлинг "Задать ссылку". Отслеживание состояния url. 
    await state.set_state(FormUrl.url)
    await message.answer("Скопируй ссылку и отправь мне. Затем, нажми 'Начать'.")
    logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} вызвал команду 'Задать ссылку'.")

@form_router.message(FormUrl.url)
async def process_url(message: Message, state: FSMContext):
    # Форматирование из состояния url.
    global URL_TEXT
    url_text_local = await state.update_data(url=message.text)
    URL_TEXT = url_text_local['url']
    # Проверка валидности ссылки.
    try:
        check = requests.head(URL_TEXT)
        if check.status_code == 200:
            await message.answer("Принял ссылку.Нажми 'Начать'.")
            logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} ввёл валидную ссылку")
            logger.info(f"chek status code = {check.status_code}, url = {URL_TEXT}")
        else:
            await message.answer("Ссылка не валидна. Проверь ссылку и нажми 'Задать ссылку' снова.")
            logger.info(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} ввёл не валидную ссылку")
            logger.info(f"chek status code = {check.status_code}, url = {URL_TEXT}")
    except requests.exceptions.MissingSchema:
        await message.answer("Это не ссылка. Нажми 'Задать ссылку' снова. чтобы ввести правильный адрес.")
        logger.info(f"url = {URL_TEXT}")
        logger.exception(f"Пользователь id = {message.from_user.id} name = {(message.from_user.full_name)} ввёл не ссылку {requests.exceptions.MissingSchema}")
        

if __name__ == "__main__":
    asyncio.run(main())