from data_processing import df_after2008
import streamlit as st
import pandas as pd


def calculate_df(df):
        dict_timeslices = {
                               "year" : df['year'].unique(),
                               "month" : df['month'].unique(),
                               "day" : df['day'].unique(),
                               "day_name":  df['day_name'].unique()                              
                               
                               }
        name_timeslices = dict_timeslices.keys()
        
        dict_variables = { "balls" : ['boule_1', 'boule_2', 'boule_3', 'boule_4','boule_5'],
                            "lucky_number" : ['numero_chance']
            }
        name_variables = dict_variables.keys()


#from streamlit, get timeslice selected

# year_selected = 
# month_selected =
# day_selected =
# day_week_selected =

def options_menu (df,col):
    list = df_after2008[col].unique().tolist()
    list.insert(0,"")
    return list

def app():
    col1, col2, col3, col4 = st.beta_columns(4)


    year = col1.selectbox("Année", options = options_menu(df_after2008, "year") )
    month = col2.selectbox("Mois", options = options_menu(df_after2008, "month"))
    day = col3.selectbox("Jour", options = options_menu(df_after2008, "day"))
    day_name = col4.selectbox("Jour de la semaine", options = options_menu(df_after2008, "day_name"))

    timeslice = [year,month,day,day_name]
    name_timeslice = ["year","month","day","day_name"]
    timeslice_has_value = [timeslice != "" for timeslice in timeslice]
    valid_timeslice = timeslice_has_value.count(True)
    index_timeslice = [index for index, value in enumerate(timeslice) if value != ""]


    if st.button("Rechercher"): 

        st.markdown("### Résultats pour la date selectionée")
        
        dict_variables = { "balls" : ['boule_1', 'boule_2', 'boule_3', 'boule_4','boule_5'],
                            "lucky_number" : ['numero_chance']
            }
        name_variables = dict_variables.keys()
                
        dict_df_timeslice = dict()
        for name_variable in name_variables: # Loop through variables
            
            variable_to_count = dict_variables[name_variable]
            df_query = df_after2008.loc[df_after2008['variable'].isin(variable_to_count)]

   
            if valid_timeslice == 1 :
                
                name_timeslice1 = name_timeslice[index_timeslice[0]]
                t1 = timeslice[index_timeslice[0]]

                df_group = pd.DataFrame(df_query[(df_query[name_timeslice1]==t1) ].groupby("value").size()) 
            if valid_timeslice == 2 : 

                name_timeslice1 = name_timeslice[index_timeslice[0]]
                name_timeslice2 = name_timeslice[index_timeslice[1]]
                t1 = timeslice[index_timeslice[0]]
                t2 = timeslice[index_timeslice[1]]

                df_group = pd.DataFrame(df_query[(df_query[name_timeslice1]==t1) & (df_query[name_timeslice2]==t2) ].groupby("value").size()) 
            if valid_timeslice == 3 : 

                name_timeslice1 = name_timeslice[index_timeslice[0]]                
                name_timeslice2 = name_timeslice[index_timeslice[1]]                
                name_timeslice3 = name_timeslice[index_timeslice[2]]                
                t1 = timeslice[index_timeslice[0]]                
                t2 = timeslice[index_timeslice[1]]                
                t3 = timeslice[index_timeslice[2]]
                
                df_group = pd.DataFrame(df_query[(df_query[name_timeslice1]==t1) & (df_query[name_timeslice2]==t2) & (df_query[name_timeslice3]==t3) ].groupby("value").size()) 
                
            if valid_timeslice == 4 : 

                name_timeslice1 = name_timeslice[index_timeslice[0]]
                name_timeslice2 = name_timeslice[index_timeslice[1]]
                name_timeslice3 = name_timeslice[index_timeslice[2]]
                name_timeslice4 = name_timeslice[index_timeslice[3]]
                t1 = timeslice[index_timeslice[0]]
                t2 = timeslice[index_timeslice[1]]
                t3 = timeslice[index_timeslice[2]]
                t4 = timeslice[index_timeslice[3]]

                df_group = pd.DataFrame(df_query[(df_query[name_timeslice1]==t1) & (df_query[name_timeslice2]==t2) & (df_query[name_timeslice3]==t3) & (df_query[name_timeslice4]==t4) ].groupby("value").size()) 


            df_group.reset_index(inplace=True)
            dict_df_timeslice[name_variable] = df_group
        col1, col2 = st.beta_columns(2)
        col1.write("5 boules:")
        col2.write("numero de chance:")

        col1, col2 = st.beta_columns(2)

        col1.write(dict_df_timeslice["balls"])
        col2.write(dict_df_timeslice["lucky_number"])