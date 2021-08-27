from data_processing import dict_frequencies
import streamlit as st

print(dict_frequencies["overall_frequency-lucky_number"])
# st.title('Combien des fois chaque numero est sorti ?')
# st.write("numero de chance:")
dict_frequencies["overall_frequency-lucky_number"]

def app():
    # st.markdown("## Combien des fois chaque numero est sorti ?")
    st.markdown("## Reussite de chaque numero")
    # st.markdown("### Tirage 5 boules:")
    # st.markdown("### Tirage Numero de chance")
    st.write("\n")
    st.write("Tirage numero de chance:")
    st.write(dict_frequencies["overall_frequency-lucky_number"])
    
     

    