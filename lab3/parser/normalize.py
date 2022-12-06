import datetime
import argparse

import numpy as np
import pandas as pd
import winsound
from selenium import webdriver
from lxml import html
from time import sleep
from selenium.webdriver.chrome.options import Options


parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--input', nargs='+', help='Пути к входным данным', required=True)
args = parserArgs.parse_args()

# Функция для преобразования строк в числа в DataFrame
def df_string_to_number(df):
   dfCopy = df.copy(deep=True)

   for column in dfCopy.columns.values.tolist():
      for property in propertyList:
         if column == property.name:
            for i in range(len(property.values)):
               dfCopy[column] = dfCopy[column].replace([property.values[i]], int(len(property.values) - i))
            break

      # Зануляем пустые значения
      dfCopy[column] = dfCopy[column].replace(np.nan, 0)

      # Зануляем строки, которых нет в параметрах
      for value in dfCopy[column]:
         if type(value) is str:
            dfCopy[column] = dfCopy[column].replace([value], 0)

   return dfCopy


#./normalize.py --input cars_20221206123816478055.csv cars_20221206123935723457.csv cars_20221206124944227138.csv
if __name__ == '__main__':
    try:
        if len(args.input) == 0:
            raise Exception('Не указан путь к данным!\n')

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(len(args.input)) + '\n')

        dfInput1 = pd.read_csv(args.input[0])
        for i in range(1, len(args.input)):
            dfInput2 = pd.read_csv(args.input[i])
            dfInput1 = pd.concat([dfInput1, dfInput2], ignore_index=True)
            print('Выполнена итерация [' + str(i) + '/' + str(len(args.input)) + ']');

    except Exception as e:
        print('\nОшибка при выполнении программы: ' + str(e))

    finally:
        now = datetime.datetime.now();
        dfInput1.to_csv('normalize_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=False);
        print('\nСохранено в файл normalize_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');

        #winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        input('\nНажмите Enter для выхода...');