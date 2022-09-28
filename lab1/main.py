# Лабораторная работа 1
# Отхонов Баир КТбо3-8
# Бакухин Александр КТбо3-8


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_absolute_error



# Класс для хранения свойств
class Property:
   def __init__(self, name, values):
      self.name = name
      self.values = values
   name = ""
   values = []
   k = 0

# Инициализация
propertyList = []


def rmsle(y_true, y_pred):
   assert len(y_true) == len(y_pred)
   return np.square(np.log(y_pred + 1) - np.log(y_true + 1)).mean() ** 0.5

def read_file():
   with open("data_description.txt", "r") as f:
      for line in f.readlines():
         isName = False
         isValues = False

         if line.startswith("\n") or line.startswith("\t"):
            continue
         elif line.startswith(' '):
            isValues = True
         else:
            isName = True

         if isName == True:
            for word in line.split(':'):
               propertyList.append(Property(word, []))
               break
            continue
         elif isValues == True:
            cnt = 0
            for i in line:
               cnt += 1
               if i != ' ':
                  word = line[cnt - 1: line.find('\t')]
                  break
            propertyList[len(propertyList) - 1].values.append(word)


# Start
if __name__ == '__main__':
   # Чтение файла
   read_file()
   print(propertyList[0].name)

   # Считываем данные как dataframe
   dfTrain = pd.read_csv('./train.csv')
   print(dfTrain.head())

   # Получаем столбцы
   dfTabs = dfTrain.columns.values.tolist()

   # Получаем коэффициенты корреляции
   for tab in dfTabs:
      if tab != 'SalePrice' and tab != 'Id':
         k = (pd.to_numeric(dfTrain[tab], errors='coerce', downcast='integer')).corr(dfTrain['SalePrice'])

         for property in propertyList:
            if property.name == tab:
               property.k = k
               break

   # cnt = 0
   # for property in propertyList:
   #    if pd.isna(property.k) == False and property.k > 0.6:
   #       cnt += 1
   #       sns.set_style("darkgrid")
   #       plt.subplot(2, 3, cnt)
   #       sns.lineplot(data=df, x=property.name, y="SalePrice")

   # Отрисофка графиков
   sns.set_style("darkgrid")
   sns.pairplot(dfTrain[["SalePrice", "OverallQual", "TotalBsmtSF", "GrLivArea", "GarageCars", "GarageArea"]], height=2.5)


   for property in propertyList:
      print(property.name, property.k)

   #X = dfTrain[['LotArea', 'OverallQual', 'YearBuilt', 'TotRmsAbvGrd']]
   X = dfTrain[["SalePrice", "OverallQual", "TotalBsmtSF", "GrLivArea", "GarageCars", "GarageArea"]]
   Y = dfTrain.SalePrice

   # Разделение на train и validation
   # Обучать будем на 75% данных, проверять на 25%
   X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=42)
   # X_train = X_train
   # y_train = y_train
   # X_test = X_test
   # y_test = y_test

   # # Обучение модели и получение предсказания
   lr = LinearRegression()
   lr.fit(X_train, y_train)
   LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

   prediction = lr.predict(X_test)

   mae = mean_absolute_error(y_test, prediction)
   print(mae)
   # 57324.261901630831

   # Средняя абсолютная ошибка - 57к долларов для этой модели
   result = rmsle(y_test, prediction)
   print(result)
   # 0.40943121669338522


   plt.show()