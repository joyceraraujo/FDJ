from data_processing import dict_frequencies
import streamlit as st
import pandas



def app():
    
    st.markdown("## Reussite de chaque numero")

    col1, col2 = st.beta_columns(2)
    col1.write("Tirage 5 boules:")
    col2.write("Tirage numero de chance:")

    col1, col2 = st.beta_columns(2)

    col1.write(dict_frequencies["overall_frequency-balls"])
    col2.write(dict_frequencies["overall_frequency-lucky_number"])
