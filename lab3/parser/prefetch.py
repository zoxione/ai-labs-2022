import datetime
import argparse
import threading

import pandas as pd
import winsound
from selenium import webdriver
from lxml import html
from time import sleep
from selenium.webdriver.chrome.options import Options

parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--brand', type=str, default='', help='Марка автомобиля')
parserArgs.add_argument('--count_threads', type=int, default=1, help='Количество потоков')
parserArgs.add_argument('--start', type=int, default=1, help='Начальная страница')
parserArgs.add_argument('--end', type=int, default=1, help='Конечная страница')
args = parserArgs.parse_args()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--disable-extensions")
# driver = webdriver.Chrome(options=chrome_options)

bigBrands = ['audi', 'bmw', 'chevrolet', 'ford', 'honda', 'hyundai', 'kia', 'lexus', 'mazda', 'mercedes-benz', 'mitsubishi', 'nissan', 'opel', 'renault', 'skoda', 'subaru', 'suzuki', 'toyota', 'volkswagen', 'lada'];
brands = ['acura', 'alfa_romeo', 'aro', 'asia', 'aston_martin', 'audi', 'baw', 'bentley', 'bmw', 'brilliance', 'buick', 'byd', 'cadillac', 'changan', 'chery', 'chevrolet', 'chrysler', 'citroen', 'dacia', 'dadi', 'daewoo',
          'daihatsu', 'daimler', 'datsun', 'derways', 'dodge', 'dongfeng', 'dw_hower', 'eagle', 'evolute', 'cheryexeed', 'faw', 'ferrari', 'fiat', 'fisker', 'ford', 'foton', 'gac', 'geely', 'genesis', 'geo', 'gmc',
          'great_wall', 'hafei', 'haima', 'haval', 'hawtai', 'honda', 'hongqi', 'hummer', 'hyundai', 'infiniti', 'iran_khodro', 'isuzu', 'jac', 'jaguar', 'jeep', 'kia', 'lamborghini', 'lancia', 'land_rover', 'lexus',
          'li', 'lifan', 'lincoln', 'lotus', 'luxgen', "maserati", "maybach", "mazda", "mclaren", "mercedes-benz", "mercury", "mg", "mini", "mitsubishi", "mitsuoka", "nio", "nissan", "oldsmobile", "omoda", "opel",
          "peugeot", "plymouth", "polestar", "pontiac", "porsche", "proton", "ram", "ravon", "renault", "renault_samsung", "roewe", "rolls-royce", "rover", "saab", "saturn", "scion", "seat", "shuanghuan", "skoda",
          "skywell", "smart", "ssang_yong", "subaru", "suzuki", "tata", "tesla", "tianma", "tianye", "toyota", "volkswagen", "volvo", "vortex", "voyah", "weltmeister", "xin_kai", "xpeng", "zeekr", "zotye", "zx",
          "bogdan", "gaz", "doninvest", "zaz", "izh", "lada", "luaz", "moskvitch", "other", "tagaz", "uaz"]
carsData = [];


def getTree(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    sleep(1)
    tree = html.fromstring(driver.page_source)
    return tree


# https://auto.drom.ru/toyota/all/page1/?minyear=1940&maxyear=1989
def getUrls(urlMain):
    treeMain = getTree(urlMain);
    carsUrls = []

    countCars = treeMain.xpath('//*[@id="tabs"]/div/div/div/a[1]/text()')
    if len(countCars) > 0:
        countCars = countCars[0];
        countCars = countCars[0:countCars.find('о') - 1].replace(u'\xa0', u'')
        countCars = int(countCars)
        print('Найдено объявлений: ' + str(countCars))
    else:
        countCars = 0
        print('Нет объявлений\n')

    COUNT_ITERATION = countCars // 20 + 1;
    #COUNT_ITERATION = 1;
    if COUNT_ITERATION > 100:
        COUNT_ITERATION = 100;
    print('Всего итераций: ' + str(COUNT_ITERATION));

    for i in range(1, COUNT_ITERATION + 1):
        url = urlMain.replace('page1', 'page' + str(i));
        print('\n' + 'Парсинг ссылок на странице ' + url);
        tree = getTree(url);

        urls = tree.xpath('//a[@data-ftid="bulls-list_bull"]/@href')
        for url in urls:
            carsUrls.append({'Url': url});

        print('Выполнена итерация [' + str(i) + '/' + str(COUNT_ITERATION) + ']');
        print('Осталось времени: ' + str(((COUNT_ITERATION - i) * 2) / 60) + ' минут');

    return carsUrls;


# https://auto.drom.ru/toyota/all/page1/?minyear=1940&maxyear=1989
def getCarsData(brand):
    carsUrls = [];

    if brand in bigBrands:
        for index in range(2000, 2025, 5):
            urlMain = 'https://auto.drom.ru/' + brand + '/all/page1/?minyear=' + str(index) + '&maxyear=' + str(index + 4);
            print('----------------------------------------');
            print('Парсинг ссылок в диапазоне ' + str(index) + '-' + str(index + 4) + ' годов выпуска');
            newCarsUrls = getUrls(urlMain);
            carsUrls = carsUrls + newCarsUrls;
            print('----------------------------------------\n');
    else:
        urlMain = 'https://auto.drom.ru/' + brand + '/all/page1/';
        print('----------------------------------------');
        print('Парсинг ссылок');
        newCarsUrls = getUrls(urlMain);
        carsUrls = carsUrls + newCarsUrls;
        print('----------------------------------------\n');

    return carsUrls;


def thread(num):
    print('Запуск потока ' + str(num));

    global carsData;

    for i in range(num, len(brands), args.count_threads):
        brand = brands[i];
        print('Парсинг марки ' + brand);
        newCarsData = getCarsData(brand);
        carsData = carsData + newCarsData;
        print('Парсинг бренда ' + brand + ' завершен\n');
        print('Выявлено ссылок: ' + str(len(newCarsData)));

    return;


# ./prefetch.py --count_threads 5
if __name__ == '__main__':
    try:
        # if args.brand == '':
        #     raise Exception('Не указана марка автомобиля!\n')

        print('Скрипт запущен в', datetime.datetime.now(), '\n')

        threads = []
        for i in range(args.count_threads):
            t = threading.Thread(target=thread, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        #
        # for brand in brands:
        #     print('Парсинг марки ' + brand);
        #     newCarsData = getCarsData(brand);
        #     carsData = carsData + newCarsData;

        print('Скрипт завершил свою работу');
        print('Всего выявлено ссылок: ' + str(len(carsData)));

    except Exception as e:
        print('Ошибка при парсинге')
        print(e)

    finally:
        now = datetime.datetime.now();
        dfOutput = pd.DataFrame(carsData);
        dfOutput = dfOutput.drop_duplicates(subset=['Url']);
        print('Всего уникальных ссылок: ' + str(len(dfOutput)));
        dfOutput.to_csv('./prefetch_cars/prefetch_cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=True, index_label='Id');
        print('\nСохранено в файл ./prefetch_cars/prefetch_cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');

        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        #driver.quit()
        input('\nНажмите Enter для выхода...');
