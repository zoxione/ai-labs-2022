import datetime
import argparse
import os
import json
import pandas as pd
import winsound

parserArgs = argparse.ArgumentParser()
parserArgs.add_argument('--input', type=str, default='', help='Путь к входным данным')
args = parserArgs.parse_args()


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


# ./prefetch_concat.py --input ./prefetch_cars
if __name__ == '__main__':
    try:
        if args.input == '':
            raise Exception('Не указан путь к данным!\n')

        inputFiles = [];
        for file in files(args.input):
            inputFiles.append(file)

        print('Скрипт запущен в', datetime.datetime.now())
        print('Всего итераций: ' + str(len(inputFiles) - 1) + '\n')

        dfInput1 = pd.read_csv(args.input + '/' + inputFiles[0]).drop(['Id'], axis=1)
        for i in range(1, len(inputFiles)):
            dfInput2 = pd.read_csv(args.input + '/' + inputFiles[i]).drop(['Id'], axis=1)
            dfInput1 = pd.concat([dfInput1, dfInput2], ignore_index=True)
            print('Выполнена итерация [' + str(i) + '/' + str(len(inputFiles) - 1) + ']');

        dfOutput = dfInput1
        dfOutput.to_csv('./prefetch_cars/prefetch_cars.csv', index=True, index_label='Id')
        print('\nВсего строк: ' + str(len(dfOutput)))

    finally:
        winsound.PlaySound('SystemExit', winsound.SND_ALIAS)
        input('\nНажмите Enter для выхода...');
