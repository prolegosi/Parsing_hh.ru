import back
import os
from matplotlib import pyplot as plt

while True:

    country = input('Введите название региона\n'
                    'например: московская область; россия\n'
                    ':')
    area, area_id = back.count_validation(country)
    if not area_id:
        print(area)
        continue

    os.system('cls||clear')
    jobs_string_input = input('Введите ключевые слова проффессии через пробел '
                        '\nнапример: python junior удалённо\n'
                        ':')
    jobs_string = back.job_processing(jobs_string_input)

    per_page = 5
    params = {'text': jobs_string, 'area': '113', 'per_page': per_page}
    job_list = back.list_from_api(back.url_api, params)
    skills = back.skill_list(job_list)

    skill_dict = back.sort_skill_dict(skills)

    labels = tuple(skill_dict.keys())
    explode = tuple(x / 50 for x in skill_dict.values())
    print(jobs_string_input)
    colors = ['#80302f', '#b84739', '#de704b', '#da7c49', '#f19b62', '#f5c266', '#eab186', '#cdad86', '#bdc0a5',
             '#eadbc4']
    plt.pie(skill_dict.values(), labels=labels, autopct='%1.1f%%', explode=explode, colors=colors)
    plt.title(jobs_string_input + '\n' + ' ключевые навыки')

    plt.show()
