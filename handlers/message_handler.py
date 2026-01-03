from typing import Final
from pathlib import Path
import os
from datetime import datetime
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram import F
from helpers.link_extracter import split_link
import yt_dlp
from config import *

router: Final[Router] = Router(name=__name__)

supported_domains: list[str] = [
    "www.youtube.com",
    "youtube.com",
    "youtu.be",
    "vt.tiktok.com",
    "www.instagram.com",
    "instagram.com"
]

@router.message(F.text)
async def cmd_link_export(message: Message):
    link: str = (message.text or "").strip()
    if not link:
        return

    domain = split_link(link)
    if domain not in supported_domains:
        await message.answer(UNRECOGNIZED_LINK)
        return

    await message.answer(DOWNLOADING_START)

    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = f"video_{timestamp}"
    output_path = downloads_dir / f"{safe_title}.%(ext)s"

    try:
        ydl_opts = {
            'format': 'best[height<=720]/best',
            'outtmpl': str(output_path),
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl: #type: ignore
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'Unknown') or 'Unknown'
            duration = info_dict.get('duration', 0) or 0
            uploader = info_dict.get('uploader', 'Unknown') or 'Unknown'
            duration_str = f"{duration//60}:{duration%60:02d}"

            await message.answer(
                f"📹 **{title}**\n"
                f"👤 {uploader}\n"
                f"⏱ {duration_str}\n"
                f"💾 Скачиваю..."
            )

            ydl.download([link])

        downloaded_files = list(downloads_dir.glob(f"{safe_title}.*"))
        if not downloaded_files:
            await message.answer(FILE_NOT_FOUND)
            return

        file_path = max(downloaded_files, key=os.path.getctime)

        if file_path.exists() and file_path.stat().st_size > 0:
            await message.answer_video(
                FSInputFile(file_path),
                caption=f"✅ {title[:100]}..."
            )
        else:
            await message.answer(EMPTY_FILE)
            file_path = None

    except Exception as e:
        await message.answer(
            ERROR_DOWNLOADING.format(error=str(e)[:500]),
            parse_mode="Markdown"
        )
        file_path = None

    finally:
        if 'file_path' in locals() and file_path and file_path.exists():
            file_path.unlink()