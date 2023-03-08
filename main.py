import requests
import json

url = 'https://api.hh.ru/vacancies'
job = ["'python' and 'junior'"]
params = {'text': job, 'area': '113', 'per_page': '10'}
r = requests.get(url, params=params)
d = json.loads(r.text)

for i in d.items():
    print(i)
