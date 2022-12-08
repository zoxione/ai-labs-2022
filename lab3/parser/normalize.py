import datetime
import argparse
import os
import json
import pandas as pd
import winsound


parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--input', type=str, default='', help='Путь к входным данным')
args = parserArgs.parse_args()

chooseProperty = ['Id', 'Url', 'Brand', 'Model', 'Year', 'EngineVolume', 'Power', 'Drive', 'Mileage', 'Price', 'Region', 'Engine', 'Transmission']


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


# Функция для преобразования строк в числа в DataFrame
def df_to_number(df):
    dfCopy = df.copy(deep=True)

    dfCopy['Year'] = dfCopy['Year'].apply(int)
    dfCopy['Power'] = dfCopy['Power'].apply(int)
    dfCopy['Mileage'] = pd.to_numeric(dfCopy['Mileage'], errors='coerce')
    dfCopy['Mileage'] = dfCopy['Mileage'].fillna(0)
    dfCopy['Price'] = dfCopy['Price'].apply(int)

    # Save unique values
    uniques = {}
    uniques['Brand'] = dfCopy['Brand'].unique().tolist()
    uniques['Model'] = dfCopy['Model'].unique().tolist()
    uniques['Region'] = dfCopy['Region'].unique().tolist()
    uniques['Engine'] = dfCopy['Engine'].unique().tolist()
    uniques['Transmission'] = dfCopy['Transmission'].unique().tolist()
    uniques['Drive'] = dfCopy['Drive'].unique().tolist()

    # Replace values
    dfCopy['Brand'] = pd.factorize(dfCopy['Brand'])[0] + 1 
    dfCopy['Model'] = pd.factorize(dfCopy['Model'])[0] + 1 
    dfCopy['Region'] = pd.factorize(dfCopy['Region'])[0] + 1 
    dfCopy['Engine'] = pd.factorize(dfCopy['Engine'])[0] + 1 
    dfCopy['Transmission'] = pd.factorize(dfCopy['Transmission'])[0] + 1 
    dfCopy['Drive'] = pd.factorize(dfCopy['Drive'])[0] + 1 
    #dfCopy['Body'] = pd.factorize(dfCopy['Body'])[0] + 1 
    #dfCopy['Color'] = pd.factorize(dfCopy['Color'])[0] + 1 
    #dfCopy['Wheel'] = pd.factorize(dfCopy['Wheel'])[0] + 1

    with open('uniques.json', 'w') as fp:
        json.dump(uniques, fp)

    return dfCopy


# ./normalize.py --input ./cars
if __name__ == '__main__':
    try:
        if args.input == '':
            raise Exception('Не указан путь к данным!\n')

        inputFiles = [];
        for file in files(args.input):
            inputFiles.append(file)

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(len(inputFiles)) + '\n')

        dfInput1 = pd.read_csv(args.input + '/' + inputFiles[0])
        dfInput1 = dfInput1[chooseProperty]
        for i in range(1, len(inputFiles)):
            dfInput2 = pd.read_csv(args.input + '/' + inputFiles[i])
            dfInput2 = dfInput2[chooseProperty]

            # Удаляем пустые значения
            # dfInput1 = dfInput1.fillna(0)
            # dfInput2 = dfInput2.fillna(0)
            dfInput1 = dfInput1.dropna()
            dfInput2 = dfInput2.dropna()

            dfInput1 = pd.concat([dfInput1, dfInput2], ignore_index=True)
            print('Выполнена итерация [' + str(i) + '/' + str(len(inputFiles) - 1) + ']');

        # Удаляем дубликаты
        dfInput1 = dfInput1.drop_duplicates(subset=['Url'], keep='first')

        # dfTemp = dfInput1.duplicated['Url']
        # dfInput1 = dfInput1[~dfTemp]

        # Сортируем по Id
        dfInput1 = dfInput1.sort_values(by=['Id'])

        # Сравниваем с prefetch_cars.csv
        dfPrefetch = pd.read_csv('./prefetch_cars/prefetch_cars.csv')
        dfDiff = dfPrefetch.merge(dfInput1, how='left', on=['Id'], indicator=True).query("_merge == 'left_only'")['Id']
        dfDiff.to_csv('diff_cars.csv', index=False)

        # Сохраняем в файл
        dfInput1.to_csv('normalize_cars.csv', index=False);
        print('\nСохранено в файл normalize_cars.csv');
        print('Всего записей: ' + str(len(dfInput1)))

        # Преобразуем в числа
        dfInput1 = df_to_number(dfInput1)

    except Exception as e:
        print('\nОшибка при выполнении программы: ' + str(e))

    finally:
        now = datetime.datetime.now();
        dfInput1.to_csv('normalize_cars_numbers.csv', index=False);
        print('\nСохранено в файл normalize_cars_numbers.csv');

        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        input('\nНажмите Enter для выхода...');
