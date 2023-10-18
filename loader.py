import logging
from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *
from start_database import Session

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)

# storage = MemoryStorage()

session = Session()
logging.info('Database connect successfully')

bot = Bot(token=Bot_token)

dp = Dispatcher()
