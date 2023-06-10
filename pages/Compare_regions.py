import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def population(dataset):

    fig = go.Figure()
    for entry in countries:
        df = dataset[(dataset['Location'] == entry) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
        fig.add_trace(
            go.Scatter(x=df['Time'], y=df['TPopulation1July'], mode='lines+markers', name=entry)
        )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish+0.5,
                    annotation_text='Projection', annotation_position="top left",
                    fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Total Population',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        width = 1400,
        height=700,
        hovermode="x unified"
    )

    return fig

def mortality(dataset):
    fig = go.Figure()
    for entry in countries:
        df = dataset[(dataset['Location'] == entry) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
        fig.add_trace(go.Scatter(x=df['Time'], y=df['CDR'], mode='lines+markers', name=entry))

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish+0.5,
              annotation_text='Projection', annotation_position="top left",
              fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Crude Death Rate',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=2023, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        hovermode="x unified"
    )

    return fig

def life_expectancy(dataset):

    fig = go.Figure()
    for entry in countries:
        df = dataset[(dataset['Location'] == entry) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]
        fig.add_trace(
            go.Scatter(x=df['Time'], y=df['LEx'], mode='lines+markers', name=entry)
        )

    if finish > 2022.5:
        fig.add_vrect(x0=2022.5, x1=finish+0.5,
              annotation_text='Projection', annotation_position="top left",
              fillcolor="gray", opacity=0.25, line_width=0)

    fig.update_layout(
        title='Life Expectancy at Birth',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, tickmode='linear', tick0=start, dtick=10, gridcolor='rgb(230, 230, 230)'),
        yaxis=dict(showgrid=True, gridcolor='rgb(230, 230, 230)', tickformat='.3s'),
        hovermode="x unified"
    )

    return fig

def scatter(dataset):
    df = dataset[(dataset['Location'].isin(countries)) & (dataset['Time'] >= start) & (dataset['Time'] <= finish)]

    fig = px.scatter(df, x="TPopulation1July", y="PopDensity", animation_frame="Time",
                     color="Location", animation_group='Location', log_x=True,
                     hover_name='Location',
                     hover_data={
                         'Location': False,
                         'Time': True,
                         'TPopulation1July': ':.3s',
                         'PopDensity': ':.2f'
                     },
                     labels = {
                         'TPopulation1July': 'Population',
                         'PopDensity': 'Pop. Density',
                         'Location': '',
                         'Time': 'Year'
                         })

    fig.update_layout(title='Population vs Population Density',
        plot_bgcolor='white', width = 1450, height=700)
    
    fig.update_traces(marker={'size': 15})

    return fig

if __name__ == '__main__':
    st.set_page_config(layout="wide")

    df = pd.read_csv('WPP2022_Demographic_Indicators_Medium.csv', low_memory=False)
    # adjust values in thousands
    df['TPopulation1July'] = df['TPopulation1July']*1000

    st.header('Compare regions')
    region_type = st.sidebar.multiselect('Choose the type of region', options = df['LocTypeName'].unique())
    # filter countries depending on region type
    countries = st.sidebar.multiselect('Choose the region', options = np.sort(df.loc[df['LocTypeName'].isin(region_type),'Location'].unique()))
    start = st.sidebar.number_input('Pick the start year', 1950, 2050)
    finish = st.sidebar.number_input('Pick the finish year', 1951, 2050, value=2050)

    # default: world regions
    if not region_type:
        region_type = ['Geographic region']

    # default: list all options within the region type
    if not countries:
        opt = df.loc[df['LocTypeName'].isin(region_type),'Location'].unique()
        opt.sort()
        # if list of options too large, limit (too slow if too many options)
        if len(opt) > 20:
            countries = opt[:20]
        else:
            countries = opt

    with st.container():
        st.plotly_chart(population(df))

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(life_expectancy(df))
    with col2:
        st.plotly_chart(mortality(df))

    with st.container():
        st.plotly_chart(scatter(df))