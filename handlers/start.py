from typing import Final

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import WELCOME_MSG

router: Final[Router] = Router(name=__name__)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(WELCOME_MSG)
