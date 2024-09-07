import telebot
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

users_dict = {}


class User:
    def __init__(self):
        self.objects = []
        self.first_uni = True
        self.list_objects = ['математика', 'русский язык', 'обществознание', 'физика', 'история',
                             'информатика', 'биология', 'химия', 'география', 'литература',
                             'иностранный язык']
        self.user_id = None
        self.chat_id = None
        self.town_id = None
        self.message_id = None
        self.number_uni = 0
        self.result = None
        self.link_specialization = None
        self.number_spec = 0
        self.first_spec = True
        self.spec_lst = None
        self.last_message = None


items_ege = {'математика': 'mat', 'русский язык': 'rus','обществознание':'obsh','физика': 'fiz','история': 'ist',
             'информатика': 'inform','биология': 'biol','химия': 'him','география': 'georg','литература': 'liter',
             'иностранный язык': 'inyaz'
             }
