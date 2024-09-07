import time

import requests
from bs4 import BeautifulSoup
import re
import difflib
from loaders import bot, users_dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


town = {'Майкоп': '1', 'Барнаул': '2', 'Россия': '299', 'Благовещенск': '4', 'Архангельск': '5',
        'Астрахань': '7', 'Уфа': '8', 'Стерлитамак': '9', 'Белорецк': '10', 'Белгород': '11',
        'Старый Оскол': '12', 'Брянск': '13', 'Улан-Удэ': '14', 'Владимир': '15', 'Волгоград': '16',
        'Вологда': '17', 'Череповец': '18', 'Воронеж': '19', 'Махачкала': '20', 'Биробиджан': '21',
        'Чита': '22', 'Иваново': '23', 'Иркутск': '25', 'Калининград': '27', 'Калуга': '28',
        'Обнинск': '29', 'Петропавловск-Камчатский': '30', 'Черкесск': '31', 'Петрозаводск': '33',
        'Кемерово': '34', 'Киров': '35', 'Кирово-Чепецк': '36', 'Сыктывкар': '37', 'Ухта': '38',
        'Краснодар': '40', 'Сочи': '41', 'Новороссийск': '42', 'Анапа': '43', 'Геленджик': '44',
        'Красноярск': '45', 'Железногорск': '46', 'Норильск': '47', 'Курган': '48', 'Курск': '49',
        'Санкт-Петербург': '50', 'Выборг': '51', 'Сосновый Бор': '52', 'Липецк': '53', 'Елец': '54',
        'Магадан': '55', 'Саранск': '58', 'Москва': '59', 'Серпухов': '60', 'Электросталь': '61',
        'Дмитров': '62', 'Подольск': '63', 'Балашиха': '64', 'Химки': '65', 'Мурманск': '66',
        'Нижний Новгород': '67', 'Великий Новгород': '68', 'Новосибирск': '69', 'Омск': '70',
        'Оренбург': '71', 'Орск': '72', 'Орел': '73', 'Пенза': '74', 'Пермь': '75', 'Владивосток': '76',
        'Псков': '77', 'Ростов-на-Дону': '78', 'Таганрог': '79', 'Рязань': '80', 'Самара': '81',
        'Тольятти': '82', 'Екатеринбург': '83', 'Нижний Тагил': '84', 'Каменск-Уральск': '85',
        'Саратов': '86', 'Якутск': '87', 'Южно-Сахалинск': '88', 'Владикавказ': '89', 'Смоленск': '90',
        'Ставрополь': '91', 'Пятигорск': '92', 'Кисловодск': '93', 'Ессентуки': '94', 'Тамбов': '95',
        'Мичуринск': '96', 'Казань': '98', 'Набережные Челны': '99', 'Альметьевск': '100',
        'Нижнекамск': '101', 'Елабуга': '102', 'Тверь': '103', 'Конаково': '104', 'Ржев': '105',
        'Вышний Волочек': '106', 'Томск': '107', 'Тула': '109', 'Новомосковск': '110',
        'Нижневартовск': '112', 'Сургут': '113', 'Тюмень': '114', 'Ханты-Мансийск': '115',
        'Ижевск': '117', 'Ульяновск': '122', 'Хабаровск': '124', 'Абакан': '126', 'Саяногорск': '127',
        'Челябинск': '128', 'Магнитогорск': '129', 'Златоуст': '130', 'Грозный': '131', 'Чебоксары': '132',
        'Салехард': '134', 'Ярославль': '136', 'Севастополь': '593', 'Баку': '594', 'Душанбе': '595',
        'Нур-Султан (Астана)': '596', 'Ташкент': '597', 'Ереван': '598', 'Минск': '599', 'Буденновск': '600',
        'Симферополь': '601', 'Нальчик': '602', 'Йошкар-Ола': '603'
        }


def get_page(user_id):
    session = requests.Session()
    number_page = 0
    list_uni = []
    while True:
        number_page += 1
        url = 'https://vuzopedia.ru/region/city/{number_city}/poege/ege{first};ege{second};ege{third};?page={number_page}'.format(
            number_city=users_dict[user_id].town_id,
            first=users_dict[user_id].objects[0],
            second=users_dict[user_id].objects[1],
            third=users_dict[user_id].objects[2],
            number_page=number_page
            )
        try:
            response = session.get(url=url)
        except Exception as e:
            print(e)
        time.sleep(1)
        soup = BeautifulSoup(markup=response.text, features='lxml')
        ret = soup.find_all('div', class_="vuzesfullnorm")
        if ret == [] and number_page == 1:
            bot.send_message(user_id, 'Вузы по вашему запросу не найдены. Для повторного запроса /search')
            return False
        elif ret == [] and number_page != 1:
            users_dict[user_id].result = list_uni
            return True
        for elem in ret:
            try:
                # directions = elem.find('div', class_="clearfix opisItemVV").text.strip()
                # directions_in_dict = ''
                # for letter in directions:
                #     if letter == '\n':
                #         break
                #     directions_in_dict += letter
                i = 0
                lst_inf = elem.find_all('a', class_="tooltipq")

                if re.findall(r'\d+', lst_inf[2].text) == []:
                    min_free = 'нет'
                    count_free = 'нет'
                    i = 1
                else:
                    min_free = re.findall(r'\d+', lst_inf[2].text)[0]
                    count_free = re.findall(r'\d+', lst_inf[4].text)[0]
                data_univer = {elem.find('div', class_="itemVuzTitle").text.strip():
                        {'мин. стоимость': re.findall(r'\d+', lst_inf[0].text)[0],
                        'мин. бюджет': min_free,
                        'количество бюджетных мест': count_free,
                        'мин. суммарный проходной балл на платное': re.findall(r'\d+', lst_inf[5-i].text)[0],
                        'количество платных мест': re.findall(r'\d+', lst_inf[7-i].text)[0],
                        'номер вуза': elem.find('div', class_="forcheck wantabitNew").get('vuz')}}
                        #'направления': directions_in_dict}

                list_uni.append(data_univer)
            except IndexError as er:
                print('Минус один вуз')


def get_possible_town(town_from_user):
    lst_town = town.keys()
    search_town = difflib.get_close_matches(town_from_user, lst_town)
    if search_town == []:
        return False
    else:
        return search_town[0]


def get_specialties_uni(chat_id, user_id, message_id):
    number = users_dict[user_id].number_spec
    for specialties in users_dict[user_id].spec_lst[number].keys():
        text = 'Специальность: {specialties}\n\nМинимальный суммарный проходной балл на бюджет: {free_score}\n\n\
Количество бюджетных мест: {free_seats}\n\nМинимальный суммарный проходной балл на платное: от {paid_score}\n\n\
Количество платных мест: {paid_seats}\n\nСтоимость обучения (руб/год): {price} \n\nПодробнее о специальности: {href}'.format(
            specialties=specialties,
            free_score=users_dict[user_id].spec_lst[number][specialties]['free score'],
            free_seats=users_dict[user_id].spec_lst[number][specialties]['seats free'],
            paid_score=users_dict[user_id].spec_lst[number][specialties]['score paid'],
            paid_seats=users_dict[user_id].spec_lst[number][specialties]['seats paid'],
            price=users_dict[user_id].spec_lst[number][specialties]['price'],
            href=users_dict[user_id].spec_lst[number][specialties]['href']
        )
        spec_inline = InlineKeyboardMarkup()
        next_spec_button = InlineKeyboardButton(text='Следующая специальность', callback_data='next_spec')
        back_spec_button = InlineKeyboardButton(text='Предыдущая специальность', callback_data='back_spec')
        stop_buttons = InlineKeyboardButton(text='Вернуться к вузам', callback_data='back_to_uni')
        if len(users_dict[user_id].spec_lst) - 1 == number:
            spec_inline.add(back_spec_button)
            spec_inline.add(stop_buttons)
        elif number == 0:
            spec_inline.add(next_spec_button)
            spec_inline.add(stop_buttons)
        elif len(users_dict[user_id].spec_lst) == 1:
            spec_inline.add(stop_buttons)
        else:
            spec_inline.add(back_spec_button, next_spec_button)
            spec_inline.add(stop_buttons)
        print(users_dict[user_id].first_spec)
        if users_dict[user_id].first_spec is True:
            users_dict[user_id].last_message = bot.send_message(chat_id=chat_id, text=text, reply_markup=spec_inline)
            users_dict[user_id].first_spec = False
        else:
            users_dict[user_id].last_message = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=spec_inline)


def set_specialties_uni(user_id):
    i_name_spec = 0
    names_spec = []
    hrefs_specs = []
    specialties_uni = {}
    lst_uni_spec = []
    session = requests.Session()
    response = session.get(url=users_dict[user_id].link_specialization)
    soup = BeautifulSoup(markup=response.text, features='lxml')
    ret = soup.find_all('div', class_="col-md-2")
    names_of_specialization_soup = soup.find_all('div', class_='col-md-7 itemOsnInfoNewBlock')
    for name in names_of_specialization_soup:
        names_spec.append(name.find('a', class_='newItemSpPrTitle').text.strip())
        hrefs_specs.append(f"https://vuzopedia.ru{name.find('a', class_='linknap').get('href')}")
    print(len(names_spec), len(hrefs_specs))
    for specialization in ret:
        name = names_spec[i_name_spec]
        lst_score_place = specialization.find_all('a', class_='tooltipq')
        if len(lst_score_place) == 5:
            specialties_uni = {name: {
            'free score': '-',
            'seats free': '-',
            'price': re.findall(r'\d+', lst_score_place[0].text)[0],
            'seats paid': re.findall(r'\d+', lst_score_place[4].text)[0],
            'score paid': re.findall(r'\d+', lst_score_place[2].text)[0],
            'href': hrefs_specs[i_name_spec]
            }}
        elif len(lst_score_place) == 8 and re.findall(r'\d+', lst_score_place[2].text) == []:
            specialties_uni = {name: {
                'free score': '-',
                'seats free': re.findall(r'\d+', lst_score_place[4].text)[0],
                'price': re.findall(r'\d+', lst_score_place[0].text)[0],
                'seats paid': re.findall(r'\d+', lst_score_place[7].text)[0],
                'score paid': re.findall(r'\d+', lst_score_place[5].text)[0],
                'href': hrefs_specs[i_name_spec]
            }}
        elif len(lst_score_place) == 8:
            specialties_uni ={name: {
                'free score': re.findall(r'\d+', lst_score_place[2].text)[0],
                'seats free': re.findall(r'\d+', lst_score_place[4].text)[0],
                'price': re.findall(r'\d+', lst_score_place[0].text)[0],
                'seats paid': re.findall(r'\d+', lst_score_place[7].text)[0],
                'score paid': re.findall(r'\d+', lst_score_place[5].text)[0],
                'href': hrefs_specs[i_name_spec]
            }}
        i_name_spec += 1
        lst_uni_spec.append(specialties_uni)

    return lst_uni_spec



