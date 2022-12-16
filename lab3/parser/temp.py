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

    dfInput1 = pd.read_csv('./cars/cars.csv')

    dfInput1 = dfInput1[(dfInput1['Engine'] == 'бензин') | (dfInput1['Engine'] == 'дизель') | (dfInput1['Engine'] == 'электро')| (dfInput1['Engine'] == '0')]

    for column in dfInput1.columns:
        print(column + ': ')
        print(pd.unique(dfInput1[column]))

    # for value in dfInput1['Engine']:
    #     if value == 'бензин' or value == 'дизель' or value == 'электро':
    #         break
    #     print(value)




    # dfInput1 = dfPrefetch.merge(dfInput1, how='inner', on=['Url'])
    # dfInput1 = dfInput1.drop_duplicates(subset=['Id'])
    now = datetime.datetime.now();
    dfInput1.to_csv('./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv', index=False);
    print('Сохранено в файл ./cars/cars_' + now.strftime('%Y%m%d%H%M%S%f') + '.csv');

    print(dfInput1)
