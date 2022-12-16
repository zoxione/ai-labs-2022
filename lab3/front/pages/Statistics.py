import json
import streamlit as st
import pandas as pd


def getDataMetrics():
    # Получение данных из файла
    with open('../model/result_metrics.json') as json_file:
        data = json.load(json_file)
    return data

def getDataCorr():
    # Получение данных из файла
    with open('../parser/corr_values.json') as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    st.title("Статистика")
    st.sidebar.markdown("Статистика")

    st.write("Таблица: ")
    dfParams = pd.read_csv(".\params.csv")
    st.dataframe(dfParams)
    st.caption("Количество записей: " + str(dfParams.shape[0]))

    dataMetrics = getDataMetrics();
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Mean Absolute Error", value=f'{dataMetrics["MAE"]:.{2}f}')
    with col2:
        st.metric(label="Accuracy", value=f'{dataMetrics["Accuracy"]:.{2}f}')
    with col3:
        st.metric(label="Confusion Matrix", value=0)

    dataCorr = getDataCorr();
    st.write("Корреляция: ")
    s = pd.DataFrame.from_dict(dataCorr, orient='index', columns=['Коэффициент корреляции'])
    st.bar_chart(s)

    # st.write("Соотношение марки и цены: ")
    # st.bar_chart(data=dfParams, x="Brand", y="Price")
    #

    if 'Year' in dfParams.columns:
        st.write("Соотношение года и цены: ")
        st.bar_chart(data=dfParams, x="Year", y="Price")

    if 'Power' in dfParams.columns:
        st.write("Соотношение мощности и цены: ")
        st.area_chart(data=dfParams, x="Power", y="Price")

    if 'Mileage' in dfParams.columns:
        st.write("Соотношение пробега и цены: ")
        st.area_chart(data=dfParams, x="Mileage", y="Price")
