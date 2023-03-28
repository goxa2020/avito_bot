from aiogram import Bot
from sqlighter import Sqlighter
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import config

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

storage = MemoryStorage()
db = Sqlighter("database.db")
bot = Bot(token=config.Bot_token)
dp = Dispatcher(bot, storage=storage)
