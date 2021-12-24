import requests
import json

user = 'Husky022'
req = requests.get(f'https://api.github.com/users/{user}/repos')
if req.status_code == 404:
    raise Exception(f'User {user} not found!')

req_json = json.loads(req.text)

result = []
user_repos = {}
repos = {}

for element in req_json:
    repos[element['name']] = element['html_url']

user_repos[user] = repos
print(user_repos)

with open(f'{user}_repos.json', 'w') as file:
    json.dump(user_repos, file, indent=4)
