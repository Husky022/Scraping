from pymongo import MongoClient
from pprint import pprint

search = 'Python'

required_salary = 100000  #желаемый уровень зарплаты

client = MongoClient('localhost', 27017)

db = client[f'vacancy-{search}']

collection = db.vacancies_collection

# result = collection.find_one( { "$and": [ { 'name': 'Data Scientist ML/AI Engineer' }, { 'link': 'https://hh.ru/vacancy/50806691?from=vacancy_search_list&query=Python&hhtmFrom=vacancy_search_list' } ] } )

result = collection.find( { '$and': [ { 'salary.min': {'$lte': required_salary }}, { 'salary.max': {'$gte': required_salary }}]})

for el in result:
    print(el)

required_salary_count = collection.count_documents( { '$and': [ { 'salary.min': {'$lte': required_salary }}, { 'salary.max': {'$gte': required_salary }}]})

if required_salary_count:
    print(f'По запросу найдено {required_salary_count} вакансий')
else:
    print('По Вашему запросу ничего не найдено')


