import os
from pathlib import Path

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import settings
from stt import STT
from request_factory import *
from utils import *
from speach import *

bot = Bot(token=settings.token)
dp = Dispatcher(bot)

stt = STT()

@dp.message_handler(commands=['start'])
async def procces_start(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Добро пожаловать в дипломную работу за виски или крутой стаф")
    await bot.send_message(message.chat.id,
                           "Я типа умеею тебя слушать, отправь мне голосовое чел")
    
@dp.message_handler(content_types=['voice'])
async def procces_voice(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(message.voice.file_id)
    file_path = file.file_path
    file_on_disk = Path("", f"{file_id}.tmp")
    await bot.download_file(file_path, destination=file_on_disk)
    await message.reply("Аудио получено")

    text = stt.audio_to_text(file_on_disk)
    if not text:
        text = "Формат документа не поддерживается"

    if check_words_in_list(text, settings.picture):
        image_url = get_image(text)
        await message.answer(image_url)
    
    if check_words_in_list(text, settings.trans):
        resp = translate(replace_words(text, settings.trans))
        await message.answer(resp)

    if check_words_in_list(text, settings.query):
        resp = gtp(replace_words(text, settings.query))
        await message.answer(resp)
        
    await message.answer(text)

    os.remove(file_on_disk)  

@dp.message_handler()
async def procces_speach(message: types.Message):
    speach(message.text)
    time.sleep(2)
    await message.reply_audio(audio=open("test.mp3", "rb"))

@dp.message_handler(commands=['help'])
async def procces_help(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Спроси у меня про перевод я переведу на англ")
    await bot.send_message(message.chat.id,
                           "Скажи покажи и я найду картинку")
    await bot.send_message(message.chat.id,
                           "Напиши мне какую-нибудь дичь и я озвучу")

if __name__ == '__main__':
    executor.start_polling(dp)