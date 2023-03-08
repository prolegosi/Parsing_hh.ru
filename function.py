import requests
import json
#"url": "https://api.hh.ru/areas/
url = 'https://api.hh.ru/vacancies'
job = ["'python' and 'стажёр'"]
params = {'text': job, 'area': '113', 'per_page': '10'}
r = requests.get(url, params=params)
d = json.loads(r.text)

for i in d['items']:
    for j in i.items():
        print(j)
    print()
