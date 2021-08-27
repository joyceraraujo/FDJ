from data_processing import dict_frequencies
import streamlit as st



print(dict_frequencies["overall_frequency-balls"])

def app():
    st.markdown("## Data Upload")

    # Upload the dataset and save as csv
    st.markdown("### Upload a csv file for analysis.") 
    st.write("\n")

    st.title('Combien des fois chaque numero est sorti ?')
    st.write("5 numeros:")
    dict_frequencies["overall_frequency-balls"]

