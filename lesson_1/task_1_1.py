"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""

import requests

user = "antomin"  # Enter username here
url = f"https://api.github.com/users/{user}/repos"
responce = requests.get(url)

if responce.ok:
    with open("data.json", "w") as new_json:
        new_json.write(
            responce.text
        )  # Не уверен, что можно в json хранить список словарей. Прокоментируйте, пожалуйста.

    for el in responce.json():
        print(el["name"])
else:
    print(f'User "{user}" not found.')
