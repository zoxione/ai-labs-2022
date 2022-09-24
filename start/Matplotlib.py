import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import requests

# https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?end=2021&locations=CN-US&start=2000&view=chart
countries = {
    'China': [1.21, 1.34, 1.47, 1.66, 1.96, 2.29, 2.75, 3.55, 4.59, 5.1, 6.09, 7.55, 8.53, 9.57, 10.48, 11.06, 11.23, 12.31, 13.89, 14.28, 14.69, 17.73],
    'United States': [10.25, 10.58, 10.93, 11.46, 12.22, 13.04, 13.82, 14.47, 14.77, 14.48, 15.05, 15.6, 16.25, 16.84, 17.55, 18.21, 18.7, 19.48, 20.53, 21.37, 20.89, 23],
    'Russian Federation': [0.259, 0.3, 0.34, 0.43, 0.59, 0.76, 0.98, 1.3, 1.66, 1.22, 1.52, 2.05, 2.21, 2.29, 2.06, 1.36, 1.28, 1.57, 1.66, 1.69, 1.49, 1.78],
    'Germany': [1.95, 1.95, 2.08, 2.5, 2.81, 2.85, 2.99, 3.43, 3.75, 3.41, 3.4, 3.75, 3.53, 3.73, 3.89, 3.36, 3.47, 3.69, 3.98, 3.89, 3.85, 4.22],
    'Japan': [4.97, 4.37, 4.18, 4.52, 4.83, 4.83, 4.6, 4.58, 5.11, 5.29, 5.76, 6.23, 6.27, 5.21, 4.9, 4.4, 5.0, 4.93, 5.04, 5.12, 5.04, 4.94],
}

API_KEY = "5a1bad8482f1201fa279d16731030c36"
CITY_NAME = "Taganrog"
LAT = 0
LON = 0
TEMP_LIST = []

try:
    res = requests.get("http://api.openweathermap.org/geo/1.0/direct", params={'q': CITY_NAME, 'appid': API_KEY, 'limit': 1})
    data = res.json()
    LAT = data[0]['lat']
    LON = data[0]['lon']
except Exception as e:
    print("Exception (direct):", e)
    pass

try:
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={'lat': LAT, 'lon': LON, 'appid': API_KEY, 'cnt': 16, 'units': 'metric', 'lang': 'ru'})
    data = res.json()
    for item in data['list']:
        TEMP_LIST.append(item['main']['temp'])
except Exception as e:
    print("Exception (weather):", e)
    pass

print(TEMP_LIST)


# Создание фигуры
fig = plt.figure()


# Создание графика 1
ax1 = fig.add_subplot(2, 1, 1)
ax1.set_title('ВВП стран мира')
ax1.set_xlabel('года')
ax1.set_ylabel('ввп')
ax1.set_xlim([2000, 2021])
ax1.set_xticks(np.arange(2000, 2021, 2))
ax1.set_ylim([0, 30])
ax1.grid()

x = np.linspace(2000, 2021, 22)
countriesNames = list(countries.keys())
for item in countries:
    ax1.plot(x, countries[item], label=item)
    ax1.scatter(x, countries[item], marker='.')
ax1.legend()


# Создание графика 2
ax2 = fig.add_subplot(2, 2, 3)
ax2.set_title('Сердце')

ax2.plot([5, 10, 9, 6, 5, 4, 1, 0, 5], [5, 12, 14, 14, 12, 14, 14, 12, 5], 'r')


# Создание графика 3
ax3 = fig.add_subplot(2, 2, 4)
ax3.set_title('Погода в Таганроге')
ax3.set_xlabel('дни')
ax3.set_ylabel('температура')
ax3.grid(axis = 'y', color = 'k')

x = np.arange(1, TEMP_LIST.__len__() + 1)
ax3.bar(x, TEMP_LIST, color = 'green')


# Вывод графиков
plt.suptitle('Matplotlib')
plt.show()
