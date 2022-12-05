import datetime
import pandas as pd
from selenium import webdriver
from lxml import html
from time import sleep
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

MAX_PAGE = 1
carsData = []


def getTree(url):
    driver.get(url)
    sleep(2)
    tree = html.fromstring(driver.page_source)
    return tree


def getUrls(tree):
    urls = tree.xpath('//a[@data-ftid="bulls-list_bull"]/@href')
    return urls


if __name__ == '__main__':
    try:
        index = 1;
        urlMain = 'https://auto.drom.ru/all/';

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(index) + '\n');

        while True:
            print('Парсинг ссылок на странице ' + urlMain + 'page' + str(index) + '/');
            treeMain = getTree(urlMain + 'page' + str(index) + '/');

            urls = getUrls(treeMain);

            for url in urls:
                carsData.append({'Url': url});

            print('Выполнена итерация [' + str(index) + '/' + str(MAX_PAGE) + ']');
            index += 1;
            if index == (MAX_PAGE + 1):
                break;

        print('\nСкрипт завершил свою работу');
        print('Всего ссылок: ' + str(len(carsData)));

    except Exception as e:
        print('Ошибка при парсинге')
        print(e)

    finally:
        now = datetime.datetime.now();
        df = pd.DataFrame(carsData);
        df.to_csv('prefetch_cars_' + now.strftime("%Y-%m-%d %H-%M-%S") + '.csv', index=True, index_label='Id');
        print('\nСохранено в файл prefetch_cars_' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.csv');

        driver.quit()
        input('\nНажмите Enter для выхода...');
