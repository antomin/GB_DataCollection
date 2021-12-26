"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1. Наименование вакансии.
2. Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
3. Ссылку на саму вакансию.
4. Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json
либо csv.
"""

import requests
from bs4 import BeautifulSoup


def salary_parser(sal_str):
    if sal_str is None:
        return [None, None, None]
    sal_lst = sal_str.text.replace('\u202f', '').replace(' –', '').split(' ')
    if sal_lst[0] == 'от':
        return [int(sal_lst[1]), None, sal_lst[2]]
    elif sal_lst[0] == 'до':
        return [None, int(sal_lst[1]), sal_lst[2]]
    else:
        return [int(sal_lst[0]), int(sal_lst[1]), sal_lst[2]]


position = 'python'
url = 'https://hh.ru/search/vacancy'
params = {
    'text': position,
    'customDomain': 1,
    'page': 0
}
headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
vacancies_list = []

while True:
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if not soup.find('a', {'data-qa': 'pager-next'}):
        break

    vacancies = soup.select('.vacancy-serp-item__row_header')

    for vacancy in vacancies:
        vacancy_data = {}
        info = vacancy.find('a', {'class': 'bloko-link'})
        salary_src = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        href = info['href']
        site = 'hh.ru'
        sub_vacancy = vacancy.find_next_sibling('div')
        employer = sub_vacancy.find('a')
        location = sub_vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})

        vacancy_data['name'] = info.text
        salary = salary_parser(salary_src)
        vacancy_data['salary_min'] = salary[0]
        vacancy_data['salary_max'] = salary[1]
        vacancy_data['salary_currency'] = salary[2]
        vacancy_data['href'] = href.split('?')[0]
        vacancy_data['site_vacancy'] = site
        vacancy_data['employer'] = employer.text.replace('\xa0', ' ')
        vacancy_data['location'] = location.text

        vacancies_list.append(vacancy_data)

    params['page'] += 1
