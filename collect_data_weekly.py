import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os

ua = UserAgent()


def collect_data_weekly(course):
    data_weekly = []
    date_weekly = []

    r = requests.get(
        url='http://eetk.ru/78-2/82-2/88-2/',
        headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(r.text, "lxml")

    if course == 1:
        schedules = soup.find_all("tr", class_="row-1 odd")
    elif course == 2:
        schedules = soup.find_all("tr", class_="row-2 even")
    elif course == 3:
        schedules = soup.find_all("tr", class_="row-3 odd")
    elif course == 4:
        schedules = soup.find_all("tr", class_="row-4 even")

    schedules_names = soup.find_all(
        "article", class_="post-88 page type-page status-publish hentry")

    for schedule in schedules:
        data_weekly += [link.get("href") for link in schedule.find_all("a")]
    for schedules_name in schedules_names:
        date_weekly += [link.text for link in schedules_name.find_all("h3")]

    with open("texts/schedules.txt", "w") as file:
        for item in data_weekly:
            print(item, file=file)
    with open("texts/schedules_names.txt", "w") as file:
        for item in date_weekly:
            print(item, file=file)

    download_file(data_weekly)


def download_file(ids):
    for id in ids:

        part = id.rpartition('public/')[-1]
        name = id.rpartition('/')[-1]
        if os.path.isfile(f'pdfs/{name}.pdf'):
            continue
        temp = requests.get(id)
        temp = temp.text

        magic = temp.rpartition('"weblink_get"')[2].rpartition('"weblink_thumbnails":')[0]
        magic = magic.partition('"url": "')[2].partition('no"')[0] + f'no/{part}'
        pdf = requests.get(magic)
        with open(f'pdfs/{name}.pdf', 'wb') as f:
            f.write(pdf.content)


def main():
    collect_data_weekly()


if __name__ == '__main__':
    main()
