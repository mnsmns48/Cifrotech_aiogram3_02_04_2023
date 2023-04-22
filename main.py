import asyncio

from bot import bot, dp
from commands import commands

from distrib_mail_parsing import mail_parsing

from handlers.admin import register_admin_handlers, admin_
from handlers.user import register_user_handlers, user_


async def bot_working():
    register_admin_handlers()
    register_user_handlers()
    dp.include_routers(admin_, user_)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    finally:
        await bot.session.close()


async def main():
    bot_task = asyncio.create_task(bot_working())
    mail_monitoring_task = asyncio.create_task(mail_parsing())
    await asyncio.gather(bot_task, mail_monitoring_task)


if __name__ == '__main__':
    try:
        print('Bot went to work')
        print('Checking mail: Cifrotechmobile@inbox.ru')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot Stopped')
