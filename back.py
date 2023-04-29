import requests
import json
import sqlite3
import textdistance



def list_from_api(url, par=None):
    """
    Функция получает список данных из API

    :param url: адрес hh.ru API
        url_api = 'https://api.hh.ru/vacancies' - адрес вакансий
        url_area = 'https://api.hh.ru/areas/'   - адрес регионов
        url_prof = 'https://api.hh.ru/professional_roles/' - адрес профессий
    :param par: параметры запроса
    :return: возвращает ответ API в виде словаря в списке
    """
    req = requests.get(url, params=par)
    out = json.loads(req.text)
    if type(out) == dict and len(out) > 1:
        out = out['items']
    elif type(out) == dict and len(out) == 1:
        out = out['categories']
    return out


def skill_list(job_list):
    """
    Функция принимает список полученный из API (функция list_from_api())

    :param job_list: список результат работы функции list_from_api()
    :return: возвращает список ключевых навыков
    """
    skill_list = []
    for i in job_list:
        url = i['url']
        key_skills = requests.get(url)
        #print(key_skills.raise_for_status())
        key_skills = json.loads(key_skills.text)
        lst = []
        for k in key_skills['key_skills']:
            lst.append(*k.values())
        if len(lst) > 0:
            skill_list.append(lst)

    return skill_list


def create_table(lst, name_table):
    """
    Создаёт таблицу на основе профессий и регионов из API

    :param lst: список из функции list_from_api()
    :param name_table: имя таблицы
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
        con.close()
        print('Ошибка подключения к базе данных')

    try:
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {name_table} (
        id INTEGER PRIMARY KEY,
        name TEXT
        )""")
    except sqlite3.OperationalError:
        print('Таблица уже создана')

    for i in lst:
        try:
            cur.execute(f"""INSERT INTO {name_table} VALUES ({int(i['id'])},'{i['name'].lower()}')""")
        except sqlite3.IntegrityError:
            print(f"Уже содержит {int(i['id'])},'{i['name']}'")

        if name_table == 'professional_roles':
            position = 'roles'
        for j in i[position]:
            try:
                cur.execute(f"""INSERT INTO {name_table} VALUES ({int(j['id'])},'{j['name'].lower()}')""")
            except sqlite3.IntegrityError:
                print(f"Уже содержит {int(j['id'])},'{j['name']}'")

    con.commit()
    cur.close()
    con.close()


def sort_skill_dict(s_dict):
    """
        Сортирует словарь по уменьшению значения
        Также обрезает словарь до 20-ти элементов
    :param s_dict: словарь
    :return: словарь отсортированный по убыванию
    """
    skill_dict = {}
    for i in s_dict:
        for j in i:
            if skill_dict.get(j) is None:
                skill_dict.setdefault(j, 1)
            else:
                skill_dict[j] += 1

    sort_dict = sorted(skill_dict.items(), key=lambda x: x[1])
    sort_dict = dict(sort_dict[::-1])
    if len(sort_dict) > 10:
        sort_dict = dict(tuple(sort_dict.items())[:10])
    return sort_dict


def count_validation(area_name):
    """
        Функция обрабатывает введённый пользователем регион по косинусному сходству
        в соответствии с табилцей доступных регионов и в случае если косниунсное сходство более 0,7
        возвращает название региони и его id для параметров API

    :param area_name: ввод пользователя содержащий название региона
    :return: возвращает кортеж первое значение строка - название региона
            второе значение id региона, для параметров API, если коснусное содство < 0,7
            в первым агрументом возвращается сообщение о неточном вводе, вторым False
    """
    area_name = area_name.lower()
    if area_name.count(' '):
        area_name = area_name.strip()
    try:
        con = sqlite3.connect('parser.db')
        cur = con.cursor()
        cur.execute("""SELECT name FROM areas""")
        count_list = cur.fetchall()
        cur.close()
        con.close()
    except:
        print('Ошибка базы данных')
        cur.close()
        con.close()
    max_cos_similarity = (0, '')
    for area in count_list:
        text_siml = textdistance.jaccard(area_name, area[0])

        if text_siml > max_cos_similarity[0]:
            max_cos_similarity = text_siml, area[0]

    if max_cos_similarity[0] < 0.7:
        return 'Уточните название региона', False
    else:
        try:
            con = sqlite3.connect('parser.db')
            cur = con.cursor()
            cur.execute(f"""SELECT id FROM areas
                            WHERE name = '{max_cos_similarity[1]}';""")
            count_id = cur.fetchall()
            cur.close()
            con.close()
        except:
            print('Ошибка базы данных')
            cur.close()
            con.close()
        return max_cos_similarity[1].capitalize(), count_id[0][0]


def job_processing(prof_input_str):
    """
    Собирает JSON строку
    :param prof_input_str: строка, в которой слова разделены пробелами
    :return: строка вида 'word_1' and 'word_2'...
    """
    prof_input_str = prof_input_str.strip()
    prof_lst = prof_input_str.lower().split()
    # Сборка форматированной строки
    out = ["'" + x + "'" + ' ' + 'and' if prof_lst.index(x) != len(prof_lst) - 1 else "'" + x + "'" for x in prof_lst]
    out = ' '.join(out)
    return out



url_api = 'https://api.hh.ru/vacancies'
url_area = 'https://api.hh.ru/areas/'
url_prof = 'https://api.hh.ru/professional_roles/'

job = ["'frontend' and 'junior'"]
per_page = 10
params = {'text': job, 'area': '113', 'per_page': per_page}

if __name__ == '__main__':
    print('Working')

    #area, area_id = count_validation(string)
    job_list = list_from_api(url_api, params)
    # area_list = list_from_api(url_area)
    # prof_list = list_from_api(url_prof)

    #create_table(area_list, 'areas')
    #create_table(prof_list, 'professional_roles')

    skills = skill_list(job_list)
    #print(skills)
    skill_dict = sort_skill_dict(skills)
    print(skill_dict)
    #print(area, area_id)
    #print(job_processing(string))
