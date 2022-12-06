import datetime
import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd
import winsound
from selenium import webdriver
from lxml import html
from time import sleep
from selenium.webdriver.chrome.options import Options


parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--input', type=str, default='', help='Путь к входным данным')
args = parserArgs.parse_args()

chooseProperty = ['Id', 'Url', 'Brand', 'Model', 'Year', 'EngineVolume', 'Power', 'Drive', 'Mileage', 'Price']


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

    # dfCopy = dfCopy[['Year', 'EngineVolume', 'Power', 'Drive', 'Mileage']]

    # for column in dfCopy.columns.values.tolist():
        # if

    return dfCopy


#./normalize.py --input ./cars
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

            # Зануляем пустые значения
            # dfInput1 = dfInput1.fillna(0)
            # dfInput2 = dfInput2.fillna(0)
            dfInput1 = dfInput1.dropna()
            dfInput2 = dfInput2.dropna()

            dfInput1 = pd.concat([dfInput1, dfInput2], ignore_index=True)
            print('Выполнена итерация [' + str(i) + '/' + str(len(inputFiles) - 1) + ']');

        # Удаляем дубликаты
        dfInput1 = dfInput1.drop_duplicates(subset=['Url']);

        # Сортируем по Id
        dfInput1 = dfInput1.sort_values(by=['Id'])

        # Преобразуем в числа
        dfInput1 = df_to_number(dfInput1)

    except Exception as e:
        print('\nОшибка при выполнении программы: ' + str(e))

    finally:
        now = datetime.datetime.now();
        dfInput1.to_csv('normalize_cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=False);
        print('\nСохранено в файл normalize_cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');

        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        input('\nНажмите Enter для выхода...');