import streamlit as st
import pandas as pd

st.title("Статистика")
st.sidebar.markdown("Статистика")

params = pd.read_csv("params.csv")

accurency = 0
confusionMatrix = 0

st.write("Таблица: ")
st.dataframe(params)

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Accurency", value=accurency)
with col2:
    st.metric(label="Confusion Matrix", value=confusionMatrix)

st.write("Соотношение марки и цены: ")
st.bar_chart(data=params, x="Brand", y="Price")

st.write("Соотношение модели и цены: ")
st.bar_chart(data=params, x="Model", y="Price")

st.write("Соотношение местонахожения автомобиля и цены: ")
st.bar_chart(data=params[~pd.isnull(params["Region"])], x="Region", y="Price")
