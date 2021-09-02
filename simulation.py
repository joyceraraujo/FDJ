from data_processing import df_after2008
import streamlit as st
import pandas as pd


def count_win(df): 
    list_win_nb5 = [5,5,4,4,3,3,2,2,1,0]
    list_win_nbchance = [1,0,1,0,1,0,1,0,1,1]
    list_combine_win = [str(m)+ " " + "boule(s)" + " + " + str(n) + " numero de chance" for m,n in zip(list_win_nb5,list_win_nbchance)]

    list_count = []
    i = 0
    for nb5 in list_win_nb5:
        count =  df[(df["balls"] == nb5) & (df["lucky_number"] == list_win_nbchance[i])].shape[0]
        i=i+1
        list_count.append(count)

    return pd.DataFrame({'Combinaison': list_combine_win, 'Numero de tirages gagnantes': list_count}) 


def search_df(user_sequency):
    
    dict_variables = { "balls" : ['boule_1', 'boule_2', 'boule_3', 'boule_4','boule_5'],
                            "lucky_number" : ['numero_chance']
            }
    name_variables = dict_variables.keys()

    ids = df_after2008["annee_numero_de_tirage"].unique()
    
    dict_df = dict()
    dict_df["id_game"] =  list(ids)
    # print(len(list(ids)))
    for name_variable in name_variables:   
        variable_to_count =  dict_variables[name_variable]
        list_nb = []
        for id in ids: 
            
            
            result = list(df_after2008.loc[(df_after2008['variable'].isin(variable_to_count)) & (df_after2008['annee_numero_de_tirage']==id),"value"]) 
            
            
            match = list(set(result).intersection(user_sequency[name_variable]))
            
            size_match = len(match)
            list_nb.append(size_match)
        # print(name_variable,len(list_nb))
        dict_df[name_variable] = list_nb

    df_win = count_win(pd.DataFrame(dict_df))     
    return  df_win#pd.DataFrame(dict_df)#df_win

def app ():

    values = range(1,50,1)
    values_chance = range(1,11,1)

    bol1,bol2,bol3,bol4,bol5,bol6 = st.beta_columns(6)
    nb5 = list()
    bol1 = bol1.selectbox("boule 1",values)
    bol2 = bol2.selectbox("boule 2",values)
    bol3 = bol3.selectbox("boule 3",values)
    bol4 = bol4.selectbox("boule 4",values)
    bol5 = bol5.selectbox("boule 5",values)
    bol6 = bol6.selectbox("numero de chance",values_chance)
    nb5 = [bol1,bol2,bol3,bol4,bol5]
    #verifiy duplicated values before starting searching
    is_duplicated = len(nb5) != len(set(nb5)) 
    dict_user_sequency = { "balls" : nb5,
                            "lucky_number" : [bol6]
            }


    if st.button("Rechercher"): 
        if not is_duplicated:
            st.write(is_duplicated)     
            # st.write(df_after2008)

            st.write(search_df(dict_user_sequency))
            # st.write(search_df(dict_user_sequency))
        else : 
            st.write("Valeurs doublons, corriger svp =)") 