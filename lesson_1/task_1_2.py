"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
пройдя авторизацию. Ответ сервера записать в файл.
"""

# Сервис last.fm выдаёт топ песен по заданному артисту
import requests

api_key = 'b2cdd74fcee30058c33cebede779d331'
artist_name = 'ыукпу'
url = 'http://ws.audioscrobbler.com/2.0/'
params = {
    'method': 'artist.gettoptracks',
    'artist': artist_name,
    'api_key': api_key,
    'format': 'json'
}

responce = requests.post(url, params=params)

with open(f'top_tracks_of_{artist_name}.txt', 'w') as new_file:
    new_file.write(responce.text)
