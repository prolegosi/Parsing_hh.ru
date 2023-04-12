import back
import os
while True:
    os.system('cls||clear')
    country = input('Введите название региона\n'
                    'например: московская область; россия\n'
                    ':')
    area, area_id = back.count_validation(country)
    if not area_id:
        os.system('cls||clear')
        print(area)
        continue

    os.system('cls||clear')
    jobs_string = input('Введите ключевые слова проффессии через пробел '
                        '\nнапример: python junior удалённо\n'
                        ':')
    jobs_string = back.job_processing(jobs_string)

    os.system('cls||clear')

    per_page = 1
    params = {'text': jobs_string, 'area': '113', 'per_page': per_page}
    job_list = back.list_from_api(back.url_api, params)
    skills = back.skill_list(job_list)

    skill_dict = back.sort_skill_dict(skills)
    print(skill_dict)


