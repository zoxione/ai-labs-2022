import joblib
import streamlit as st
import pandas as pd
from collections import Counter


params = pd.read_csv("params.csv")
selection = dict()

chooseProperty = ['Year', 'EngineVolume', 'Power', 'Mileage']

def buttonHandler():
    model = joblib.load('../model/modelLinearRegression.pkl');
    pred = model.predict(selection)
    pred = pred.astype(int)
    st.write(pred)

# streamlit run MainPage.py
# cd lab3 ||||||||| python -m streamlit run MainPage.py
if __name__ == "__main__":
    st.title("Предсказание цены на автомобиль")
    st.sidebar.markdown("Предсказание цены на автомобиль")

    st.write("Введите данные для предсказания: ")

    selection["Brand"] = st.selectbox(
        "Выберите марку автомобиля",
        Counter(params["Brand"]))

    selection["Model"] = st.selectbox(
        "Выберите модель автомобиля",
        Counter(params.loc[params["Brand"] == selection["Brand"]]["Model"]))

    # selection["Region"] = st.selectbox(
    #     "Выберите местонахождение автомобиля",
    #     Counter(params["Region"][~pd.isnull(params["Region"])]))

    selection["Year"] = st.slider(
        "Выберите год выпуска автомобиля",
        Counter(params["Year"])[min(Counter(params["Year"]))])

    # selection["Engine"] = st.radio(
    #     "Выберите тип двигателя",
    #     Counter(params["Engine"]))

    selection["Engine_volume"] = st.slider(
        "Выберите объем двигателя",
        Counter(params["EngineVolume"])[min(Counter(params["EngineVolume"]))])

    selection["Power"] = st.number_input("Введите количество лошадиных сил")

    # selection["Transmission"] = st.selectbox(
    #     "Выберите тип коробки передач",
    #     Counter(params["Transmission"][~pd.isnull(params["Transmission"])]))
    #
    # selection["Drive_unit"] = st.radio(
    #     "Выберите привод автомобиля",
    #     Counter(params["Drive_unit"][~pd.isnull(params["Drive_unit"])]))
    #
    # selection["Color"] = st.selectbox(
    #     "Выберите цвет автомобиля",
    #     Counter(params["Color"][~pd.isnull(params["Color"])]))

    selection["Mileage"] = st.number_input("Введите пробег автомобиля")

    # selection["Rudder"] = st.radio(
    #     "Выберите расположение руля",
    #     Counter(params["Rudder"][~pd.isnull(params["Rudder"])]))
    #
    # selection["Body"] = st.radio(
    #     "Выберите тип кузова",
    #     Counter(params.loc[params["Model"] == selection["Model"]]["Body"][~pd.isnull(params["Body"])]))

    if st.button('Рассчитать'):
        buttonHandler()
