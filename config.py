from dataclasses import dataclass
from environs import Env


@dataclass
class MiscPath:
    photo_path: str
    yadisk: str


@dataclass
class DbConfig:
    dsn: str
    user: str
    password: str


@dataclass
class MailConnect:
    mailbox: str
    mail_pass: str
    mail_path: str
    subject_keywords: str


@dataclass
class TgBot:
    bot_token: str
    admin_id: list[int]


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc_path: MiscPath
    mail_connect: MailConnect


def load_config(path: str = None):
    env = Env()
    env.read_env()

    return Config(
        tg_bot=TgBot(
            bot_token=env.str("BOT_TOKEN"),
            admin_id=list(map(int, env.list("ADMIN_ID"))),
        ),
        db=DbConfig(
            dsn=env.str('DB_DSN'),
            user=env.str('DB_USER'),
            password=env.str('DB_PASSWORD'),
        ),
        misc_path=MiscPath(
            photo_path=env.str("PHOTO_PATH"),
            yadisk=env.str("YATOKEN"),
        ),
        mail_connect=MailConnect(
            mailbox=env.str("MAIL_BOX"),
            mail_pass=env.str("MAIL_PASS"),
            mail_path=env.str("MAIL_PATH"),
            subject_keywords=env.str("SUBJECT_KEYWORDS"),
        ),
    )


hidden_vars = load_config('..env')
