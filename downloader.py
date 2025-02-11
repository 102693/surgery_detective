import yt_dlp
import asyncio
import os

# Папка для скачанных файлов
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def download_video(url: str, format: str) -> str:
    """
    Скачивает видео или аудио с YouTube с использованием куки из браузера.
    :param url: ссылка на YouTube-видео
    :param format: 'video' или 'audio'
    :return: путь к скачанному файлу
    """
    loop = asyncio.get_running_loop()
    
    # Опции для yt-dlp
    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": True,
        # Добавляем автоматическое извлечение куки из браузера (например, Chrome)
        "cookies_from_browser": "chrome",
        # Если у тебя другой браузер, например, firefox или edge, укажи его название
    }
    
    if format == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts.update({"format": "best[ext=mp4]/best"})
    
    def run_yt_dlp():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    
    file_path = await loop.run_in_executor(None, run_yt_dlp)
    
    if format == "audio":
        file_path = file_path.rsplit(".", 1)[0] + ".mp3"
    
    return file_path
