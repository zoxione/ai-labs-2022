import joblib
import streamlit as st
import pandas as pd
from collections import Counter
import json


def getDataImportanceProperty():
    chooseProperty = []

    with open('../model/result_importance.json') as json_file:
        importanceProperty = json.load(json_file)

    for key in importanceProperty:
        if key != "IMPORTANCE_VALUE" and importanceProperty[key] > importanceProperty["IMPORTANCE_VALUE"]:
            chooseProperty.append(key)

    return chooseProperty


params = pd.read_csv(".\params.csv")
selection = dict()
params = params[getDataImportanceProperty()]


def buttonHandler():
    # Формирование данных для предсказания
    with open('../parser/uniques.json') as json_file:
        uniques = json.load(json_file)

    #st.write(selection)
    dfSelection = pd.DataFrame(selection, index=[0])
    for column in dfSelection.columns:
        if column in uniques:
            dfSelection[column] = uniques[column].index(selection[column])
    #st.write(dfSelection)

    # Предсказание модели на указанных данных
    model = joblib.load('../model/model_linearRegression.pkl');
    pred = model.predict(dfSelection)
    pred = pred.astype(int)

    price = pred[0]
    if price < 0:
        price = 0
    st.subheader('Предсказанная цена: ' + str(price) + ' рублей')


# streamlit run MainPage.py
if __name__ == "__main__":
    st.title("Предсказание цены на автомобиль")
    st.sidebar.markdown("Предсказание цены на автомобиль")

    st.subheader("Введите данные для предсказания: ")

    if 'Brand' in params.columns:
        selection["Brand"] = st.selectbox(
            "Выберите марку автомобиля",
            Counter(params["Brand"].sort_values())
        )

    if 'Model' in params.columns:
        selection["Model"] = st.selectbox(
            "Выберите модель автомобиля",
            Counter(params.loc[params["Brand"] == selection["Brand"]]["Model"].sort_values())
        )

    if 'Region' in params.columns:
        selection["Region"] = st.selectbox(
            "Выберите местонахождение автомобиля",
            Counter(params["Region"][~pd.isnull(params["Region"])].sort_values())
        )

    if 'Year' in params.columns:
        selection["Year"] = st.slider(
            "Выберите год выпуска автомобиля",
            min_value=2000,max_value=2022,step=1
        )

    if 'Engine' in params.columns:
        selection["Engine"] = st.radio(
            "Выберите тип двигателя",
            # without zero
            Counter(params["Engine"][params["Engine"] != "0"].sort_values())
        )

    if 'EngineVolume' in params.columns:
        selection["EngineVolume"] = st.selectbox(
            "Выберите объем двигателя",
            Counter(params["EngineVolume"][params["EngineVolume"] != 0.0].sort_values())
        )

    if 'Power' in params.columns:
        selection["Power"] = st.number_input("Введите количество лошадиных сил", min_value=1, max_value=1000, step=10)

    if 'Transmission' in params.columns:
        selection["Transmission"] = st.selectbox(
            "Выберите тип коробки передач",
            Counter(params["Transmission"][~pd.isnull(params["Transmission"])].sort_values())
        )

    if 'Drive' in params.columns:
        selection["Drive"] = st.radio(
            "Выберите привод автомобиля",
            Counter(params["Drive"][~pd.isnull(params["Drive"])].sort_values())
        )

    if 'Body' in params.columns:
        selection["Body"] = st.selectbox(
            "Выберите тип кузова",
            Counter(params["Body"][(params["Body"] != "0") & (params["Body"] != "0.0") ].sort_values())
        )

    if 'Color' in params.columns:
        selection["Color"] = st.selectbox(
            "Выберите цвет автомобиля",
            Counter(params["Color"][params["Color"] != "0"].sort_values())
        )

    if 'Mileage' in params.columns:
        selection["Mileage"] = st.number_input("Введите пробег автомобиля", min_value=0, max_value=1000000, step=1000)

    if 'Wheel' in params.columns:
        selection["Wheel"] = st.radio(
            "Выберите тип руля",
            Counter(params["Wheel"][params["Wheel"] != "0"].sort_values())
        )

    if 'Generation' in params.columns:
        selection["Generation"] = st.selectbox(
            "Выберите поколение автомобиля",
            Counter(params["Generation"][params["Generation"] != "0"].sort_values())
        )

    if 'Complectation' in params.columns:
        selection["Complectation"] = st.radio(
            "Выберите комплектацию автомобиля",
            Counter(params["Complectation"][~pd.isnull(params["Complectation"])].sort_values())
        )

    if 'IsSold' in params.columns:
        selection["IsSold"] = st.radio(
            "Продан ли автомобиль",
            ["Да", "Нет"]
        )
        selection["IsSold"] = 1 if selection["IsSold"] == "Да" else 0

    if st.button('Рассчитать'):
        buttonHandler()
