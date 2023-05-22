from aiogram import Bot
from database_launcher import Database_launcher
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from config import *

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

storage = MemoryStorage()
db = Database_launcher(
            database=database_name,
            user=database_user,
            password=database_password,
            host=database_host,
            port=database_port
)
bot = Bot(token=Bot_token)
dp = Dispatcher(bot, storage=storage)
