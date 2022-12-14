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
parserArgs.add_argument('--input', type=str, default='', help='Путь к входным данным')
parserArgs.add_argument('--start', type=int, default=0, help='Начальная позиция')
parserArgs.add_argument('--end', type=int, default=0, help='Конечная позиция')
args = parserArgs.parse_args()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

carsData = []
ITERATION = 0;
COUNT_ITERATION = args.end - args.start + 1;


def getTree(url):
    driver.get(url)
    sleep(1)
    tree = html.fromstring(driver.page_source)
    return tree


def parsingOnce(tree, url):
    print('Парсинг ссылки ' + url);

    brand = tree.xpath('/html/body/div[2]/div[2]/div[2]/div/div/div/div[3]/a/span/text()')
    if len(brand) > 0:
        brand = brand[0]
    else:
        brand = ''

    model = tree.xpath('/html/body/div[2]/div[2]/div[2]/div/div/div/div[4]/a/span/text()')
    if len(model) > 0:
        model = model[0]
    else:
        model = ''

    price = tree.xpath('/html/body/div/div/div/div/div/div[2]/div[1]/div[1]/text()')
    if len(price) > 0:
        price = price[0]
    else:
        price = ''

    region = tree.xpath('/html/body/div/div/div/div/div/div[2]/div/div/span[contains(text(),"Город")]//parent::div/text()')
    if len(region) > 0:
        region = region[0];
        if region.find(',') > 0:
            region = region[0:region.find(',')]
    else:
        region = ''

    year = tree.xpath('/html/body/div/div/div/h1/span/text()')
    if len(year) > 0:
        year = year[0].split(',');
        year = year[len(year) - 1];
        year = year[1:year.find('г') - 1];
    else:
        year = ''

    result = {}

    table = tree.xpath('//table/tbody/tr');
    for row in table:
        key = row.xpath('th/text()')
        if len(key) > 0:
            key = key[0]
        else:
            # break;
            continue;

        if key == 'Двигатель' or key == 'Мощность' or key == 'Пробег, км':
            value = row.xpath('td/span/text()')
        elif key == 'Поколение' or key == 'Комплектация':
            value = row.xpath('td/a/text()')
        else:
            value = row.xpath('td/text()')

        if len(value) > 0:
            result[key] = value[0]
        else:
            result[key] = ''

    isSold = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/span/text()')
    if len(isSold) > 0:
        result['Продано'] = '1'
    else:
        result['Продано'] = '0'

    carData = {
        'Url': url,
        'Brand': brand,
        'Model': model,
        'Region': region,
        'Year': year,
        'Engine': '',
        'EngineVolume': '',
        'Power': '',
        'Transmission': '',
        'Drive': '',
        'Body': '',
        'Color': '',
        'Mileage': '',
        'Wheel': '',
        'Generation': '',
        'Complectation': '',
        'IsSold': '',
        'Price': ''
    }

    if 'Двигатель' in result:
        if result['Двигатель'].find(',') >= 0:
            carData['Engine'] = result['Двигатель'][0:result['Двигатель'].find(',')]
            carData['EngineVolume'] = result['Двигатель'][result['Двигатель'].find(',') + 2:result['Двигатель'].find('.') + 2]
        else:
            if result['Двигатель'].find('.') >= 0:
                carData['Engine'] = ''
                carData['EngineVolume'] = result['Двигатель'][0:result['Двигатель'].find('.') + 2]
            else:
                carData['Engine'] = result['Двигатель']
                carData['EngineVolume'] = ''

    if 'Мощность' in result:
        carData['Power'] = result['Мощность']

    if 'Коробка передач' in result:
        carData['Transmission'] = result['Коробка передач']

    if 'Привод' in result:
        carData['Drive'] = result['Привод']

    if 'Тип кузова' in result:
        carData['Body'] = result['Тип кузова']

    if 'Цвет' in result:
        carData['Color'] = result['Цвет']

    if 'Пробег, км' in result:
        carData['Mileage'] = result['Пробег, км'].replace(u'\xa0', u'')

    if 'Руль' in result:
        carData['Wheel'] = result['Руль']

    if 'Поколение' in result:
        carData['Generation'] = result['Поколение']

    if 'Комплектация' in result:
        carData['Complectation'] = result['Комплектация']

    if 'Продано' in result:
        carData['IsSold'] = result['Продано']

    carData['Price'] = price.replace(u'\xa0', u'')

    return carData;

def saveData(df):
    for car in carsData:
        if car['Price'] == '':
            carsData.remove(car)

    print('Всего входных записей: ' + str(COUNT_ITERATION));
    print('Удалось получить: ' + str(len(carsData)));

    if len(carsData) > 0:
        now = datetime.datetime.now();
        dfOutput = df.copy(deep=True);
        dfOutput = dfOutput.drop(labels=['Brand'], axis=1);
        dfOutput = dfOutput.merge(pd.DataFrame(carsData), how='right', on=['Url']);
        dfOutput.to_csv('./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=False);
        print('Сохранено в файл ./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');
    else:
        print('\nНет данных для сохранения');


# ./parse.py --input ./prefetch_cars/prefetch_cars.csv --start 0 --end 216324
if __name__ == '__main__':
    isErrorAgain = False;
    MAXRETRYCAR = 1;
    MAXRETRYCARS = 3;

    while True:
        try:
            if args.input == '':
                raise Exception('Не указан путь к данным!\n')

            print('Скрипт запущен в', datetime.datetime.now())
            print('Всего итераций: ' + str(COUNT_ITERATION));
            print('Примерное время выполнения: ' + str((COUNT_ITERATION * 2) / 60) + ' минут\n');

            print('Чтение данных из файла ' + args.input + '\n');
            dfInput = pd.read_csv(args.input);
            urls = dfInput.Url;

            dfDiff = pd.read_csv('diff_cars.csv');
            idDiff = dfDiff['Id'].tolist();

            retryCars = 0;
            for i in range(args.start + ITERATION, args.end + 1):
                if i not in idDiff:
                    ITERATION += 1;
                    continue;

                if len(carsData) == 1000:
                    saveData(dfInput);
                    carsData = [];

                tree = getTree(urls[i]);
                res = parsingOnce(tree, urls[i]);

                if res['Price'] == '':
                    retryCars += 1;
                else:
                    retryCars = 0;

                if retryCars > MAXRETRYCAR:
                    retryCars = 0;
                    print('Превышено количество повторных попыток получения данных об машинах. Остановка на 3 минуты \n');
                    sleep(180);

                retryCar = 0;
                while res['Price'] == '' and retryCar < MAXRETRYCAR:
                    print('Повторная попытка получения данных...\n');
                    tree = getTree(urls[i]);
                    res = parsingOnce(tree, urls[i]);
                    retryCar += 1;

                carsData.append(res);
                print('Выполнена итерация [' + str(ITERATION + 1) + '/' + str(COUNT_ITERATION) + ']');
                print('Осталось времени: ' + str(((COUNT_ITERATION - ITERATION + 1) * 2) / 60) + ' минут\n');
                ITERATION += 1;

            saveData(dfInput);

            winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
            driver.quit()
            input('\nНажмите Enter для выхода...');
            break;

        except BaseException as e:
            print('Ошибка при парсинге')
            print(e)
            saveData(dfInput);

            if isErrorAgain:
                winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
                driver.quit()
                input('\nНажмите Enter для выхода...');
                break;

            print('Перезапуск скрипта')
            isErrorAgain = True;
            continue
