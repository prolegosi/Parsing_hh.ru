import requests
import json
import pandas as pd
import sqlite3


# получение списка данных из API
def list_from_api(url, par=None):
    r = requests.get(url, params=par)
    out = json.loads(r.text)
    if type(out) == dict:
        out = out['items']
    return out

# Создание базы данных кодов регионов
def city_list(lst,name_table):
    try:
        con = sqlite3.connect('parser.db')
        cur = con.cursor()
    except :
        cur.close()
        print('Ошибка подключения к базе данных')


    try:
        cur.execute(f"""CREATE TABLE {name_table} (
        id INTEGER PRIMARY KEY,
        name TEXT
        )""")
    except sqlite3.OperationalError:
        print('Таблица уже создана')

    for i in lst:
        try:
            cur.execute(f"""INSERT INTO {name_table} VALUES ({int(i['id'])},'{i['name']}')""")
        except sqlite3.IntegrityError:
            print(f"Уже содержит {int(i['id'])},'{i['name']}'")

        for j in i['areas']:
            try:
                cur.execute(f"""INSERT INTO {name_table} VALUES ({int(j['id'])},'{j['name']}')""")
            except sqlite3.IntegrityError:
                print(f"Уже содержит {int(j['id'])},'{j['name']}'")

    con.commit()
    cur.close()

url_api = 'https://api.hh.ru/vacancies'
url_area = "https://api.hh.ru/areas/"

job = ["'python' and 'стажёр'"]

params = {'text': job, 'area': '113', 'per_page': '10'}

c = list_from_api(url_api, params)
d = list_from_api(url_area)

city_list(d, 'area')
