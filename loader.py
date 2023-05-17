from aiogram import Bot
from database_launcher import Database_launcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import config

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

storage = MemoryStorage()
db = Database_launcher(
            database='mydb',
            user='pyuser',
            password='1111',
            host='127.0.0.1',
            port='5432'
)
bot = Bot(token=config.Bot_token)
dp = Dispatcher(bot, storage=storage)
