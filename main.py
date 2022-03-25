from fake_useragent import UserAgent
from collect_data_weekly import collect_data_weekly
from collect_data_daily import collect_data_daily
import requests
from bs4 import BeautifulSoup
import time
import os
import glob

data_weekly = []
data_daily = []
result_weekly = []
result_daily = []
user_id = []

ua = UserAgent()
token = 'bot5068878742:AAEB6rC4kEmngswkQS6n31fAVR3szf7NshE'


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


def collect_result():
    while True:

        time.sleep(40)

        # Weekly check
        global result_weekly
        result_weekly.clear()

        try:
            r = requests.get(
                url='http://eetk.ru/78-2/82-2/88-2/',
                headers={'user-agent': f'{ua.random}'})
        except requests.ConnectionError as e:
            print(str(e))
            time.sleep(60)
            continue
        except requests.Timeout as e:
            print(str(e))
            time.sleep(60)
            continue
        except requests.RequestException as e:
            print(str(e))
            time.sleep(60)
            continue
        except KeyboardInterrupt:
            print("Something closed the program")

        soup = BeautifulSoup(r.text, "lxml")
        schedules = soup.find_all("tr", class_="row-4 even")
        for schedule in schedules:
            result_weekly += [link.get("href") for link in schedule.find_all("a")]

        time.sleep(40)

        # Daily check
        global result_daily
        result_daily.clear()

        try:
            r = requests.get(
                url='http://eetk.ru/78-2/2953-2/3115-2/',
                headers={'user-agent': f'{ua.random}'})
        except requests.ConnectionError as e:
            print(str(e))
            time.sleep(60)
            continue
        except requests.Timeout as e:
            print(str(e))
            time.sleep(60)
            continue
        except requests.RequestException as e:
            print(str(e))
            time.sleep(60)
            continue
        except KeyboardInterrupt:
            print("Something closed the program")

        soup = BeautifulSoup(r.text, "lxml")
        changes = soup.find_all("article", class_="post-3115 page type-page status-publish hentry")
        for change in changes:
            result_daily += [link.get("href") for link in change.find_all("a")]

        if data_weekly != result_weekly:
            check(result_weekly)
        elif data_daily != result_daily:
            check(result_daily)
        else:
            result_weekly.clear()
            result_daily.clear()


def check(check_data):
    if check_data == result_weekly:
        time.sleep(30)
        if data_weekly != result_weekly:
            send_message('На сайте выложили новое расписание!')
            reload_data()
            collect_data()
    elif check_data == result_daily:
        time.sleep(30)
        if data_daily != result_daily:
            send_message('На сайте появились изменения!')
            reload_data()
            collect_data()


def send_message(message):
    global user_id
    user_id.clear()

    with open('user_id.txt') as file:
        user_id = [line.strip() for line in file]

    for req in range(len(user_id)):
        time.sleep(1)
        r = requests.get(f'https://api.telegram.org/{token}/sendMessage'
                         f'?chat_id={user_id[req]}&text={message}')


def reload_data():
    for file in glob.glob('pdfs/*'):
        os.remove(file)

    collect_data_daily()

    course = 1
    for course in range(1, 5):
        time.sleep(2)
        try:
            collect_data_weekly(course)
        except:
            pass


# 760196701 author
# 825248757 nikita

if __name__ == '__main__':
    collect_data()
