from aiogram import Bot, Dispatcher, types


bot = Bot("")

dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":    
    dp.run_polling(bot)