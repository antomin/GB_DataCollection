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
from pprint import pprint
import json


def salary_parser(sal_str):
    if sal_str is None or sal_str.text[0] == 'П':
        return [None, None, None]
    sal_lst = sal_str.text.replace('\u202f', '').replace('\xa0', ' ').replace(' –', '').replace(' —', '').split(' ')
    for idx, el in enumerate(sal_lst):
        if el == '000':
            sal_lst[idx - 1] = sal_lst[idx - 1] + sal_lst.pop(idx)
    if len(sal_lst) == 2:
        return [int(sal_lst[0]), int(sal_lst[0]), sal_lst[1]]
    elif sal_lst[0] == 'от':
        return [int(sal_lst[1]), None, sal_lst[2]]
    elif sal_lst[0] == 'до':
        return [None, int(sal_lst[1]), sal_lst[2]]
    else:
        return [int(sal_lst[0]), int(sal_lst[1]), sal_lst[2]]


def vacancy_data_constructor(name, sal, hrf, site, empl, loc):
    salary = salary_parser(sal)
    return {'name': name.text,
            'salary_min': salary[0],
            'salary_max': salary[1],
            'salary_currency': salary[2],
            'href': hrf,
            'site_vacancy': site,
            'employer': empl.text if empl is not None else None,
            'location': loc
            }


position = 'python'
url_hh = 'https://hh.ru/search/vacancy'
url_sj = 'https://russia.superjob.ru'
params_hh = {
    'text': position,
    'customDomain': 1,
    'page': 38 # ПОПРАВИТЬ НА 0!!!!
}
params_sj = {
    'keywords': position,
    'page': 3  # ПОПРАВИТЬ НА 1!!!!
}
headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
vacancies_list = []

# HeadHunter
while True:
    response = requests.get(url_hh, params=params_hh, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if not soup.find('a', {'data-qa': 'pager-next'}):
        break

    vacancies = soup.select('.vacancy-serp-item__row_header')

    for vacancy in vacancies:
        info = vacancy.find('a', {'class': 'bloko-link'})
        salary_src = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        href = info['href'].split('?')[0]
        sub_vacancy = vacancy.find_next_sibling('div')
        employer = sub_vacancy.find('a')
        location = sub_vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        vacancies_list.append(vacancy_data_constructor(info, salary_src, href, 'hh.ru', employer, location))

    params_hh['page'] += 1

# SuperJob
while True:
    response = requests.get(url_sj + '/vacancy/search', params=params_sj, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    if not soup.find('a', {'class': 'f-test-button-dalshe'}):
        break

    vacancies = soup.select('.jNMYr.GPKTZ._1tH7S')

    for vacancy in vacancies:
        info = vacancy.find('a')
        salary_src = vacancy.find('span', {'class': '_2Wp8I _3a-0Y _3DjcL _1tCB5 _3fXVo'})
        href = url_sj + vacancy.find('a')['href']
        sub_vacancy = vacancy.find_next_sibling('div')
        employer = sub_vacancy.find('a')
        location = sub_vacancy.find('span', {'class': 'f-test-text-company-item-location'}).text.split(' ')[-1]

        vacancies_list.append(vacancy_data_constructor(info, salary_src, href, 'superjob.ru', employer, location))

    params_sj['page'] += 1

pprint(vacancies_list)

with open('vacancies.json', 'w', encoding='utf-8') as json_file:
    json.dump(vacancies_list, json_file, ensure_ascii=False)


