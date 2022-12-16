import argparse
import json

import joblib
import numpy as np
import pandas as pd
from matplotlib import pyplot
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
np.seterr(divide='ignore', invalid='ignore')


parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='', help='Режим работы приложения')
parser.add_argument('--dataset', type=str, default='', help='Путь к набору данных')
parser.add_argument('--model', type=str, default='', help='Путь к модели')
parser.add_argument('--input', type=str, default='', help='Путь к входным данным')
parser.add_argument('--output', type=str, default='', help='Путь к выходным данным')
args = parser.parse_args()

IMPORTANCE_VALUE = 4500


def getDataImportanceProperty():
    chooseProperty = []

    with open('result_importance.json') as json_file:
        importanceProperty = json.load(json_file)

    for key in importanceProperty:
        if importanceProperty[key] > IMPORTANCE_VALUE:
            chooseProperty.append(key)

    return chooseProperty


def trainMode():
    chooseProperty = []
    importanceProperty = {}

    print('Выбран режим train - обучение модели\n');

    # Считываем данные как dataframe
    print('[1] Считываем данные из файла', args.dataset);
    dfTrain = pd.read_csv(args.dataset);
    dfTrainCopy = dfTrain.copy(deep=True)
    dfTrainCopy = dfTrainCopy.drop(['Id', 'Url', 'Price'], axis=1)
    print('[2] Считанные данные обработаны');

    X = dfTrainCopy
    Y = dfTrain['Price']

    model = LinearRegression()
    model.fit(X, Y)

    print('[3] Вычисление важности свойств');
    print('Выбранные свойства: ')
    importance = model.coef_
    index = 0
    for column in dfTrainCopy.columns:
        if importance[index] > importanceValue:
            chooseProperty.append(column)
            print(column, importance[index])

        importanceProperty[column] = importance[index]
        index += 1

    X = X[chooseProperty]
    with open('result_importance.json', 'w') as fp:
        json.dump(importanceProperty, fp)

    print('[4] Обучение модели');
    # Обучать будем на 90% данных, проверять на 10%
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)

    # Обучение модели и получение предсказания
    # model = LogisticRegression(solver='liblinear', random_state=42, max_iter=1000, verbose=1)
    model = LinearRegression()
    model.fit(X_train, Y_train)
    print('[5] Модель обучена');

    # Оценка качества модели
    Y_train_pred = model.predict(X_train)
    Y_test_pred = model.predict(X_test)
    mseTrain = mean_squared_error(Y_train, Y_train_pred)
    mseTest = mean_squared_error(Y_test, Y_test_pred)
    print('[6] Оценка качества модели');
    print('MSE train: %.3f, test: %.3f' % (mseTrain, mseTest))
    print('RMSE train: %.3f, test: %.3f' % (np.sqrt(mseTrain), np.sqrt(mseTest)))
    score = model.score(X_test, Y_test)
    print('R2 score: %.3f' % score)

    # Сохранение модели
    joblib.dump(model, args.model)
    print('[6] Модель сохранена в файле', args.model);


def inferenceMode():
    print('\n\nВыбран режим inference - применение модели\n');

    print('[1] Чтение модели из файла', args.model);
    model = joblib.load(args.model);
    print('[2] Чтение данных из файла', args.input);
    dfInput = pd.read_csv(args.input);
    dfInputCopy = dfInput.copy(deep=True)
    dfInputCopy = dfInputCopy.drop(['Id', 'Url', 'Price'], axis=1)
    print('[3] Данные обработаны');


    chooseProperty = getDataImportanceProperty()
    dfInputCopy = dfInputCopy[chooseProperty]

    print('[4] Предсказание модели на указанных данных');
    pred = model.predict(dfInputCopy)
    pred = pred.astype(int)
    dfOutput = pd.DataFrame({'Id': dfInput['Id'], 'Price': pred})
    dfOutput.to_csv(args.output, index=False)
    print('[5] Предсказание сделано и записано в файл ' + args.output);


# def exitMode():
#     input('\nНажмите Enter для выхода...');


# ./model.py --mode train --dataset ./train.csv --model ./model_linearRegression.pkl
# ./model.py --mode inference --model ./model_linearRegression.pkl --input ./train.csv --output ./result_to_commit.csv
if __name__ == '__main__':
    try:
        if args.mode == 'train':
            trainMode();
        elif args.mode == 'inference':
            inferenceMode();
        elif args.mode == '':
            print('Не указан режим работы');
    except Exception as e:
        print(e)
    # finally:
    #     exitMode();
