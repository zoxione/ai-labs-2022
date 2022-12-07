import joblib
import streamlit as st
import pandas as pd
from collections import Counter
import json


params = pd.read_csv("./params.csv")
selection = dict()


def buttonHandler():
    # Формирование данных для предсказания
    with open('../parser/uniques.json') as json_file:
        uniques = json.load(json_file)

    # st.write(selection)
    dfSelection = pd.DataFrame(selection, index=[0])
    dfSelection['Brand'] = uniques['Brand'].index(selection['Brand'])
    dfSelection['Model'] = uniques['Model'].index(selection['Model'])
    dfSelection['Region'] = uniques['Region'].index(selection['Region'])
    dfSelection['Engine'] = uniques['Engine'].index(selection['Engine'])
    dfSelection['Drive'] = uniques['Drive'].index(selection['Drive'])
    dfSelection['Transmission'] = uniques['Transmission'].index(selection['Transmission'])
    # st.write(dfSelection)

    # Предсказание модели на указанных данных
    model = joblib.load('../model/model_linearRegression.pkl');
    pred = model.predict(dfSelection)
    pred = pred.astype(int)

    price = pred[0]
    if price < 0:
        price = 0
    st.subheader('Предсказанная цена: ' + str(price) + ' рублей')


# streamlit run MainPage.py
# cd lab3 ||||||||| python -m streamlit run MainPage.py
if __name__ == "__main__":
    st.title("Предсказание цены на автомобиль")
    st.sidebar.markdown("Предсказание цены на автомобиль")

    st.subheader("Введите данные для предсказания: ")

    selection["Brand"] = st.selectbox(
        "Выберите марку автомобиля",
        Counter(params["Brand"].sort_values())
    )

    selection["Model"] = st.selectbox(
        "Выберите модель автомобиля",
        Counter(params.loc[params["Brand"] == selection["Brand"]]["Model"].sort_values())
    )

    selection["Region"] = st.selectbox(
        "Выберите местонахождение автомобиля",
        Counter(params["Region"][~pd.isnull(params["Region"])].sort_values())
    )

    selection["Year"] = st.slider(
        "Выберите год выпуска автомобиля",
        min_value=2000,max_value=2022,step=1
    )

    selection["Engine"] = st.radio(
        "Выберите тип двигателя",
        Counter(params["Engine"].sort_values())
    )

    selection["EngineVolume"] = st.selectbox(
        "Выберите объем двигателя",
        Counter(params["EngineVolume"][~pd.isnull(params["EngineVolume"])].sort_values())
    )

    selection["Power"] = st.number_input("Введите количество лошадиных сил", min_value=1, max_value=1000, step=10)

    selection["Drive"] = st.radio(
        "Выберите привод автомобиля",
        Counter(params["Drive"][~pd.isnull(params["Drive"])])
    )

    selection["Transmission"] = st.selectbox(
        "Выберите тип коробки передач",
        Counter(params["Transmission"][~pd.isnull(params["Transmission"])].sort_values())
    )

    selection["Mileage"] = st.number_input("Введите пробег автомобиля", min_value=0, max_value=1000000, step=1000)

    if st.button('Рассчитать'):
        buttonHandler()
