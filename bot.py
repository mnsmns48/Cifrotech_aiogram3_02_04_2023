import logging

from aiogram import Bot, Dispatcher

from config import hidden_vars

bot = Bot(token=hidden_vars.tg_bot.bot_token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)
