"""
Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять
только новые вакансии/продукты в вашу базу.
"""

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


def salary_parser(sal_str):
    if sal_str is None or sal_str.text[0] == "П":
        return [None, None, None]
    sal_lst = sal_str.text.replace("\u202f", "").replace("\xa0", " ").replace(" –", "").replace(" —", "").split(" ")
    for idx, el in enumerate(sal_lst):
        if el == "000":
            sal_lst[idx - 1] = sal_lst[idx - 1] + sal_lst.pop(idx)
    if len(sal_lst) == 2:
        return [int(sal_lst[0]), int(sal_lst[0]), sal_lst[1]]
    elif sal_lst[0] == "от":
        return [int(sal_lst[1]), None, sal_lst[2]]
    elif sal_lst[0] == "до":
        return [None, int(sal_lst[1]), sal_lst[2]]
    else:
        return [int(sal_lst[0]), int(sal_lst[1]), sal_lst[2]]


def vacancy_data_constructor(name, sal, hrf, site, empl, loc, v_id):
    salary = salary_parser(sal)
    vacancy_data = {
        "_id": v_id,
        "name": name.text,
        "salary_min": salary[0],
        "salary_max": salary[1],
        "salary_currency": salary[2],
        "href": hrf,
        "site_vacancy": site,
        "employer": empl.text if empl is not None else None,
        "location": loc,
    }

    collection.insert_one(vacancy_data)


# Request params
position = "python"
url_hh = "https://hh.ru/search/vacancy"
url_sj = "https://russia.superjob.ru"
params_hh = {"text": position, "customDomain": 1, "page": 0}
params_sj = {"keywords": position, "page": 1}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# db params
client = MongoClient("127.0.0.1", 27017)
db = client["vacancies"]
collection = db.all_vacancies
id_vacancies_list = [el["_id"] for el in collection.find({}, {"_id"})]

# HeadHunter
while True:
    response = requests.get(url_hh, params=params_hh, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if not soup.find("a", {"data-qa": "pager-next"}):
        break

    vacancies = soup.select(".vacancy-serp-item__row_header")

    for vacancy in vacancies:
        info = vacancy.find("a", {"class": "bloko-link"})
        href = info["href"].split("?")[0]
        vac_id = f"hh_{href.split('/')[-1]}"
        if vac_id in id_vacancies_list:
            continue
        salary_src = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        sub_vacancy = vacancy.find_next_sibling("div")
        employer = sub_vacancy.find("a").replace("\xa0", "")
        location = sub_vacancy.find("div", {"data-qa": "vacancy-serp__vacancy-address"}).text
        vacancy_data_constructor(info, salary_src, href, "hh.ru", employer, location, vac_id)

    params_hh["page"] += 1

# SuperJob
while True:
    response = requests.get(url_sj + "/vacancy/search", params=params_sj, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    if not soup.find("a", {"class": "f-test-button-dalshe"}):
        break

    vacancies = soup.select(".jNMYr.GPKTZ._1tH7S")

    for vacancy in vacancies:
        info = vacancy.find("a")
        href = url_sj + vacancy.find("a")["href"]
        vac_id = f"sj_{href.split('-')[-1].split('.')[0]}"
        if vac_id in id_vacancies_list:
            continue
        salary_src = vacancy.find("span", {"class": "_2Wp8I _3a-0Y _3DjcL _1tCB5 _3fXVo"})
        sub_vacancy = vacancy.find_next_sibling("div")
        employer = sub_vacancy.find("a")
        location = sub_vacancy.find("span", {"class": "f-test-text-company-item-location"}).text.split(" ")[-1]

        vacancy_data_constructor(info, salary_src, href, "superjob.ru", employer, location, vac_id)

    params_sj["page"] += 1
