from data_processing import df_after2008
import streamlit as st
import pandas as pd

def calculate_frequency(dfObj,list_cols): #calculate the frequency of occurences over the whole dataset
        
        df_frequency = pd.DataFrame(dfObj.groupby(list_cols[0]).size())#Count the frequency a value occurs  
        df_frequency.reset_index(inplace=True)
        df_frequency.columns = list_cols  
           
        df_frequency  = df_frequency.astype({"value": int})  
        df_frequency.sort_values(by=list_cols[1],ascending=False,inplace=True) #order the number that occurs most of time
        
        return df_frequency
    

def calculate_df(nb, variable_to_count): 

    max_index = df_after2008['new_date'].idxmax() 
    id_last_draw = df_after2008.loc[max_index,"annee_numero_de_tirage"]    
    range_last_draw = list(range(id_last_draw,id_last_draw+nb))    
    df_query = df_after2008.loc[(df_after2008['variable'].isin(variable_to_count)) & (df_after2008['annee_numero_de_tirage'].isin(range_last_draw))] 
          
    list_cols = ["value","frequency"]

    return calculate_frequency(df_query,list_cols)

def app():

    nb = st.slider('Sélectionnez le nombre de tirages ', min_value=1, value=50 ,max_value=50)

    

    st.markdown("## Résultats pour le nombre des tirages selectioné")
        
    dict_variables = { "balls" : ['boule_1', 'boule_2', 'boule_3', 'boule_4','boule_5'],
                            "lucky_number" : ['numero_chance']
            }
    name_variables = dict_variables.keys()
                
    dict_df = dict()
    for name_variable in name_variables: # Loop through variables
            
            variable_to_count = dict_variables[name_variable]         
            
            dict_df[name_variable] = calculate_df(nb, variable_to_count).rename(columns={"value": "Numéro", "frequency": "Réussite"})


    col1, col2 = st.columns(2)
    col1.write("Cinq boules:")
    col2.write("Numéro de chance:")

    col1, col2 = st.columns(2)

    col1.write(dict_df["balls"])
    col2.write(dict_df["lucky_number"])