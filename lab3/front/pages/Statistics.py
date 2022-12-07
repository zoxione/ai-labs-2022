import json
import streamlit as st
import pandas as pd


def getDataMetrics():
    # Получение данных из файла
    with open('../model/result_metrics.json') as json_file:
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

    st.write("Соотношение марки и цены: ")
    st.bar_chart(data=dfParams, x="Brand", y="Price")

    st.write("Соотношение года и цены: ")
    st.bar_chart(data=dfParams, x="Year", y="Price")

    st.write("Соотношение мощности и цены: ")
    st.area_chart(data=dfParams, x="Power", y="Price")
