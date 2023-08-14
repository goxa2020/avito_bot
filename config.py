__all__ = ('Bot_token', 'yookassa_token', 'Bot_name', 'chanel_name', 'chanel_id', 'no_photo_id',
           'database_name', 'database_user', 'database_password', 'database_host', 'database_port')
from dotenv import load_dotenv
import os

load_dotenv('ignore/.env')

Bot_token = os.getenv('TOKEN')
yookassa_token = os.getenv('YOOKASSA_TOKEN')
Bot_name = 'testtikk_bbot'
chanel_name = '@ttttttttesst'
chanel_id = os.getenv('CHANEL_ID')
no_photo_id = os.getenv('PHOTO_ID')
database_name = os.getenv('DATABASE_NAME')
database_user = os.getenv('DATABASE_USER_NAME')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')
# I love u very much
