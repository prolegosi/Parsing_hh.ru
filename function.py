import requests
import json
import pandas as pd
def list_from_api(url, par=None):
    r = requests.get(url, params=par)
    out = json.loads(r.text)
    if type(out) == dict:
        out = out['items']
    return out


url_api = 'https://api.hh.ru/vacancies'
url_area = "https://api.hh.ru/areas/"

job = ["'python' and 'стажёр'"]


params = {'text': job, 'area': '113', 'per_page': '10'}

# получение списка данных из API



c = list_from_api(url_api, params)
d = list_from_api(url_area)

for i in d:
    for j in i.items():
        print(j)
    print()

for i in c:
    for j in i.items():
        print(j)
    print()

