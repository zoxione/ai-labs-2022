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
parserArgs.add_argument('--count_threads', type=int, default=1, help='Количество потоков')
parserArgs.add_argument('--brand', type=str, default='', help='Марка автомобиля')
parserArgs.add_argument('--start', type=int, default=1, help='Начальная марка')
parserArgs.add_argument('--end', type=int, default=1, help='Конечная марка')
args = parserArgs.parse_args()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--disable-extensions")

bigBrands = ['audi', 'bmw', 'chevrolet', 'ford', 'honda', 'hyundai', 'kia', 'lexus', 'mazda', 'mercedes-benz',
             'mitsubishi', 'nissan', 'opel', 'renault', 'skoda', 'subaru', 'suzuki', 'toyota', 'volkswagen', 'lada'];
brands = ['acura', 'alfa_romeo', 'aston_martin', 'audi', 'bentley', 'bmw', 'brilliance', 'byd', 'cadillac', 'changan',
          'chery', 'chevrolet', 'chrysler', 'citroen', 'dacia', 'daewoo', 'daihatsu', 'datsun', 'dodge', 'dongfeng',
          'evolute', 'cheryexeed', 'faw', 'ferrari', 'fiat', 'ford', 'foton', 'gac', 'geely', 'genesis', 'gmc',
          'great_wall', 'hafei', 'haima', 'haval', 'honda', 'hummer', 'hyundai', 'infiniti', 'iran_khodro', 'isuzu',
          'jac', 'jaguar', 'jeep', 'kia', 'lamborghini', 'land_rover', 'lexus', 'lifan', 'lincoln', 'lotus',
          "maserati", "maybach", "mazda", "mclaren", "mercedes-benz", "mercury", "mini", "mitsubishi", "nissan", "omoda",
          "opel","peugeot", "pontiac", "porsche", "ram", "ravon", "renault", "rolls-royce", "rover", "saab", "scion",
          "seat", "skoda", "smart", "ssang_yong", "subaru", "suzuki", "tesla", "toyota", "volkswagen",
          "volvo", "vortex", "zotye", "bogdan", "gaz", "zaz", "izh", "lada", "luaz", "moskvitch", "tagaz", "uaz"]
carsData = [];
carsUrls = [];


def getTree(url):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    sleep(1)
    tree = html.fromstring(driver.page_source)
    #driver.close()
    return tree


# https://auto.drom.ru/toyota/all/page1/?minyear=1940&maxyear=1989
def getUrls(urlMain):
    treeMain = getTree(urlMain);

    countCars = treeMain.xpath('//*[@id="tabs"]/div/div/div/a[1]/text()')
    if len(countCars) > 0:
        countCars = countCars[0];
        countCars = countCars[0:countCars.find('о') - 1].replace(u'\xa0', u'')
        countCars = int(countCars)
        print('Найдено объявлений: ' + str(countCars))
    else:
        countCars = treeMain.xpath('//*[@id="tabs"]/div[1]/text()')
        if len(countCars) > 0:
            countCars = countCars[0];
            countCars = countCars[0:countCars.find('о') - 1].replace(u'\xa0', u'')
            countCars = int(countCars)
            print('Найдено объявлений: ' + str(countCars))
        else:
            countCars = 0
            print('Нет объявлений')

    COUNT_ITERATION = countCars // 20 + 1;
    #COUNT_ITERATION = 1;
    if COUNT_ITERATION > 100:
        COUNT_ITERATION = 100;
    print('Всего итераций: ' + str(COUNT_ITERATION) + ' (по 20 объявлений на странице)\n')

    for i in range(1, COUNT_ITERATION + 1, args.count_threads):
        threads = []
        isEnd = False;

        for j in range(0, args.count_threads):
            if i + j > COUNT_ITERATION:
                isEnd = True;
                break;

            url = urlMain.replace('page1', 'page' + str(i + j));
            print('Парсинг ссылок на странице ' + url);

            threads.append(threading.Thread(target=thread, args=(j, url,)))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        if isEnd:
            break;

    return carsUrls;


# https://auto.drom.ru/toyota/all/page1/?minyear=1940&maxyear=1989
def getCarsData(brand):
    carsData = [];
    carsUrls = [];

    if brand in bigBrands:
        for index in range(2000, 2025, 5):
            urlMain = 'https://auto.drom.ru/' + brand + '/all/page1/?minyear=' + str(index) + '&maxyear=' + str(index + 4);
            print('Применяется парсинг ссылок в диапазоне ' + str(index) + '-' + str(index + 4) + ' годов выпуска');
            carsUrls = getUrls(urlMain);
    else:
        urlMain = 'https://auto.drom.ru/' + brand + '/all/page1/';
        print('Применяется парсинг ссылок без диапазона годов выпуска');
        carsUrls = getUrls(urlMain);

    for i in range(len(carsUrls)):
        carsData.append({'Brand': brand, 'Url': carsUrls[i]['Url']});

    return carsData;


def thread(num, url):
    print('Запуск потока ' + str(num + 1));

    tree = getTree(url);

    urls = tree.xpath('//a[@data-ftid="bulls-list_bull"]/@href')
    for url in urls:
        carsUrls.append({'Url': url});

    print('Завершение потока ' + str(num + 1));
    return;

def saveData():
    now = datetime.datetime.now();
    dfOutput = pd.DataFrame(carsData);
    dfOutput = dfOutput.drop_duplicates(subset=['Url']);
    print('Всего выявлено ссылок: ' + str(len(carsData)));
    print('Всего уникальных ссылок: ' + str(len(dfOutput)));
    dfOutput.to_csv('./prefetch_cars/prefetch_cars_' + args.brand + '_' + str(args.start) + '_' + str(args.end) + '_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=True, index_label='Id');
    print('\nСохранено в файл ./prefetch_cars/prefetch_cars_' + args.brand + '_' + str(args.start) + '_' + str(args.end) + '_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');


# ./prefetch.py --count_threads 5 --brand toyota --start 1 --end 92
if __name__ == '__main__':
    inputBrand = args.brand;
    nowBrand = "";
    nowIndex = 0;

    while True:
        try:
            print('Скрипт запущен в', datetime.datetime.now(), '\n')

            if inputBrand == '':
                if nowIndex == 0:
                    for i in range(args.start, args.end + 1):
                        nowBrand = brands[i];
                        print('----------------------------------------');
                        print('Парсинг марки ' + nowBrand);
                        newCarsData = getCarsData(nowBrand);
                        carsData = carsData + newCarsData;
                        print('----------------------------------------\n');
                        nowIndex = i;
                else:
                    for i in range(nowIndex, args.end):
                        nowBrand = brands[i];
                        print('----------------------------------------');
                        print('Парсинг марки ' + nowBrand);
                        newCarsData = getCarsData(nowBrand);
                        carsData = carsData + newCarsData;
                        print('----------------------------------------\n');
                        nowIndex = i;
            else:
                print('----------------------------------------');
                print('Парсинг марки ' + inputBrand);
                carsData = getCarsData(inputBrand);
                print('----------------------------------------\n');

            print('Скрипт завершил свою работу');

            saveData();

            winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
            input('\nНажмите Enter для выхода...');
            break;

        except BaseException as e:
            print('Ошибка при парсинге')
            print(e)
            saveData();
            print('Перезапуск скрипта')
            continue
