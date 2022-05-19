from fake_useragent import UserAgent
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


# Сбор данных с сайта колледжа (Промежуток расписания и ссылка на него)
# На вход поступает номер курса из ТГ-бота
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

    # Записываем в файл ссылки на расписание
    with open("texts/schedules.txt", "w") as file:
        for item in data_weekly:
            print(item, file=file)
    # Записываем в файл промежуток расписания
    with open("texts/schedules_names.txt", "w") as file:
        for item in date_weekly:
            print(item, file=file)

    download_file(data_weekly, date_weekly)


# Скачивание файлов для отправки в ТГ-бота (на вход подаются ссылки)
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

                # Если файл уже скачан, то еще раз он качаться не будет
                if os.path.isfile(f'pdfs/{name}.pdf'):
                    continue

                # Парсим сайт cloud.mail.ru
                temp = requests.get(id)
                temp = temp.text

                # Магическим образом достаем ссылку для скачивания
                magic_link = Link.parse_raw(temp.partition('"weblink_get":')[2].partition(',"weblink')[0])
                pdf = requests.get(magic_link.url + f'/{part}')

                # Скачиваем нужный нам pdf-файл
                with open(f'pdfs/{name}.pdf', 'wb') as f:
                    f.write(pdf.content)

            # Отлов ошибок при скачивании, которые будут выводиться в консоль
            except Exception as ex:
                print(f'Не удалось скачать файл {id}, из-за {ex}')

        # Если pdf-файл залит на сайт колледжа
        else:
            name = id.rpartition('/')[-1]  # Будущее имя файла      

            # Если файл уже скачан, то еще раз он качаться не будет
            if os.path.isfile(f'pdfs/{name}'):
                continue

            # Скачиваем нужный нам pdf-файл
            response = requests.get(id)
            temp_formats.append('pdf')
            with open(f'pdfs/{name}', 'wb') as f:
                f.write(response.content)

def main():
    collect_data_weekly(1)


if __name__ == '__main__':
    main()
