import requests
from data import token

url = "https://cloud-api.yandex.net/v1/disk/resources?path=/"


payload = ""
headers = {'Authorization': token}


response = requests.request("GET", url, headers=headers, data=payload)

rj = response.json()
# print(rj)

sort = rj['_embedded']
# print(sort)

items = sort['items']
# print(items)

for i in items:
    print(i['name'] + ' - ' + i['type'])


close = requests.post(url=url, headers={'Connection': 'close'})
