import argparse
import math

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

np.seterr(divide='ignore', invalid='ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--ground_truth', type=str, default='', help='Путь к набору данных')
parser.add_argument('--predictions', type=str, default='', help='Путь к предсказанным данным')
args = parser.parse_args()

# Инициализация значений
propertyList = []
K_VALUE = 0.62
chooseProperty = ['OverallQual', 'GrLivArea', 'ExterQual', 'KitchenQual', 'GarageCars', 'GarageArea'];

# Функция для подсчета средней квадратичной ошибки
def rmsle(y_true, y_pred):
   assert len(y_true) == len(y_pred)
   return np.square(np.log(y_pred + 1) - np.log(y_true + 1)).mean() ** 0.5

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


def exitMode():
    input('\nНажмите Enter для выхода...');

# ./evaluate.py --ground_truth ./train.csv  --predictions ./result_to_commit.csv

if __name__ == '__main__':
    try:
        print('[1] Чтение обучающих данных из файла', args.ground_truth);
        dfTrain = pd.read_csv(args.ground_truth);
        print('[2] Чтение предсказанных данных из файла', args.predictions);
        dfPredict = pd.read_csv(args.predictions);
        print('[3] Обучающие данные и предсказанные данные обработаны');

        X = dfTrain.SalePrice;
        Y = dfPredict.SalePrice;

        # Среднее абсолютное отклонение
        mae = mean_absolute_error(X, Y)
        print("[4] mae: " + str(mae))

        # Средняя квадратичная ошибка
        result = rmsle(X, Y)
        print("[5] rmsle: " + str(result))

        # Accuracy
        accuracy = accuracy_score(X, Y)
        print("[6] Accuracy: " + str(accuracy))

        # Confusion Matrix
        confusion_matrix = confusion_matrix(X, Y)
        print("[7] Confusion Matrix: " + str(confusion_matrix))

    except Exception as e:
        print(e)
    finally:
        exitMode();
