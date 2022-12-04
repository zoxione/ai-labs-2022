import datetime
import argparse
import pandas as pd
from pydantic import BaseModel
from selenium import webdriver
from lxml import html
from time import sleep
import os
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--input', type=str, default='', help='Путь к входным данным')
args = parserArgs.parse_args()


chrome_options = Options()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=chrome_options)

MAX_ITERATION = 200
carsData = []


def getTree(url):
    driver.get(url)
    sleep(1)
    tree = html.fromstring(driver.page_source)
    return tree


def parsingOnce(tree, url):
    print('\nПарсинг ссылки ', url);

    result = {}

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

    isSold = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[1]/div[1]/span/text()')
    if len(isSold) > 0:
        print('Автомобиль продан')

        price = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/text()')
        if len(price) > 0:
            price = price[0]
        else:
            price = ''

        region = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[2]/div[4]/div[2]/text()')
        if len(region) > 0:
            region = region[0]
            region = region[0:region.find(',')]
        else:
            region = ''

        for i in range(0, 11):
            key = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/th/text()')
            if len(key) > 0:
                key = key[0]
            else:
                key = ''

            if key == 'Поколение' or key == 'Комплектация':
                value = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td/a/text()')
            elif key == 'Двигатель' or key == 'Мощность' or key == 'Пробег, км' or key == 'Поколение':
                value = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td/span/text()')
            else:
                value = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[3]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td/text()')

            if len(value) > 0:
                value = value[0]
            else:
                value = ''

            if len(key) > 0:
                result[key] = value

    else:
        price = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/text()')
        if len(price) > 0:
            price = price[0]
        else:
            price = ''

        region = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[4]/div[2]/text()')
        if len(region) > 0:
            region = region[0]
            if region.find(',') > 0:
                region = region[0:region.find(',')]
        else:
            region = ''

        for i in range(0, 11):
            key = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/th/text()')
            if len(key) > 0:
                key = key[0]
            else:
                key = ''

            if key == 'Поколение' or key == 'Комплектация':
                value = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td/a/text()')
            elif key == 'Двигатель' or key == 'Мощность' or key == 'Пробег, км' or key == 'Поколение':
                value = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td/span/text()')
            else:
                value = tree.xpath('/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(i) + ']/td/text()')

            if len(value) > 0:
                value = value[0]
            else:
                value = ''

            if len(key) > 0:
                result[key] = value

    carData = {
        'Url': url,
        'Brand': brand,
        'Model': model,
        'Region': region,
        'Engine': result['Двигатель'][0:result['Двигатель'].find(',')] if ('Двигатель' in result) else '',
        'Engine_volume': result['Двигатель'][result['Двигатель'].find(',')+2:result['Двигатель'].find('.')+2] if ('Двигатель' in result) else '',
        'Power': result['Мощность'] if ('Мощность' in result) else '',
        'Transmission': result['Коробка передач'] if ('Коробка передач' in result) else '',
        'Drive_unit': result['Привод'] if ('Привод' in result) else '',
        'Color': result['Цвет'] if ('Цвет' in result) else '',
        'Mileage': result['Пробег, км'].replace(u'\xa0', u'') if ('Пробег, км' in result) else '',
        'Rudder': result['Руль'] if ('Руль' in result) else '',
        'Generation': result['Поколение'] if ('Поколение' in result) else '',
        'Equipment': result['Комплектация'] if ('Комплектация' in result) else '',
        'Body': result['Тип кузова'] if ('Тип кузова' in result) else '',
        'Price': price.replace(u'\xa0', u''),
    }

    print(carData)
    return carData;

#./parse.py --input prefetch_cars_2022-12-04-21-09-12.csv
if __name__ == '__main__':
    try:
        if args.input == '':
            raise Exception('Не указан путь к данным!')

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(MAX_ITERATION) + '\n');

        print('Чтение данных из файла ' + args.input);
        dfInput = pd.read_csv(args.input);
        urls = dfInput.Url;

        for i in range(0, MAX_ITERATION):
            tree = getTree(urls[i]);
            res = parsingOnce(tree, urls[i]);
            carsData.append(res);
            print('Выполнена итерация [' + str(i + 1) + '/' + str(MAX_ITERATION) + ']');

    except Exception as e:
        print('Ошибка при парсинге')
        print(e)

    finally:
        now = datetime.datetime.now();
        df = pd.DataFrame(carsData);
        df.to_csv('cars_' + now.strftime("%Y-%m-%d %H-%M-%S") + '.csv', index=True, index_label='Id');
        print('\nСохранено в файл cars_' + now.strftime("%Y-%m-%d-%H-%M-%S") + '.csv');

        driver.quit()
        input('\nНажмите Enter для выхода...');