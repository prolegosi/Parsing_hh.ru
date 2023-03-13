import requests
import json
import sqlite3


# получение списка данных из API
def list_from_api(url, par=None):
    """

    :param url:
    :param par:
    :return:
    """
    r = requests.get(url, params=par)
    out = json.loads(r.text)
    if type(out) == dict and len(out) > 1:
        out = out['items']
    elif type(out) == dict and len(out) == 1:
        out = out['categories']
    return out

#функция получения списка скилов из списка вакансий
def skill_list(job_list):
    """

    :param job_list:
    :return:
    """
    skill_list = []
    for i in job_list:
        url = i['url']
        key_skills = requests.get(url)
        key_skills = json.loads(key_skills.text)
        lst = []
        for k in key_skills['key_skills']:
            lst.append(*k.values())
        if len(lst) > 0:
            skill_list.append(lst)

    return skill_list

# Создание базы данных кодов регионов
def create_table(lst, name_table):
    """

    :param lst:
    :param name_table:
    :return:
    """
    position = name_table
    # Исключение для списка профессий, данные c ip имеют немного разный формат
    if name_table == 'professional_roles':
        position = 'roles'

    try:
        con = sqlite3.connect('parser.db')
        cur = con.cursor()
    except:
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

        if name_table == 'professional_roles':
            position = 'roles'
        for j in i[position]:
            try:
                cur.execute(f"""INSERT INTO {name_table} VALUES ({int(j['id'])},'{j['name']}')""")
            except sqlite3.IntegrityError:
                print(f"Уже содержит {int(j['id'])},'{j['name']}'")

    con.commit()
    cur.close()


url_api = 'https://api.hh.ru/vacancies'
url_area = 'https://api.hh.ru/areas/'
url_prof = 'https://api.hh.ru/professional_roles/'
job = ["'python' and 'стажёр'"]
per_page = 5
params = {'text': job, 'area': '113', 'per_page': per_page}

if __name__ == '__main__':
    job_list = list_from_api(url_api, params)
    area_list = list_from_api(url_area)
    prof_list = list_from_api(url_prof)

    create_table(area_list, 'areas')
    create_table(prof_list, 'professional_roles')
    skills = skill_list(job_list)
    print(skills)



