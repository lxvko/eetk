from fake_useragent import UserAgent
from urllib.parse import urlencode
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
import os

# Формирование фейкового юзер-агента, чтобы сайт не блочил доступ при частых запросах
ua = UserAgent()


# Упрощенная система парсинга ссылок для скачивания pdf-файлов с cloud.mail.ru
class Format(BaseModel):
    name: str


class Link(BaseModel):
    url: str


# Сбор данных с сайта колледжа (Имя изменений и ссылка на них)
def collect_data_daily():
    data_daily = []
    date_daily = []

    r = requests.get(
        url='http://eetk.ru/78-2/2953-2/3115-2/',
        headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(r.text, "lxml")
    changes = soup.find_all(
        "article", class_="post-3115 page type-page status-publish hentry")
    changes_names = changes

    for change in changes:
        data_daily += [link.get("href") for link in change.find_all("a")]
    for changes_name in changes_names:
        date_daily += [link.text for link in changes_name.find_all("a")]

    # Записываем в файл ссылки на изменения
    with open("texts/changes.txt", "w") as file:
        for item in data_daily:
            print(item, file=file)
    # Записываем в файл имена изменений
    with open("texts/changes_names.txt", "w") as file:
        for item in date_daily:
            print(item, file=file)

    download_file(data_daily, date_daily)


# Скачивание файлов для отправки в ТГ-бота (на вход подаются ссылки и имена)
def download_file(ids, names):
    counter = -1
    temp_formats = []
    for id in ids:
        counter += 1
        # Если pdf-файл залит в cloud.mail.ru
        if 'cloud.mail.ru' in id:
            try:
                part = id.rpartition('public/')[-1]  # Кусок будущей ссылки для скачивания
                name = id.rpartition('/')[-1]  # Будущее имя файла

                # Парсим сайт cloud.mail.ru
                temp = requests.get(id)
                temp = temp.text

                # Магическим образом достаем формат будущего файла
                magic_format = Format.parse_raw(temp.partition('"list": [\n')[2].partition(']')[0])
                temp_formats.append(magic_format.name.split('.')[-1])

                # Магическим образом достаем ссылку для скачивания
                magic_link = Link.parse_raw(temp.partition('"weblink_get": ')[2].partition(',\n\t\t"')[0])
                pdf = requests.get(magic_link.url + f'/{part}')

                # Если файл уже скачан, то еще раз он качаться не будет
                if os.path.isfile(f'pdfs/{name}.pdf'):
                    continue
                # Проверка на jpg формат.. :/ Были случаи..
                elif os.path.isfile(f'pdfs/{name}.jpg'):
                    continue

                # Скачиваем нужный нам pdf-файл
                with open(f'pdfs/{name}.{temp_formats[-1]}', 'wb') as f:
                    f.write(pdf.content)

            # Отлов ошибок при скачивании, которые будут выводиться в консоль
            except Exception as ex:
                print(f'Не удалось скачать файл {id}, из-за {ex}')

        # Если pdf-файл залит на Яндекс Диск (боже, упаси)
        # Возможно ТГ-бот их не отправит, потому что мне было лень реализовывать НАСТОЛЬКО редкий случай :)
        elif 'disk.yandex.ru' in id:
            try:
                # Это база (формируем запрос для получения ссылки скачивания с Яндекс Диска)
                base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
                final_url = base_url + urlencode(dict(public_key=id))

                # Обращаемся к API сайта
                response = requests.get(final_url)
                download_url = response.json()['href']  # Вытаскиваем ссылку на скачивание pdf-файла
                name = (download_url.split('&filename='))[1].split('&disposition')[0]  # Вытаскиваем имя будущего файла
                temp_formats.append(name.split('.')[-1])

                # Если файл уже скачан, то еще раз он качаться не будет
                if os.path.isfile(f'pdfs/{name}'):
                    continue

                # Скачиваем нужный нам pdf-файл
                pdf = requests.get(download_url)
                with open(f'pdfs/{name}', 'wb') as f:
                    f.write(pdf.content)

            # Отлов ошибок при скачивании, которые будут выводиться в консоль
            except Exception as ex:
                print(f'Не удалось скачать файл {id}, из-за {ex}')

        # Если pdf-файл залит на сайт колледжа
        else:
            # Если файл уже скачан, то еще раз он качаться не будет
            if os.path.isfile(f'pdfs/{names[counter]}.pdf'):
                continue

            # Скачиваем нужный нам pdf-файл
            response = requests.get(id)
            temp_formats.append('pdf')
            with open(f'pdfs/{names[counter]}.pdf', 'wb') as f:
                f.write(response.content)

    # Ведем запись форматов, которые сейчас находятся в папке, для корректной работы ТГ-бота
    if temp_formats:
        with open('texts/temp_formats.txt', 'w') as file:
            for item in temp_formats:
                print(item, file=file)


def main():
    collect_data_daily()


if __name__ == '__main__':
    main()
