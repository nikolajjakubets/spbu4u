# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hmac
from collections import OrderedDict
from datetime import timedelta
from hashlib import sha256

from app import app

sha_string = hmac.new(bytearray(app.config['SECRET_KEY'], "utf-8"),
                      bytearray(app.config['OTHER_SECRET_KEY'], "utf-8"),
                      sha256).hexdigest()

ids = {
    "my": 200466757,
    "ks": 71591548
}

webhook_host = ""
webhook_port = 443
webhook_url_base = "https://{0}:{1}".format(webhook_host, webhook_port)
webhook_url_path = "/{0}/".format(sha_string)

max_inline_button_text_len = 32

server_timedelta = timedelta(hours=0)

urls = {
    "ya_search": "https://api.rasp.yandex.net/v3.0/search/"
}

emoji = {"info": "\U00002139", "star": "\U00002B50",
         "settings": "\U00002699", "suburban": "\U0001F689",
         "editor": "\U0001F4DD", "alarm_clock": "\U000023F0",
         "calendar": "\U0001F4C5", "sleep": "\U0001F634",
         "clock": "\U0001F552", "cross_mark": "\U0000274C",
         "check_mark": "\U00002705", "mailbox_off": "\U0001F4EA",
         "mailbox_on": "\U0001F4EB", "door": "\U0001F6AA",
         "school": "\U0001F3EB", "disappointed": "\U0001F61E",
         "cold_sweat": "\U0001F613", "halo": "\U0001F607",
         "smile": "\U0001F604", "bullet": "\U00002022",
         "horns": "\U0001F608", "orange_diamond": "\U0001F538",
         "blue_diamond": "\U0001F539", "runner": "\U0001F3C3",
         "arrow_up": "\U00002B06", "warning": "\U000026A0",
         "arrows_counterclockwise": "\U0001F504",
         "bust_in_silhouette": "\U0001F464", "back": "\U0001F519",
         "mag_right": "\U0001F50E", "arrow_backward": "\U000025C0",
         "arrow_forward": "\U000025B6", "star2": "\U00002728",
         "new": "\U0001F195", "prev_block": "\U00002B05",
         "next_block": "\U000027A1", "Отмена": "Отмена",
         "heavy_check_mark": "\U00002705", "ruble_sign": "\U000020BD",
         "train": "\U0001F683", "express": "\U0001F684",
         "en_dash": "\U00002013", "couch_and_lamp": "\U0001F6CB",
         "books": "\U0001F4DA"}

week_day_number = OrderedDict([
    ("Пн", 1), ("Вт", 2), ("Ср", 3), ("Чт", 4), ("Пт", 5), ("Сб", 6)
])

week_day_titles = OrderedDict([
    ("Понедельник", "Пн"), ("Вторник", "Вт"), ("Среда", "Ср"),
    ("Четверг", "Чт"), ("Пятница", "Пт"), ("Суббота", "Сб")
])

subject_short_type = OrderedDict([
    ("лекция", "Л"), ("практическое занятие", "ПР"), ("сам. работа", "СР"),
    ("семинар", "С"), ("урок", "У"), ("лабораторная работа", "ЛР"),
    ("контрольная работа", "КР"), ("показ работ", "ПОКАЗ РАБОТ"),
    ("текущий контроль", "ТК"), ("зачёт", "ЗАЧЁТ"),
    ("зачёт (пересдача)", "ЗАЧЁТ (ПЕР.)"), ("консультация групповая", "КОНС"),
    ("экзамен", "ЭКЗАМЕН"), ("экзамен (пересдача)", "ЭКЗАМЕН (ПЕР.)")
])

all_stations = OrderedDict([
    ("Санкт-Петербург", "c2"), ("Броневая", "s9603500"),
    ("Ленинский Проспект", "s9603435"), ("Дачное", "s9603596"),
    ("Ульянка", "s9603532"), ("Лигово", "s9603837"),
    ("Сосновая Поляна", "s9603431"), ("Сергиево (Володарская)", "s9603567"),
    ("Стрельна", "s9603542"), ("Красные Зори", "s9603483"),
    ("Новый Петергоф", "s9603887"), ("Старый Петергоф", "s9603547"),
    ("Университетская (Университет)", "s9603770"), ("Мартышкино", "s9603619"),
    ("Ораниенбаум-1", "s9603138"), ("Лебяжье", "s9602688"),
    ("Калище", "s9602687")
])

months = OrderedDict([
    ("января", 1), ("февраля", 2), ("марта", 3), ("апреля", 4), ("мая", 5),
    ("июня", 6), ("июля", 7), ("августа", 8), ("сентября", 9), ("октября", 10),
    ("ноября", 11), ("декабря", 12)
])

months_date = OrderedDict([
    (1, "Январь"), (2, "Февраль"), (3, "Март"), (4, "Апрель"), (5, "Май"),
    (6, "Июнь"), (7, "Июль"), (8, "Август"), (9, "Сентябрь"), (10, "Октябрь"),
    (11, "Ноябрь"), (12, "Декабрь")
])

loading_text = {
    "schedule": [
        "Загружаю", "Смотрю расписание", "Подождите, пожалуйста", "Ищу занятия",
        "Загружаю пары", "Жду ответ от сервера", "Сейчас спрошу у кого-нибудь"
    ],
    "ya_timetable": [
        "Загружаю", "Смотрю расписание", "Подождите, пожалуйста",
        "Жду ответ от сервера", "Смотрю на rasp.yandex.ru"
    ]
}

briefly_info_answer = \
    'КРАТКАЯ ИНФОРМАЦИЯ\n\n' \
    '<b>Раздел "Расписание"</b>\n' \
    'Здесь ты можешь <i>узнать расписание</i> на любой день, а также ' \
    '<i>подписаться на рассылку</i>.\n\n' \
    '<b>Раздел "{}"</b>\n' \
    'Здесь ты можешь <i>сменить группу</i> или <i>завершить работу</i> с ' \
    'ботом.\n\n' \
    '<b>Раздел "{}"</b>\n' \
    'Здесь ты можешь <i>оценить бота</i> и посмотреть <i>средний балл</i> ' \
    'оценок пользователей.\n\n' \
    '<b>Раздел "{}"</b>\n' \
    'Здесь ты можешь <i>скрыть</i> или <i>вернуть</i> занятие в расписании, ' \
    'а также настроить <i>отображение адреса</i>.\n\n' \
    '<b>Раздел "{}"</b>\n' \
    'Здесь ты можешь посмотреть <i>электрички</i> от или до Университета. ' \
    'Также есть возможность проложить <i>свой маршрут</i>.'.format(
        emoji["settings"], emoji["star"], emoji["editor"], emoji["suburban"])

special_thanks = \
    'ОСОБАЯ БЛАГОДАРНОСТЬ\n\n' \
    '@SuaiBot - идейный вдохновитель\n' \
    '<a href="https://rasp.yandex.ru">Яндекс.Расписания</a> - ' \
    '<a href="https://tech.yandex.ru/rasp/raspapi/">бесплатный API</a> ' \
    'для доступа к расписаниям электричек\n' \
    '<a href="https://it.spbu.ru">УСИТ СПбГУ</a> - предоставление ' \
    '<a href="https://timetable.spbu.ru/help">API</a> для доступа к ' \
    '<a href="https://timetable.spbu.ru">расписаниям занятий СПбГУ</a>\n'

weekend_answer = emoji["sleep"] + " Выходной"
