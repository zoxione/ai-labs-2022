import datetime
import argparse
import os
import json
import pandas as pd
import winsound


parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--input', type=str, default='', help='Путь к входным данным')
parserArgs.add_argument('--corr', type=float, default=0.4, help='Коэффициент корреляции')
args = parserArgs.parse_args()

chooseProperty = ['Id', 'Url']
corrValues = {}


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def df_char_to_number(df):
    dfCopy = df.copy(deep=True)

    # Преобразование char в int
    for column in ['Id', 'Year', 'Power', 'Mileage', 'IsSold', 'Price']:
        dfCopy[column] = pd.to_numeric(dfCopy[column], errors='coerce', downcast='signed')
        dfCopy = dfCopy.fillna(0)
        dfCopy[column] = pd.to_numeric(dfCopy[column], errors='raise', downcast='signed')

    # Преобразование char в float
    for column in ['EngineVolume']:
        dfCopy[column] = pd.to_numeric(dfCopy[column], errors='coerce', downcast='float')
        dfCopy = dfCopy.fillna(0)
        dfCopy[column] = pd.to_numeric(dfCopy[column], errors='raise', downcast='float')

    # Удаление строк без цены
    dfCopy = dfCopy[dfCopy['Price'] > 0]

    return dfCopy


# Функция для преобразования строк в числа в DataFrame
def df_factorize(df):
    dfCopy = df.copy(deep=True)

    # Сохрание значений в файл
    uniques = {}
    for column in ['Brand', 'Model', 'Region', 'Engine', 'Transmission', 'Drive', 'Body', 'Color', 'Wheel', 'Generation', 'Complectation']:
        uniques[column] = dfCopy[column].unique().tolist()
    with open('uniques.json', 'w') as fp:
        json.dump(uniques, fp)

    # Замена строковых значений на числовые
    for column in ['Brand', 'Model', 'Region', 'Engine', 'Transmission', 'Drive', 'Body', 'Color', 'Wheel', 'Generation', 'Complectation']:
        dfCopy[column] = pd.factorize(dfCopy[column])[0] + 1

    return dfCopy


def save_diff(df):
    dfPrefetch = pd.read_csv('./prefetch_cars/prefetch_cars.csv')
    dfDiff = dfPrefetch.merge(df, how='left', on=['Id'], indicator=True).query("_merge == 'left_only'")['Id']
    dfDiff.to_csv('diff_cars.csv', index=False)


# ./normalize.py --input ./cars
if __name__ == '__main__':
    try:
        if args.input == '':
            raise Exception('Не указан путь к данным!\n')

        inputFiles = [];
        for file in files(args.input):
            inputFiles.append(file)

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(len(inputFiles) - 1) + '\n')

        dfInput1 = pd.read_csv(args.input + '/' + inputFiles[0])

        for i in range(1, len(inputFiles)):
            dfInput2 = pd.read_csv(args.input + '/' + inputFiles[i])

            # Удаляем пустые значения
            dfInput1 = dfInput1.fillna(0)
            dfInput2 = dfInput2.fillna(0)
            # dfInput1 = dfInput1.dropna()
            # dfInput2 = dfInput2.dropna()

            dfInput1 = pd.concat([dfInput1, dfInput2], ignore_index=True)
            print('Выполнена итерация [' + str(i) + '/' + str(len(inputFiles) - 1) + ']');

        # Сортируем по Id
        dfOutputDefault = dfInput1.sort_values(by=['Id'])

        # Сравниваем с prefetch_cars.csv и сохраняем разницу
        save_diff(dfOutputDefault)

        # Преобразуем в числа
        dfOutputDefault = df_char_to_number(dfOutputDefault)
        dfOutputDefault = dfOutputDefault.drop_duplicates(subset=['Url'], keep='first')
        dfOutputNum = df_factorize(dfOutputDefault)
        dfOutputDefault.to_csv('./cars/cars.csv', index=False);
        print('\nСохранено в файл ./cars/cars.csv');

        # Получаем коэффициенты корреляции
        for column in ['Brand', 'Model', 'Region', 'Year', 'Engine', 'EngineVolume', 'Power', 'Transmission', 'Drive', 'Body', 'Color', 'Mileage', 'Wheel', 'Generation', 'Complectation', 'IsSold']:
            corr = dfOutputNum[column].corr(dfOutputNum['Price'], method='pearson')
            corrValues[column] = corr
            if corr >= args.corr or corr <= -args.corr:
                chooseProperty.append(column)

        print('\nКоэффициенты корреляции:')
        for key, value in corrValues.items():
            print(str(key) + ' - ' + str(value))
        print('Выбраны свойства(К=' + str(args.corr) +  '): ' + str(chooseProperty))

        # Сохраняем коэффициенты корреляции
        with open('corr_values.json', 'w') as fp:
            json.dump(corrValues, fp)

        chooseProperty.append('Price')
        dfOutputDefault = dfOutputDefault[chooseProperty]
        dfOutputNum = dfOutputNum[chooseProperty]

        # Сохраняем в файлы
        dfOutputDefault.to_csv('normalize_cars.csv', index=False);
        print('\nСохранено в файл normalize_cars.csv');
        dfOutputNum.to_csv('normalize_cars_numbers.csv', index=False);
        print('Сохранено в файл normalize_cars_numbers.csv');
        print('Всего записей: ' + str(len(dfOutputDefault)));

    except Exception as e:
        print('\nОшибка при выполнении программы: ' + str(e))

    finally:
        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        input('\nНажмите Enter для выхода...');
