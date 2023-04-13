import asyncio

from bot import bot, dp
from commands import commands
from distrib_mail_parsing import mail_parsing
from handlers.user import register_user_handlers


async def bot_working():
    register_user_handlers()
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


async def main():
    bot_task = asyncio.create_task(bot_working())
    mail_monitoring_task = asyncio.create_task(mail_parsing())
    await asyncio.gather(bot_task, mail_monitoring_task)


if __name__ == '__main__':
    try:
        print('Начало работы бота')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('BOT Stopped')
