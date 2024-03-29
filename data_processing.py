#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Feb 19 18:30:36 2021

@author: root
"""

import requests
import time #to estimate the time of execution
import pandas as pd
from bs4 import BeautifulSoup
import calendar
from itertools import permutations
pd.options.mode.chained_assignment = None  # default='warn'
import statistics   
import streamlit as st   
import plotly.express as px
# from multipage import MultiPage


def try_open_url(url):
    try:
        page = requests.get(url) 
        flag = 1
        if page.status_code == 404:
            flag = 0
    except:
        flag = 0
        page = []
    return page, flag

def df_melt(dfObj): #function to transform the columns of the results in rows. in this way, we will have a only column with results by id
         
        nb_start = 9 # skiping two first columns because they represent the index of games. 
        
        list_col = list(dfObj.columns[nb_start::])
        
        dfObj = pd.melt(dfObj, id_vars=['annee_numero_de_tirage','name_lottery_game',"ref_date",'format','new_date', 'day', 'month', 'year', 'day_name'], value_vars=list_col)
        
        
        return dfObj

def calculate_frequency(dfObj,list_cols): #calculate the frequency of occurences over the whole dataset
        
        df_frequency = pd.DataFrame(dfObj.groupby(list_cols[0]).size())#Count the frequency a value occurs  
        df_frequency.reset_index(inplace=True)
        df_frequency.columns = list_cols  
           

        df_frequency.sort_values(by=list_cols[1],ascending=False,inplace=True) #order the number that occurs most of time
        
        return df_frequency
    
def calculate_df_gap(df):
    
        dict_variables = { "balls" : ['boule_1', 'boule_2', 'boule_3', 'boule_4','boule_5'],
                            "lucky_number" : ['numero_chance']
            }
        name_variables = dict_variables.keys()

        dict_digits = { "balls"  : list(range(1,50)),
                           "lucky_number" : list(range(1,11)) 
            }
        
        dict_key_variable = { "balls" : "GapNumber" ,
                            "lucky_number" : "GapLuckyNumber"
                            }
       
        dict_gap_numbers = dict()
        
        gap_numbers_list = [] # list of dictionaries in which each dictionary corresponds to an input data row
        list_flags = []
        iflag = 0 
        for variable in name_variables:
            gap_numbers_list = [] # list of dictionaries in which each dictionary corresponds to an input data row
            for d in dict_digits[variable]:
                
                variable_to_count = dict_variables[variable] 
                list_id = df_after2008.loc[(df_after2008['variable'].isin(variable_to_count) & (df_after2008['value']==d)),"annee_numero_de_tirage"].tolist()
                list_id.sort()
                gap =  [y - x -1 for x,y in zip(list_id,list_id[1:])]
                gap.insert(0, list_id[0]-1)
                max_gap = max(gap)
                moy_gap = statistics.mean(gap)
                last_gap = gap[0]
                gap_numbers_list.append([d, last_gap, max_gap, moy_gap])
                
                gap = []
            df_gap = pd.DataFrame(gap_numbers_list) 
            df_gap.columns = ["Numéro", "Écart Actuel", "Écart Max", "Écart Moyen"]
            dict_gap_numbers[variable] = df_gap
        return dict_gap_numbers
         
start = time.time()    
#sub_url_defaut helps to validate the result of data scrapping.     
sub_urls_defaut = [#urls to download the files from FDJ website:

    "https://media.fdj.fr/static/csv/loto/loto_201911.zip",
    "https://media.fdj.fr/static/csv/loto/loto_201902.zip",
    "https://media.fdj.fr/static/csv/loto/loto_201703.zip",
    "https://media.fdj.fr/static/csv/loto/loto_200810.zip",
    "https://media.fdj.fr/static/csv/loto/loto_197605.zip",
    "https://media.fdj.fr/static/csv/loto/superloto_201907.zip",
    "https://media.fdj.fr/static/csv/loto/superloto_201703.zip",
    "https://media.fdj.fr/static/csv/loto/superloto_200810.zip",
    "https://media.fdj.fr/static/csv/loto/superloto_199605.zip",
    "https://media.fdj.fr/static/csv/loto/lotonoel_201703.zip",
    "https://media.fdj.fr/static/csv/loto/grandloto_201912.zip",
        ]


main_url = "https://www.fdj.fr/jeux-de-tirage/loto/resultats/" 
#Opening main url to data scrapping.
page, flag_main_url = try_open_url(main_url)
if flag_main_url:  
    print("#1: main url read successfully")
    data = page.text
    soup = BeautifulSoup(data, features="html.parser")   
    
    dict_references = dict()
    sub_urls_from_scrap= []
    list_df =[]
    for link in soup.find_all('a',{"class":"history-result_item"}, href=True):
             sub_url = link['href']
             ref = link['data-tracking-click'].split("::")[-2::]
             
                              
             sub_urls_from_scrap.append(sub_url)
            
             df = pd.read_csv(sub_url, compression="zip", sep=';')
             
             df["name_lottery_game"] = ref[0]
             df["ref_date"] = ref[1] 
           
             list_df.append(df)
             
             dict_references[tuple(ref)] = df
             
    if sub_urls_from_scrap == sub_urls_defaut:
        dict_df_toMongoDB = dict()
        
        print("#2: urls extracted successfully from web scrap")
        
        main_cols = ['annee_numero_de_tirage',"name_lottery_game", 'jour_de_tirage', 'date_de_tirage','boule_1', 'boule_2', 'boule_3', 'boule_4',
                 'boule_5', 'numero_chance','boule_6', 'boule_complementaire','1er_ou_2eme_tirage',"ref_date"] # for a while...
        
        
        
        cols_before_2008 = ['boule_6', 'boule_complementaire','1er_ou_2eme_tirage']
        sub_cols_before_2008 = cols_before_2008[0:2] #special lottery games, like GrandLoto/SuperLoto, don't have the column '1er_ou_2eme_tirage'   
    
        df_concat_complet = pd.concat(list_df)
        df_concat_extrait = df_concat_complet[main_cols] 

    
        #Column Date processing.
        df_concat_extrait['format'] = "new format"
        df_concat_extrait.loc[df_concat_extrait['ref_date'] == 'Avant octobre 2008', 'format'] = "old format" # that means the game is in old format.        
        df_concat_extrait['date_de_tirage'] = df_concat_extrait['date_de_tirage'].astype(str) # Convert the whole column to string is important because the data are in different format (str and int)
        df_concat_extrait['new_date'] = pd.to_datetime(df_concat_extrait['date_de_tirage'], errors='coerce') 
        df_concat_extrait.loc[df_concat_extrait['format'] == 'new format', 'new_date'] =  pd.to_datetime(df_concat_extrait.loc[df_concat_extrait['format'] == 'new format', 'date_de_tirage'], format = '%d/%m/%Y')
        
        df_concat_extrait["day"] = df_concat_extrait['new_date'].map(lambda x: x.day)
        df_concat_extrait["month"] = df_concat_extrait['new_date'].map(lambda x: x.month)
        df_concat_extrait["year"] = df_concat_extrait['new_date'].map(lambda x: x.year)
        df_concat_extrait["day_name"] = df_concat_extrait['new_date'].map(lambda x: x.day_name())
        df_concat_extrait.drop(axis=1, columns =['date_de_tirage','jour_de_tirage'], inplace=True)
        main_cols = ['annee_numero_de_tirage','name_lottery_game',"ref_date",'format','new_date', 'day', 'month', 'year', 'day_name','boule_1', 'boule_2', 'boule_3', 'boule_4',
                 'boule_5', 'numero_chance','boule_6', 'boule_complementaire','1er_ou_2eme_tirage'] # for a while...
        
        
        df_concat_extrait = df_concat_extrait.sort_values(by=['new_date'], ascending=False)
        id_game = list(range(1,len(df_concat_complet)+1))
        df_concat_extrait['annee_numero_de_tirage'] = id_game
        
        
        #Melting dataframe
        df_concat_extrait = df_concat_extrait[main_cols]
        df_concat_extrait = df_melt(df_concat_extrait)
        
        # In order to respect a standard, it will be more coerent to treat only results concerned after 2008 (before rules changing).
        # So, query is necessary to keep only these data. 
        df_after2008 =  df_concat_extrait.loc[df_concat_extrait["format"] == 'new format']
        
        d = dict(enumerate(calendar.month_abbr))
        df_after2008['month'] = df_after2008['month'].map(d)
        dict_df_toMongoDB["GeneralDF"] = df_after2008

        #Calculating frequencies of numbers

        dict_variables = { "balls" : ['boule_1', 'boule_2', 'boule_3', 'boule_4','boule_5'],
                                "lucky_number" : ['numero_chance']
                }
        name_variables = dict_variables.keys()
        list_cols = ["value","frequency"]            
        dict_frequencies = dict()
        for name_variable in name_variables: # Loop through variables
                
                variable_to_count = dict_variables[name_variable]         
                df_query = df_after2008.loc[df_after2008['variable'].isin(variable_to_count)]   
                df_query  = df_query.astype({"value": int})             
                dict_frequencies[name_variable] = calculate_frequency(df_query,list_cols).rename(columns={"value": "Numéro", "frequency": "Réussite"})




    
       #Calculate number gap : 
        dict_gap_numbers  = calculate_df_gap(df_after2008)

    
    else:
        print("#2: difference between web scrap and url defaut")
     
        

else:
    print("#1:A error to read main url was issued")
    

elapsed = time.time() - start
print(elapsed)