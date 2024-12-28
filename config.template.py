from aiogram import Bot, Dispatcher, Router

TOKEN_TG = "token"

# Инициализация бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher()
router = Router()

DB_NAME = "postgres"
DB_PORT = 5440
DB_PASSWORD = "postgres"
DB_USER = "postgres"
DB_HOST = "postgres"

NoneData = ""
