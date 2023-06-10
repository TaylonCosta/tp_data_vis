import streamlit as st

st.set_page_config(
    page_title="Hello"
)

st.write("# Demographic Indicators")

st.sidebar.success("Select a page above.")

st.markdown("""
This dashboard presents data from demographic indicators for countries and regions around the world.
""")

st.markdown("""
## Data

The 2022 Revision of World Population Prospects is the twenty-seventh edition of official United Nations population estimates and projections that have been prepared by the Population Division of the Department of Economic and Social Affairs of the United Nations Secretariat.
It presents population estimates from 1950 to the present for 237 countries or areas, underpinned by analyses of historical demographic trends.

Source: [World Population Prospects 2022](https://population.un.org/wpp/)
""")