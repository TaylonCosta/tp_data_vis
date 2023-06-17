import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def population_by_sex(dataset):

    fig = go.Figure()
    df = dataset[(dataset['Location'] == country) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
    fig.add_trace(
        go.Bar(x=df['Time'], y=df['TPopulationMale1July'], name='Male', marker_color='blue')
    )
    fig.add_trace(
        go.Bar(x=df['Time'], y=df['TPopulationFemale1July'], name='Female', marker_color='red')
    )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish+0.5,
                    annotation_text='Projection', annotation_position="top left",
                    fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Total Population by Sex',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        width = 1400,
        height=700,
        barmode='stack',
        hovermode="x unified"
    )

    return fig

def births_and_deaths(dataset):

    fig = go.Figure()
    df = dataset[(dataset['Location'] == country) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
    fig.add_trace(
        go.Bar(x=df['Time'], y=df['Births'], name='Births', marker_color='blue')
    )
    fig.add_trace(
        go.Bar(x=df['Time'], y=-df['Deaths'], name='Deaths', marker_color='red')
    )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish+0.5,
                    annotation_text='Projection', annotation_position="top left",
                    fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Total Births and Deaths',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        width = 1400,
        height=700,
        barmode='relative',
        hovermode="x unified"
    )

    return fig

def life_expectancy_sex(dataset):

    fig = go.Figure()
    df = dataset[(dataset['Location'] == country) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
    fig.add_trace(
        go.Scatter(x=df['Time'], y=df['LEx'], mode='lines+markers', name='Total')
    )
    fig.add_trace(
        go.Scatter(x=df['Time'], y=df['LExMale'], mode='lines+markers', name='Male')
    )
    fig.add_trace(
        go.Scatter(x=df['Time'], y=df['LExFemale'], mode='lines+markers', name='Female')
    )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish+0.5,
                    annotation_text='Projection', annotation_position="top left",
                    fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Life Expectancy by Sex',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        width = 1400,
        height=700,
        hovermode="x unified"
    )

    return fig

if __name__ == '__main__':
    st.set_page_config(layout="wide",
                       page_title="Explore a region")

    df = pd.read_csv('WPP2022_Demographic_Indicators_Medium.csv', low_memory=False)
    # adjust values in thousands
    df['TPopulation1July'] = df['TPopulationMale1July']*1000
    df['TPopulation1July'] = df['TPopulationFemale1July']*1000
    df['Births'] = df['Births']*1000 
    df['Deaths'] = df['Deaths']*1000 

    st.header('Explore a region')
    region_type = st.sidebar.selectbox('Choose the type of region', options = df['LocTypeName'].unique())
    # filter countries depending on region type
    country = st.sidebar.selectbox('Choose the region', options = np.sort(df.loc[df['LocTypeName']==region_type,'Location'].unique()))
    start = st.sidebar.number_input('Pick the start year', 1950, 2050)
    finish = st.sidebar.number_input('Pick the finish year', 1951, 2050, value=2050)
    st.subheader(country)

    with st.container():
        st.plotly_chart(population_by_sex(df))
        st.plotly_chart(life_expectancy_sex(df))
        st.plotly_chart(births_and_deaths(df))