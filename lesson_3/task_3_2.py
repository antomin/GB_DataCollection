"""
Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска
продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос
проверяет оба поля)
"""

from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
db = client["vacancies"]
collection = db.all_vacancies

user_salary = int(input("Желаемвя зарплата: "))

vacancies_for_user = collection.find(
    {"$and": [{"salary_min": {"$lte": user_salary}}, {"salary_max": {"$gte": user_salary}}]}
)

for idx, vacancy in enumerate(vacancies_for_user):
    print(idx, vacancy)
