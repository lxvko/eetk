import random
import json
import requests
from serpapi import GoogleSearch


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
    with open('cats/data.json', 'w') as file:
        file.write(json.dumps(results['images_results'], indent=2))


def get_kitty(kitties):
    counter = []
    kitties_work = kitties.copy()
    for i in reversed(range(len(kitties))):
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
            del kitties_work[i]
    for i in range(len(kitties_work)):
        counter.append(kitties_work[i]['position'])

    count = random.choice(counter)
    for kitty in kitties_work:
        if kitty.get('position') == count:
            image = requests.get(kitty['original']).content
            del kitties_work[counter.index(count)]
            counter.remove(count)

    with open(f'cats/kitty.jpg', 'wb') as file:
        file.write(image)

    with open('cats/data.json', 'w') as file:
        file.write(json.dumps(kitties_work, indent=2))


def collect_kitty():
    with open('cats/data.json', 'r') as file:
        kitties = json.load(file)
    if len(kitties) == 0:
        get_google_images()
        main()
    else:
        get_kitty(kitties)


def main():
    collect_kitty()


if __name__ == '__main__':
    main()
