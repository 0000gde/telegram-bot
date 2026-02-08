import asyncio
import os
import re
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import yt_dlp

BOT_TOKEN = "8171518783:AAE_1nLtFHicpYV3sOGjp37gj1vuzFh80h0"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Кинь ссылку.")


def is_supported_link(text: str) -> bool:
    return bool(re.search(r"(tiktok\.com|instagram\.com)", text))


def download_video(url: str) -> str:
    filename = os.path.join(DOWNLOAD_DIR, f"{uuid.uuid4()}.mp4")

    ydl_opts = {
        "format": "bv*[height<=720][ext=mp4]+ba[ext=m4a]/mp4",
        "outtmpl": filename,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


@dp.message()
async def handle_link(message: types.Message):
    text = message.text.strip()

    if not is_supported_link(text):
        return

    try:
        video_path = download_video(text)
        await message.answer_video(FSInputFile(video_path))
    except Exception:
        await message.answer("Ошибка при обработке ссылки.")
    finally:
        if "video_path" in locals() and os.path.exists(video_path):
            os.remove(video_path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

