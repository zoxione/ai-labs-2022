import argparse
import math

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

np.seterr(divide='ignore', invalid='ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=str, default='', help='Режим работы приложения')
parser.add_argument('--dataset', type=str, default='', help='Путь к набору данных')
parser.add_argument('--model', type=str, default='', help='Путь к модели')
parser.add_argument('--input', type=str, default='', help='Путь к входным данным')
parser.add_argument('--output', type=str, default='', help='Путь к выходным данным')
args = parser.parse_args()

# Инициализация значений
propertyList = []
K_VALUE = 0.62
chooseProperty = ['OverallQual', 'GrLivArea', 'ExterQual', 'KitchenQual', 'GarageCars', 'GarageArea'];




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


def trainMode():
    print('Выбран режим train - обучение модели\n');

    # Считываем данные как dataframe
    print('[1] Считываем данные из файла', args.dataset);
    dfTrain = pd.read_csv(args.dataset);
    dfTrainCopy = df_string_to_number(dfTrain)
    dfTrainCopy['SalePrice'] = dfTrain['SalePrice']
    print('[2] Считанные данные обработаны');

    X = dfTrainCopy[chooseProperty]
    Y = dfTrainCopy.SalePrice

    print('[3] Обучение модели');
    # Обучать будем на 70% данных, проверять на 30%
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    # Обучение модели и получение предсказания
    model = LinearRegression()
    model.fit(X_train, y_train)
    print('[4] Модель обучена');

    # Сохранение модели
    joblib.dump(model, args.model)
    print('[5] Модель сохранена в файле', args.model);


def inferenceMode():
    print('Выбран режим inference - применение модели\n');

    print('[1] Чтение модели из файла', args.model);
    model = joblib.load(args.model);
    print('[2] Чтение данных из файла', args.input);
    dfInput = pd.read_csv(args.input);
    dfInputCopy = df_string_to_number(dfInput)
    dfInputCopy = dfInputCopy[chooseProperty]
    print('[3] Данные обработаны');

    print('[4] Предсказание модели на указанных данных');
    pred = model.predict(dfInputCopy)
    pred = pred.astype(int)
    dfInputCopy.drop(chooseProperty, axis=1, inplace=True)
    dfInputCopy['Id'] = dfInput['Id']
    dfInputCopy['SalePrice'] = pred
    dfInputCopy.to_csv(args.output, index=False)
    print('[5] Предсказание сделано и записано в файл ' + args.output);


def exitMode():
    input('\nНажмите Enter для выхода...');


# ./main.py --mode train --dataset ./train.csv --model ./modelLinearRegression.pkl
# ./main.py --mode inference --model ./modelLinearRegression.pkl --input ./train.csv --output ./result_to_commit.csv

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
    finally:
        exitMode();
