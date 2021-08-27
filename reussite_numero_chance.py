from data_processing import dict_frequencies
import streamlit as st


def app():

    st.markdown("## Reussite de chaque numero")
    st.write("\n")
    st.write("Tirage numero de chance:")
    st.write(dict_frequencies["overall_frequency-lucky_number"])
    
     

    