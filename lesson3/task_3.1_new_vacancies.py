from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
from pymongo import MongoClient
from uuid import uuid4


search = 'Python'

client = MongoClient('localhost', 27017)

db = client[f'vacancy-{search}']

collection = db.vacancies_collection

url = f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&hhtmFrom=vacancy_search_list'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

params = {
    'text': search
}

vacancy_count = 0
page_count = 0
new_vacancy_count = 0

while True:
    params['page'] = page_count
    response = requests.get(url, headers=headers, params=params).text
    soup = bs(response, 'html.parser')
    vacancies = soup.find_all('div', {'class': ['vacancy-serp-item', 'vacancy-serp-item_premium']})
    for el in vacancies:
        vacancy_count += 1
        print(vacancy_count)
        vacancy_info = {}
        vacancy_salary = {}
        vacancy_name = el.find_all('a', {'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})[0]
        vacancy_info['name'] = vacancy_name.string
        vacancy_info['link'] = vacancy_name['href']
        salary_all = el.find('span', {'class': 'bloko-header-section-3 bloko-header-section-3_lite',
                                      'data-qa': 'vacancy-serp__vacancy-compensation'})
        if salary_all:
            salary_string = salary_all.text
            salary_valute = salary_string.split()[-1]
            vacancy_salary['valute'] = salary_valute
            salary_string = "".join(salary_string.split())[:-len(salary_valute)]
            if salary_string.startswith('от'):
                vacancy_salary['min'] = int(salary_string[2:])
                vacancy_salary['max'] = None
            if salary_string.startswith('до'):
                vacancy_salary['min'] = None
                vacancy_salary['max'] = int(salary_string[2:])
            if '–' in salary_string:
                vacancy_salary['min'] = int(salary_string.split('–')[0])
                vacancy_salary['max'] = int(salary_string.split('–')[1])
        else:
            vacancy_salary['min'], vacancy_salary['max'], vacancy_salary['valute'] = None, None, None

        vacancy_info['salary'] = vacancy_salary
        vacancy_info['_id'] = str(uuid4())
        find_vacancy = collection.find_one( { "$and": [ { 'name': vacancy_info['name'] }, { 'link': vacancy_info['link'] } ] } )

        if not find_vacancy:
            new_vacancy_count += 1
            collection.insert_one(vacancy_info)

    if len(soup.find_all('a',{'class': 'bloko-button', 'data-qa': 'pager-next'})) > 0:
        page_count += 1

    else:
        if new_vacancy_count:
            print(f'\nПо запросу "{search}" - {new_vacancy_count} новых вакансий')
        else:
            print(f'\nНе добавлено новых вакансий по запросу - {search}')
        break



