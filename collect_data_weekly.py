import pathlib
import time
import os
import os.path
import requests

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

ua = UserAgent()


def collect_data_weekly():
    data_weekly = []
    date_weekly = []

    r = requests.get(
        url='http://eetk.ru/78-2/82-2/88-2/',
        headers={'user-agent': f'{ua.random}'})

    soup = BeautifulSoup(r.text, "lxml")
    schedules = soup.find_all("tr", class_="row-4 even")
    schedules_names = soup.find_all("article", class_="post-88 page type-page status-publish hentry")

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

    download_file(data_weekly, date_weekly)


def download_file(ids, names):
    check_file = []
    for i in range(len(names)):
        check_file.append(os.path.exists(f'pdfs/{ids[i].rpartition("/")[-1]}.pdf'))
    if all(check_file):
        print('vse norm')
        return

    path = "/app/downloads/"
    glob_path = pathlib.Path("/app/downloads/")

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": f'{path}'}
    options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.headless = True
    driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),
                              options=options)

    for id in ids:
        try:
            driver.get(f'{id}')
            driver.find_element(By.XPATH, '//div [@data-qa-id="download"]').click()
            time.sleep(2)
            for i, path in enumerate(glob_path.glob('*.pdf')):
                new_name = id.rpartition('/')[-1] + '.pdf'
                path.rename(f'pdfs/{new_name}')
        except:
            driver.quit()

    files = glob_path.glob('*.pdf')
    for f in files:
        os.remove(f)


def main():
    collect_data_weekly()


if __name__ == '__main__':
    main()
