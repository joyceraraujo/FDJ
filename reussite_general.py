from data_processing import dict_frequencies
import streamlit as st
import pandas
import plotly.express as px


def app():
    
    st.markdown("## Réussite de chaque numero")

    col1, col2 = st.columns(2)
    col1.write("Cinq boules:")
    col2.write("Numéro de chance:")

    col1, col2 = st.columns(2)

    col1.write(dict_frequencies["balls"])
    col2.write(dict_frequencies["lucky_number" ])
    

    st.markdown('## Vue graphique')
    col1, col2 = st.columns(2)
    fig = px.bar(dict_frequencies["balls" ], x="Numéro", y="Réussite", color='Réussite')
    st.write("Cinq boules:")
    st.write(fig)

    fig = px.bar(dict_frequencies["lucky_number"], x="Numéro", y="Réussite", color='Réussite')
    st.write("Numéro de chance:")
    st.write(fig)