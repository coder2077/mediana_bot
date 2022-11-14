import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
	debug: bool
	host: str
	password: str
	user: str
	database: str
	port: int

@dataclass
class TgBot:
	token: str
	channel_username: str

@dataclass
class Config:
	tgbot: TgBot
	db: DbConfig


def cast_bool(value: str) -> bool:
	if not value:
		return False
	return value.lower() in ("true", "t", "1", "yes")

def load_config(path: str = 'bot.ini'):
	config = configparser.ConfigParser()
	config.read(path)
	tgbot = config["tgbot"]

	return Config(
		tgbot=TgBot(
			token=tgbot["token"], 
			channel_username=tgbot["channel"]
		),
		db=DbConfig(**config["db"]),
	)

def make_db_uri():
	config = load_config("bot.ini")
	return f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}"

def get_file_path():
	# return "D://Projects/projects/mediana_project"
	return f"/root"
