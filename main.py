from collect_data_weekly import collect_data_weekly
from collect_data_daily import collect_data_daily
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import time
import glob
import os

# Ввод глобальных переменных
data_weekly = []
data_daily = []
result_weekly = []
result_daily = []
user_id = []
# Формирование фейкового юзер-агента, чтобы сайт не блочил доступ при частых запросах
ua = UserAgent()

# Вводим токен нашего бота с припиской bot
token = 'bot5085326595:AAGVsDbtRcsj4at6haoV10d5_vSnBoaeNqg'

# 5068878742:AAHeLzjo7WNXb_siW9YVQTKpfae3R6wKHIg Токен главного бота
# 5085326595:AAGVsDbtRcsj4at6haoV10d5_vSnBoaeNqg Токен тестового бота

# 760196701 Это я)) @lxvko


# Собираем актуальные данные для использования в качестве оригинала
def collect_data():
    global data_weekly
    data_weekly.clear()
    r = requests.get(
        url='http://eetk.ru/78-2/82-2/88-2/',
        headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(r.text, "lxml")
    schedules = soup.find_all("tr", class_="row-4 even")
    for schedule in schedules:
        data_weekly += [link.get("href") for link in schedule.find_all("a")]

    global data_daily
    data_daily.clear()
    r = requests.get(
        url='http://eetk.ru/78-2/2953-2/3115-2/',
        headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(r.text, "lxml")
    changes = soup.find_all("article", class_="post-3115 page type-page status-publish hentry")
    for change in changes:
        data_daily += [link.get("href") for link in change.find_all("a")]

    collect_result()


# Проверяем на наличие отличий в вечном цикле
def collect_result():
    while True:
        # Такие большие задержки нужны чтобы парсинг был 24/7 и чтобы сайт не запрещал доступ

        time.sleep(40)

        if collect_result_weekly() is False:
            continue

        time.sleep(40)

        if collect_result_daily() is False:
            continue

        # Сверяем оригинал с копией (первая проверка)
        if data_weekly != result_weekly:
            check(result_weekly)
        elif data_daily != result_daily:
            check(result_daily)
        # Если все совпало, то очищаем копии
        else:
            result_weekly.clear()
            result_daily.clear()


# Проверка расписания
def collect_result_weekly():
    # Собираем актуальные данные для использования в качестве копии
    global result_weekly
    result_weekly.clear()

    # Обход различных ошибок со стороны сайта
    try:
        r = requests.get(
            url='http://eetk.ru/78-2/82-2/88-2/',
            headers={'user-agent': f'{ua.random}'})
    except requests.ConnectionError as e:
        print(str(e))
        time.sleep(60)
        return False
    except requests.Timeout as e:
        print(str(e))
        time.sleep(60)
        return False
    except requests.RequestException as e:
        print(str(e))
        time.sleep(60)
        return False
    except KeyboardInterrupt:
        print("Something closed the program")

    soup = BeautifulSoup(r.text, "lxml")
    schedules = soup.find_all("tr", class_="row-4 even")
    for schedule in schedules:
        result_weekly += [link.get("href") for link in schedule.find_all("a")]
    return True


# Проверка измерений
def collect_result_daily():
    # Собираем актуальные данные для использования в качестве копии
    global result_daily
    result_daily.clear()

    # Обход различных ошибок со стороны сайта
    try:
        r = requests.get(
            url='http://eetk.ru/78-2/2953-2/3115-2/',
            headers={'user-agent': f'{ua.random}'})
    except requests.ConnectionError as e:
        print(str(e))
        time.sleep(60)
        return False
    except requests.Timeout as e:
        print(str(e))
        time.sleep(60)
        return False
    except requests.RequestException as e:
        print(str(e))
        time.sleep(60)
        return False
    except KeyboardInterrupt:
        print("Something closed the program")
        return False

    soup = BeautifulSoup(r.text, "lxml")
    changes = soup.find_all("article", class_="post-3115 page type-page status-publish hentry")
    for change in changes:
        result_daily += [link.get("href") for link in change.find_all("a")]
    return True


# Вторая сверка оригинала с копией (на вход подается копия)
def check(check_data):
    if check_data == result_weekly:
        time.sleep(30)
        # Собираем актуальные данные для использования в качестве копии
        collect_result_weekly()
        # Ожидаем время и еще раз проводим сверку оригинала с копией
        if data_weekly != result_weekly:
            # Если на сайте точно есть новое расписание - запускаем рассылку
            send_message('На сайте выложили новое расписание!')
            # Производим обновление папки pdfs до актуальной версии
            reload_data()
            # Получаем новый оригинал и отправляемся крутить цикл дальше
            collect_data()
    elif check_data == result_daily:
        time.sleep(30)
        # Собираем актуальные данные для использования в качестве копии
        collect_result_daily()
        # Ожидаем время и еще раз проводим сверку оригинала с копией
        if data_daily != result_daily:
            # Если на сайте точно есть изменения - запускаем рассылку
            send_message('На сайте появились изменения!')
            # Производим обновление папки pdfs до актуальной версии
            reload_data()
            # Получаем новый оригинал и отправляемся крутить цикл дальше
            collect_data()


# Функция отправки сообщений участникам рассылки
def send_message(message):
    global user_id
    user_id.clear()

    # Подгружаем базу данных пользователей
    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    # Отправляем каждому пользователю по очереди сообщение с нужным текстом
    for req in range(len(user_id)):
        time.sleep(1)
        r = requests.get(f'https://api.telegram.org/{token}/sendMessage'
                         f'?chat_id={user_id[req]}&text={message}')


# Обновление папки pdfs до актуальной версии
def reload_data():
    # Удаляем все файлы из папки pdfs
    for file in glob.glob('pdfs/*'):
        os.remove(file)

    # Скачиваем актуальные файлы изменений
    collect_data_daily()

    course = 1
    # Скачиваем актуальные файлы расписания для всех курсов
    for course in range(1, 5):
        time.sleep(2)
        try:
            collect_data_weekly(course)
        except:
            pass


if __name__ == '__main__':
    collect_data()
