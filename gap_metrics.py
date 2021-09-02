from data_processing import dict_gap_numbers
import streamlit as st
  


def app():
    st.markdown("## Metriques sur les écarts")

    col1, col2 = st.beta_columns(2)
    col1.write("5 boules:")
    col2.write("numero de chance:")

    col1, col2 = st.beta_columns(2)

    col1.write(dict_gap_numbers["balls"])
    col2.write(dict_gap_numbers["lucky_number"])