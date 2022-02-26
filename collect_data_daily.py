# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()


def collect_data_daily():
    data_daily = []
    date_daily = []

    r = requests.get(
        url='http://eetk.ru/78-2/2953-2/3115-2/',
        headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(r.text, "lxml")
    changes = soup.find_all("article", class_="post-3115 page type-page status-publish hentry")
    changes_names = changes

    for change in changes:
        data_daily += [link.get("href") for link in change.find_all("a")]
    for changes_name in changes_names:
        date_daily += [link.text for link in changes_name.find_all("a")]

    with open("texts/changes.txt", "w") as file:
        for item in data_daily:
            print(item, file=file)
    with open("texts/changes_names.txt", "w") as file:
        for item in date_daily:
            print(item, file=file)

    download_file(data_daily, date_daily)


def download_file(ids, names):
    counter = -1
    temp_formats = []
    for id in ids:
        counter += 1
        if 'cloud.mail.ru' in id:
            try:
                part = id.rpartition('public/')[-1]
                name = id.rpartition('/')[-1]
                temp = requests.get(id)

                with open('texts/temp.txt', 'wb') as file:
                    file.write(temp.content)
                with open('texts/temp.txt', 'r', encoding='utf-8') as file:
                    temp = file.read()

                magic_format = temp.rpartition('"virus_scan": "pass",')[2].rpartition('"size":')[0]
                magic_format = magic_format.rpartition('"name": "')[2].rpartition('.')[2].rpartition('"')[0]
                temp_formats.append(magic_format)

                magic = temp.rpartition('"weblink_get"')[2].rpartition('"stock":')[0]
                magic = magic.rpartition('"url": "')[2].rpartition('"\n')[0] + f'/{part}'
                pdf = requests.get(magic)

                with open(f'pdfs/{name}.{magic_format}', 'wb') as f:
                    f.write(pdf.content)
            except:
                print(f'Не удалось скачать файл {id}')
        else:
            response = requests.get(id)
            temp_formats.append('pdf')
            with open(f'pdfs/{names[counter]}.pdf', 'wb') as file:
                file.write(response.content)
    with open('texts/temp_formats.txt', 'w') as file:
        for item in temp_formats:
            print(item, file=file)


def main():
    collect_data_daily()


if __name__ == '__main__':
    main()
