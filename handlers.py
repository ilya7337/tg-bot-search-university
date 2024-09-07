from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loaders import bot, users_dict, items_ege
from info_on_universities import get_possible_town, town, get_page


def get_inline_objects(user_id):
    list_objects = users_dict[user_id].list_objects
    inline_objects = InlineKeyboardMarkup()
    for elem in list_objects:
        if items_ege[elem] not in users_dict[user_id].objects:
            inline_objects.add(InlineKeyboardButton(text=elem, callback_data=elem))
    bot.send_message(users_dict[user_id].chat_id, 'Выберите предметы по которым Вы хотите поступать:',
                     reply_markup=inline_objects)


def get_town_university(message):
    search_town = get_possible_town(message.text)
    if search_town:
        bot.send_message(message.chat.id, f'Ищу вузы в городе {search_town}')
        users_dict[message.from_user.id].town_id = town[search_town]
        if get_page(message.from_user.id):
            get_result(user_id=message.from_user.id, chat_id=message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Извините, такого города нет в моей базе. Попробуйте ввести другой город: ')
        bot.register_next_step_handler(message, get_town_university)


def get_result(user_id, chat_id):
    text = ''
    lst_inf_uni = get_inf_uni(user_id)
    text = lst_inf_uni[0]
    users_dict[user_id].link_specialization = lst_inf_uni[1]
    university_inline = InlineKeyboardMarkup()
    next_uni_button = InlineKeyboardButton(text='Следующий вуз', callback_data='next_uni')
    back_uni_button = InlineKeyboardButton(text='Предыдущий вуз', callback_data='back_uni')
    specialization_button = InlineKeyboardButton(text='Посмотреть специальности', callback_data='specialization')
    if users_dict[user_id].number_uni == 0:
        university_inline.add(next_uni_button)
        print(len(users_dict[user_id].result))
    elif users_dict[user_id].number_uni == len(users_dict[user_id].result)-1:
        university_inline.add(back_uni_button)
    else:
        university_inline.add(back_uni_button, next_uni_button)
    university_inline.add(specialization_button)
    university_inline.add(InlineKeyboardButton(text='Остановить поиск', callback_data='stop'))
    if users_dict[user_id].first_uni:
        users_dict[user_id].last_message = bot.send_message(chat_id=chat_id, text=text, reply_markup=university_inline)
        users_dict[user_id].first_uni = False
    else:
        users_dict[user_id].last_message = bot.edit_message_text(chat_id=chat_id, message_id=users_dict[user_id].message_id,
                              reply_markup=university_inline, text=text)



def get_inf_uni(user_id):
    text = None
    result = users_dict[user_id].result[users_dict[user_id].number_uni]
    for elem in result.keys():
        link = f'https://vuzopedia.ru/vuz/{result[elem]["номер вуза"]}/poege/ege{users_dict[user_id].objects[0]};\
ege{users_dict[user_id].objects[1]};ege{users_dict[user_id].objects[2]};'
        text = 'Название вуза: {name}\n\nМинимальный суммарный проходной балл на бюджет по вузу: {min_budget_score}\n\n\
Количество бюджетных мест по вузу: {budget_seats}\n\nМинимальный суммарный проходной балл на платное по вузу: {min_paid}\n\n\
Количество платных мест по вузу: {paid_seats}\n\nПодробнее о вузе: {link}'.format(name=elem,
                                            min_budget_score=result[elem]['мин. бюджет'],
                                            budget_seats=result[elem]['количество бюджетных мест'],
                                            link=link,
                                            min_paid=result[elem]['мин. суммарный проходной балл на платное'],
                                            paid_seats=result[elem]['количество платных мест']
                                            )
        return [text, link]
