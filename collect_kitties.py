# Эта фича была придумана и реализована будучи в нетрезвом состоянии ума и тела
# О ней почти никто не знает и на том спасибо :)
# Кодовое слово в ТГ-боте "Милый котик"

# По-хорошему, реализацию фичи нужно переделать под сайт 'https://random.cat/'
# Но мне лень

from serpapi import GoogleSearch
import requests
import random
import json


# Функция обращается к сервису, который собирает картинки по параметру "q":
def get_google_images():
    params = {
        "api_key": "d094df85fa3f2b1047d7f464e3989d9c48ccbba4bd4359b982e10333ddf1a89a",
        "engine": "google",
        "ijn": "0",
        "q": "милые котики",
        "google_domain": "google.com",
        "tbm": "isch"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # Записываем 100 первых ссылок на картинки с котиками из гугла
    with open('cats/data.json', 'w') as file:
        file.write(json.dumps(results['images_results'], indent=2))


# Получаем котиков в картинках (На вход подается json котиков)
def get_kitty(kitties):
    counter = []
    # Копируем оригинальный json для внесения правок
    kitties_work = kitties.copy()
    for i in reversed(range(len(kitties))):
        # Перечень сайтов, которые так или иначе плохо возвращают котиков (список можно пополнять)
        if \
                kitties_work[i]['source'] == 'm.facebook.com' \
                or kitties_work[i]['source'] == 'facebook.com' \
                or kitties_work[i]['source'] == 'ont.by' \
                or kitties_work[i]['source'] == 'novosti-n.org' \
                or kitties_work[i]['source'] == 'ysia.ru' \
                or kitties_work[i]['source'] == 'krasivosti.pro' \
                or kitties_work[i]['source'] == 'mover.uz' \
                or kitties_work[i]['source'] == 'cultmall.com.ua · In stock' \
                or kitties_work[i]['source'] == 'mariart.kiev.ua · In stock' \
                or kitties_work[i]['source'] == 'pets.24tv.ua' \
                or kitties_work[i]['source'] == 'stickers.wiki':
            # Эти сайты удаляются из json с котиками, чтобы в будущем не мешать работе
            del kitties_work[i]
    # Реализуем номера для котиков
    for i in range(len(kitties_work)):
        counter.append(kitties_work[i]['position'])

    # Берем рандомный номер из списка
    count = random.choice(counter)
    for kitty in kitties_work:
        if kitty.get('position') == count:
            # Сохраняем котика :)
            image = requests.get(kitty['original']).content
            # Удаляем использованного котика :(
            del kitties_work[counter.index(count)]
            counter.remove(count)

    # Записываем котика в файл
    with open(f'cats/kitty.jpg', 'wb') as file:
        file.write(image)

    # Перезаписываем базу данных котиков
    with open('cats/data.json', 'w') as file:
        file.write(json.dumps(kitties_work, indent=2))


# Основная функция
def collect_kitty():
    # Открываем базу данных котиков из файла
    with open('cats/data.json', 'r') as file:
        kitties = json.load(file)
    # Если в базе нет ни одного котика, то парсим новых через сервис
    if len(kitties) == 0:
        get_google_images()
        main()
    # Иначе сохраняем котика на компьютер
    else:
        get_kitty(kitties)


def main():
    collect_kitty()


if __name__ == '__main__':
    main()
