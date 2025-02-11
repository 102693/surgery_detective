import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, FSInputFile, InlineKeyboardButton, CallbackQuery, InputFile
from config import BOT_TOKEN
from downloader import download_video

# Логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопка доната
donate_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💰 Поддержать", url="https://boosty.to/your_link")]
    ]
)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Отправь ссылку на YouTube, и я помогу скачать аудио или видео 🎵📹", 
                         reply_markup=donate_keyboard)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Отправь мне ссылку на видео с YouTube, и я предложу варианты скачивания.")

@dp.message()
async def handle_url(message: types.Message):
    if "youtube.com" in message.text or "youtu.be" in message.text:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🎵 Скачать MP3", callback_data=f"audio:{message.text}")],
                [InlineKeyboardButton(text="📹 Скачать MP4", callback_data=f"video:{message.text}")]
            ]
        )
        await message.answer("Выберите формат:", reply_markup=keyboard)
    else:
        await message.answer("Это не похоже на ссылку с YouTube. Попробуй ещё раз!")

@dp.callback_query()
async def process_download(call: CallbackQuery):
    format_type, url = call.data.split(":", 1)
    await call.message.answer(f"⏳ Скачиваю {format_type}...")
    
    try:
        file_path = await download_video(url, format_type)
        
        # Создаем объект FSInputFile из пути к файлу
        file_input = FSInputFile(file_path)
        
        if format_type == "audio":
            await call.message.answer_audio(file_input)
        else:
            await call.message.answer_video(file_input)
        
        # Удаляем файл после отправки
        os.remove(file_path)
    except Exception as e:
        await call.message.answer("❌ Ошибка при скачивании.")
        logging.error(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
