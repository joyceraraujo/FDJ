from data_processing import dict_frequencies
import streamlit as st
import pandas



def app():
    
    st.markdown("## Réussite de chaque numero")

    col1, col2 = st.beta_columns(2)
    col1.write("Cinq boules:")
    col2.write("Numéro de chance:")

    col1, col2 = st.beta_columns(2)

    col1.write(dict_frequencies["balls"])
    col2.write(dict_frequencies["lucky_number" ])
