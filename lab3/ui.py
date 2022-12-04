import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

# streamlit run ui.py
if __name__ == '__main__':
    st.title("Предсказание цены на недвижимость")
    st.write("Введите данные для предсказания: ")

    st.markdown("# Main pages 🎈")
    st.sidebar.markdown("# Main pages 🎈")

    x = st.slider('x')  # 👈 this is a widget
    st.write(x, 'squared is', x * x)

    st.text_input("Your name", key="name")

    option = st.selectbox(
        'Which number do you like best?',
            df['first column'])

    'You selected: ', option

    if st.button('Say hello'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')
