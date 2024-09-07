import time
from info_on_universities import get_specialties_uni, set_specialties_uni
from loaders import bot, users_dict, User, items_ege
import emoji
from handlers import get_inline_objects, get_town_university, get_result


@bot.message_handler(commands=['start'])
def start_message(message):
    school = emoji.emojize(':school:')
    arrow = emoji.emojize(':backhand_index_pointing_right:')
    users_dict[message.from_user.id] = User()
    bot.send_message(message.chat.id, f'Приветствую!\n Я бот для поиска вузов по России {school}\n\
Для начала поиска нажмите сюда {arrow} /search')
    users_dict[message.from_user.id].user_id = message.from_user.id
    users_dict[message.from_user.id].chat_id = message.chat.id


@bot.message_handler(commands=['search'])
def start_search(message):
    time.sleep(1)
    users_dict[message.from_user.id].firsr_spec = True
    users_dict[message.from_user.id].objects = []
    users_dict[message.from_user.id].first_uni = True
    users_dict[message.from_user.id].town_id = None
    users_dict[message.from_user.id].number_uni = 0
    get_inline_objects(message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call:
        if call.data == 'next_uni':
            users_dict[call.from_user.id].number_uni += 1
            users_dict[call.from_user.id].message_id = call.message.id
            get_result(user_id=call.from_user.id, chat_id=call.message.chat.id)
        elif call.data == 'back_uni':
            users_dict[call.from_user.id].number_uni -= 1
            users_dict[call.from_user.id].message_id = call.message.id
            get_result(user_id=call.from_user.id, chat_id=call.message.chat.id)
        elif call.data == 'stop':
            bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
            users_dict[call.from_user.id].flag_for_for = False
            bot.send_message(chat_id=call.message.chat.id, text='Для начала поиска вуза нажмите сюда /search')
        elif call.data == 'specialization':
            bot.delete_message(chat_id=call.message.chat.id, message_id=users_dict[call.from_user.id].last_message.message_id)
            users_dict[call.from_user.id].first_uni = True
            message_waiting = bot.send_message(chat_id=call.message.chat.id, text='Пожалуйста подождите, загружаю данные')
            users_dict[call.from_user.id].spec_lst = set_specialties_uni(user_id=call.from_user.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=message_waiting.id)
            users_dict[call.from_user.id].number_spec = 0
            get_specialties_uni(chat_id=call.message.chat.id, user_id=call.from_user.id, message_id=call.message.id)
        elif call.data == 'next_spec':
            users_dict[call.from_user.id].number_spec += 1
            get_specialties_uni(chat_id=call.message.chat.id, user_id=call.from_user.id, message_id=call.message.id)
        elif call.data == 'back_spec':
            users_dict[call.from_user.id].number_spec -= 1
            get_specialties_uni(chat_id=call.message.chat.id, user_id=call.from_user.id, message_id=call.message.id)
        elif call.data == 'back_to_uni':
            bot.delete_message(chat_id=call.message.chat.id, message_id=users_dict[call.from_user.id].last_message.message_id)
            users_dict[call.from_user.id].first_spec = True
            get_result(user_id=call.from_user.id, chat_id=call.message.chat.id)
        else:
            users_dict[call.from_user.id].objects.append(items_ege[call.data])
            bot.delete_message(message_id=call.message.id,chat_id=call.message.chat.id)
            if len(users_dict[call.from_user.id].objects) != 3:
                get_inline_objects(call.from_user.id)
            elif len(users_dict[call.from_user.id].objects) == 3:
                bot.send_message(call.message.chat.id, 'Введите название города')
                bot.register_next_step_handler(call.message, get_town_university)


if __name__ == '__main__':
    print('Бот готов к работе')
    bot.polling(none_stop=True, timeout=1)


