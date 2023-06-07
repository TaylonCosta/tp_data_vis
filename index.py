import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def populacao(dataset):

    fig = go.Figure()
    for entry in countries:
        df = dataset[(dataset['Location'] == entry) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
        fig.add_trace(
            go.Scatter(x=df['Time'], y=df['TPopulation1July'], mode='lines+markers', name=entry)
        )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish,
                    annotation_text='Projeção', annotation_position="top left",
                    fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Densidade populacional versus população ao longo do tempo',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        width = 1400,
        height=700,
    )

    return fig

def mortalidade(dataset):
    fig = go.Figure()
    for entry in countries:
        if finish > 2023:
            f = 2023
        else:
            f = finish
        df = dataset[(dataset['Location'] == entry) & (dataset['Time'] >= start) & (dataset['Time'] <= f)]
        fig.add_trace(go.Scatter(x=df['Time'], y=df['CDR'], mode='lines+markers', name=entry))

    fig.add_vrect(x0=2019.5, x1=2022.5, fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Taxa de Mortalidade (mortes por mil habitantes)',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=2023, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s')
    )

    return fig

def expectativa(dataset):

    fig = go.Figure()
    for entry in countries:
        df = dataset[(dataset['Location'] == entry) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
        fig.add_trace(
            go.Scatter(x=df['Time'], y=df['LEx'], mode='lines+markers', name=entry)
        )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish,
              annotation_text='Projeção', annotation_position="top left",
              fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Expectativa de vida ao nascer',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s')
    )

    return fig

def dispersao(dataset):
    df = px.data.gapminder()
    fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
               size="pop", color="continent", hover_name="country",
               log_x=True, size_max=55, range_x=[100, 100000], range_y=[25, 90])

    fig.update_layout(title='Expectativa de vida ao nascer',
        plot_bgcolor='white', width = 1450, height=700)

    return fig

if __name__ == '__main__':
    st.set_page_config(layout="wide")

    df = pd.read_csv('WPP2022_Demographic_Indicators_Medium.csv', low_memory=False)

    tab1, tab2 = st.tabs(['Comparação entre países', 'Análise de país'])

    with tab1:
        st.header('Comparação entre países')
        countries = st.sidebar.multiselect('choose the countries', ['Brazil', 'Argentina', 'Uruguay', 'Paraguay', 'Peru', 'Colombia', 'Bolivia'])
        start = st.sidebar.number_input('Pick the start year', 1950, 2050)
        finish = st.sidebar.number_input('Pick the finish year', 1951, 2050, value=2050)

        if not countries:
            countries = ['Brazil', 'Argentina', 'Uruguay', 'Paraguay', 'Peru', 'Colombia', 'Bolivia']

        with st.container():
            st.plotly_chart(populacao(df))

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(expectativa(df))
        with col2:
            st.plotly_chart(mortalidade(df))

        with st.container():
            st.plotly_chart(dispersao(df))

    with tab2:
        st.header('Análise de país')
        country = st.sidebar.selectbox('choose the countries', ['Brazil', 'Argentina', 'Uruguay', 'Paraguay', 'Peru', 'Colombia', 'Bolivia'])
        


