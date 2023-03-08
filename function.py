import requests
import json


url_api = 'https://api.hh.ru/vacancies'
url_country = "https://api.hh.ru/areas/"

job = ["'python' and 'стажёр'"]


params = {'text': job, 'area': '113', 'per_page': '10'}


def list_from_api(url, par=None):
    r = requests.get(url, params=par)
    out = json.loads(r.text)
    return out


#d = jobs_list(url_api, params)
d = list_from_api(url_country)
for i in d:
    for j in i.items():
        print(j)
    print()
