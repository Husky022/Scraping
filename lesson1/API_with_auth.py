import requests
import json
from pprint import pprint

api_key = '78bed5c8a2532c94d4ea03b90717a0c3'
service = 'https://api-cloud.ru/api/autophoto.php'
reg_num = 'Е017ЕЕ197'
req = requests.get(f'{service}?type=regnum&token={api_key}&regNum={reg_num}')
data = json.loads(req.text)
if not data.get('message', None):
    pprint(data)
    with open(f'{reg_num}_cars_photo.json', 'w') as file:
        json.dump(data, file, indent=4)
else:
    print(data.get('message'))
