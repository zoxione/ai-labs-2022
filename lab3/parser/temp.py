import datetime
import os

import pandas as pd


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


if __name__ == '__main__':
    inputFiles = [];
    for file in files('./cars'):
        inputFiles.append(file)

    print('Всего итераций: ' + str(len(inputFiles) - 1) + '\n')

    dfInput1 = pd.read_csv('./cars' + '/' + inputFiles[0])

    for i in range(1, len(inputFiles)):
        dfInput2 = pd.read_csv('./cars'+ '/' + inputFiles[i])

        # Удаляем пустые значения
        dfInput1 = dfInput1.fillna(0)
        dfInput2 = dfInput2.fillna(0)
        # dfInput1 = dfInput1.dropna()
        # dfInput2 = dfInput2.dropna()

        dfInput1 = pd.concat([dfInput1, dfInput2], ignore_index=True)
        print('Выполнена итерация [' + str(i) + '/' + str(len(inputFiles) - 1) + ']')

    dfPrefetch = pd.read_csv('./prefetch_cars' + '/' + 'prefetch_cars.csv')
    dfPrefetch = dfPrefetch.drop(labels=['Brand'], axis=1)

    dfInput1 = dfInput1.drop(labels=['Id'], axis=1)

    dfInput1 = dfPrefetch.merge(dfInput1, how='inner', on=['Url'])
    dfInput1 = dfInput1.drop_duplicates(subset=['Id'])
    now = datetime.datetime.now();
    dfInput1.to_csv('./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=False);
    print('Сохранено в файл ./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');

    print(dfInput1)
