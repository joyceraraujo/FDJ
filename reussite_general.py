from data_processing import dict_frequencies
import streamlit as st
import pandas



def app():
    st.markdown("## Reussite de chaque numero")
    st.write("\n")
    st.write("Tirage 5 boules:")
    st.write(dict_frequencies["overall_frequency-balls"])
 

    

