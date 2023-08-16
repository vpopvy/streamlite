import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import streamlit as st
import pandas as pd
import seaborn as sns
from scipy import stats

# Загрузка данных
st.title("Анализ данных с использованием Streamlit")

uploaded_file = st.file_uploader("Загрузите CSV файл", type=["csv"])

if uploaded_file is not None:
    if uploaded_file.name.split('.')[-1] != 'csv':
        st.write('Файл не csv, загрузите другой файл')
    else:
        df = pd.read_csv(uploaded_file)

        # Краткая информация о файле
        st.sidebar.subheader("Информация о файле")
        st.sidebar.write("Количество строк:", df.shape[0])
        st.sidebar.write("Количество столбцов:", df.shape[1])
        st.sidebar.write("Размер файла:", f"{round(uploaded_file.size / 1024, 2)} KB")

        # Выбор колонок для исследования
        st.sidebar.header("Выберите переменные для исследования")
        col1 = st.sidebar.selectbox("Переменная 1", df.columns)
        is_categorical_col1 = df[col1].dtype == "object"
        if is_categorical_col1: st.sidebar.info("Категорильные")
        col2 = st.sidebar.selectbox("Переменная 2", df.columns)
        is_categorical_col2 = df[col2].dtype == "object"
        if is_categorical_col2: st.sidebar.info("Категорильные")

        # Выбор алгоритма теста гипотез
        st.sidebar.header("Выберите алгоритм теста гипотез")



        st.dataframe(df.head())

        test_algorithm = st.sidebar.selectbox("Алгоритм", ["t-test", "Chi-squared test"])

        # Визуализация распределения переменных
        st.subheader("Визуализация распределения переменных")
        if col1 != col2:
            if (is_categorical_col1 and is_categorical_col2):
                fig1 = px.pie(df[col1].value_counts()[:30], names=df[col1].value_counts()[:30].index,
                              title=f"Распределение {col1}")
                st.plotly_chart(fig1)

                fig2 = px.pie(df[col2].value_counts()[:30], names=df[col2].value_counts()[:30].index,
                              title=f"Распределение {col2}")
                st.plotly_chart(fig2)

                st.text("Выбраны первые 30 значений для корректного отображения графиков")
            elif (is_categorical_col1 == True and is_categorical_col2 == False):
                fig1 = px.pie(df[col1].value_counts()[:30], names=df[col1].value_counts()[:30].index,
                              title=f"Распределение {col1}")
                st.plotly_chart(fig1)

                fig2 = px.histogram(df[:30], x=col2, nbins=10, title=f"Распределение {col2}")
                st.plotly_chart(fig2)

                st.text("Выбраны первые 30 значений для корректного отображения графиков")
            elif (is_categorical_col2 == True and is_categorical_col1 == False):
                fig1 = px.histogram(df[:30], x=col1, nbins=10, title=f"Распределение {col1}")
                st.plotly_chart(fig1)

                fig2 = px.pie(df[col2].value_counts()[:30], names=df[col2].value_counts()[:30].index,
                              title=f"Распределение {col2}")
                st.plotly_chart(fig2)

                st.text("Выбраны первые 30 значений для корректного отображения графиков")
            elif (is_categorical_col1 == is_categorical_col2 == False):
                fig1 = px.histogram(df[:30], x=col1, nbins=10, title=f"Распределение {col1}")
                fig2 = px.histogram(df[:30], x=col2, nbins=10, title=f"Распределение {col2}")

                st.plotly_chart(fig1)
                st.plotly_chart(fig2)

                st.text("Выбраны первые 30 значений для корректного отображения графиков")
        else:
            st.warning("Выберите разные переменные для сравнения")

        # Результаты теста гипотез
        if test_algorithm == "Chi-squared test" and (is_categorical_col1 == is_categorical_col2 == True):
            st.subheader("Результаты теста гипотез для категориальных данных")
            contingency_table = pd.crosstab(df[col1], df[col2])
            result = stats.chi2_contingency(contingency_table)
            st.write("Статистика хи-квадрат:", result[0])
            st.write("p-значение:", result[1])
            st.write("Степени свободы:", result[2])
            alpha = 0.05
            if result[1] < alpha:
                st.write("Гипотеза отвергается: между переменными есть значимая связь.")
            else:
                st.write("Гипотеза не отвергается: между переменными нет значимой связи.")
        elif test_algorithm == "t-test" and (not is_categorical_col1 and not is_categorical_col2):
            st.subheader("Результаты теста гипотез для числовых данных (t-test)")
            result = stats.ttest_ind(df[col1], df[col2])
            st.write("t-статистика:", result.statistic)
            st.write("p-значение:", result.pvalue)
            alpha = 0.05
            if result.pvalue < alpha:
                st.write("Гипотеза отвергается: средние значения различаются значимо.")
            else:
                st.write("Гипотеза не отвергается: нет значимого различия между средними значениями.")
        else:
            st.warning("Для категориальных данных - Chi-squared test. Для других данных t-test.")
