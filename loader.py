from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from config import *
from start_database import Session

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

storage = MemoryStorage()

session = Session()
bot = Bot(token=Bot_token)
dp = Dispatcher(bot, storage=storage)
