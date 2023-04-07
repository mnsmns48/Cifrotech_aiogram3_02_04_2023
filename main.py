import asyncio

from bot import bot, dp
from commands import commands
from core import update_shippers_data
from handlers.user import register_user_handlers


async def main():
    update_shippers_data()
    register_user_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('BOT Stopped')
