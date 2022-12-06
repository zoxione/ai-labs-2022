import datetime
import argparse
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
        carData['Engine'] = result['Двигатель'][0:result['Двигатель'].find(',')]
        carData['EngineVolume'] = result['Двигатель'][result['Двигатель'].find(',')+2:result['Двигатель'].find('.')+2]

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


#./parse.py --input prefetch_cars_20221206122926365004.csv --start 0 --end 10
if __name__ == '__main__':
    try:
        if args.input == '':
            raise Exception('Не указан путь к данным!\n')

        ITERATION = 1;
        COUNT_ITERATION = args.end - args.start + 1;

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(COUNT_ITERATION));
        print('Примерное время выполнения: ' + str((COUNT_ITERATION * 2) / 60) + ' минут\n');

        print('Чтение данных из файла ' + args.input + '\n');
        dfInput = pd.read_csv(args.input);
        urls = dfInput.Url;

        # tree = getTree('https://arkadak.drom.ru/mercedes-benz/e-class/49140661.html');
        # res = parsingOnce(tree, 'https://arkadak.drom.ru/mercedes-benz/e-class/49140661.html');
        # carsData.append(res);
        #
        # tree = getTree('https://simferopol.drom.ru/lada/2107/48805472.html');
        # res = parsingOnce(tree, 'https://simferopol.drom.ru/lada/2107/48805472.html');
        # carsData.append(res);
        #
        # tree = getTree('https://moscow.drom.ru/toyota/passo/48967039.html');
        # res = parsingOnce(tree, 'https://moscow.drom.ru/toyota/passo/48967039.html');
        # carsData.append(res);

        for i in range(args.start, args.end + 1):
            tree = getTree(urls[i]);
            res = parsingOnce(tree, urls[i]);
            carsData.append(res);
            print('Выполнена итерация [' + str(ITERATION) + '/' + str(COUNT_ITERATION) + ']');
            print('Осталось времени: ' + str(((COUNT_ITERATION - ITERATION) * 2) / 60) + ' минут\n');
            ITERATION += 1;

    except Exception as e:
        print('Ошибка при парсинге')
        print(e)

    finally:
        now = datetime.datetime.now();
        dfOutput = dfInput.copy(deep=True);
        dfOutput = dfOutput.merge(pd.DataFrame(carsData), how='right', on=['Url']);
        dfOutput.to_csv('./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=False);
        print('Сохранено в файл ./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');

        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        driver.quit()
        input('\nНажмите Enter для выхода...');
