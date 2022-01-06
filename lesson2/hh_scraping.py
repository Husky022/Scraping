from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json

search = 'Python'

url = f'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&hhtmFrom=vacancy_search_list'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

params = {
    'text': search
}

vacancies_dict = {}

page_count = 0
vacancy_count = 0

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
                vacancy_salary['min'] = salary_string.split('–')[0]
                vacancy_salary['max'] = salary_string.split('–')[1]
        else:
            vacancy_salary['min'], vacancy_salary['max'], vacancy_salary['valute'] = None, None, None

        vacancy_info['salary'] = vacancy_salary

        vacancies_dict[vacancy_count] = vacancy_info

    if len(soup.find_all('a',{'class': 'bloko-button', 'data-qa': 'pager-next'})) > 0:

        page_count += 1

    else:
        pprint(vacancies_dict)
        break


with open(f'Vacancies for search = {search}.json', 'w', encoding='utf-8') as file:
    json.dump(vacancies_dict, file, indent=4)
