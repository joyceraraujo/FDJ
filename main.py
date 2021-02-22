#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Feb 19 18:30:36 2021

@author: root
"""

import requests, zipfile,re
import io,os
import six #to read the content of the files htm
import time #to estimate the time of execution
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'

       
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
        
        print("#2: urls extracted successfully from web scrap")
        main_cols = ['annee_numero_de_tirage', 'jour_de_tirage', 'date_de_tirage','boule_1', 'boule_2', 'boule_3', 'boule_4',
                 'boule_5', 'numero_chance','boule_6', 'boule_complementaire','1er_ou_2eme_tirage',"name_lottery_game","ref_date"] # for a while...
    
        
        cols_before_2008 = ['boule_6', 'boule_complementaire','1er_ou_2eme_tirage']
        sub_cols_before_2008 = cols_before_2008[0:2] #special lottery games, like GrandLoto/SuperLoto, don't have the column '1er_ou_2eme_tirage'   
    
        df_concatenated_complet = pd.concat(list_df)
        df_concatenated_extracted = df_concatenated_complet[main_cols] 
    
    
        #Column Date processing.
        df_concatenated_extracted['format'] = "new format"
        df_concatenated_extracted.loc[df_concatenated_extracted['ref_date'] == 'Avant octobre 2008', 'format'] = "old format" # that means the game is in old format.        
        df_concatenated_extracted['date_de_tirage'] = df_concatenated_extracted['date_de_tirage'].astype(str) # Convert the whole column to string is important because the data are in different format (str and int)
        df_concatenated_extracted['new_date'] = pd.to_datetime(df_concatenated_extracted['date_de_tirage'], errors='coerce') 
        df_concatenated_extracted.loc[df_concatenated_extracted['format'] == 'new format', 'new_date'] =  pd.to_datetime(df_concatenated_extracted.loc[df_concatenated_extracted['format'] == 'new format', 'date_de_tirage'], format = '%d/%m/%Y')
        
        df_concatenated_extracted["day"] = df_concatenated_extracted['new_date'].map(lambda x: x.day)
        df_concatenated_extracted["month"] = df_concatenated_extracted['new_date'].map(lambda x: x.month)
        df_concatenated_extracted["year"] = df_concatenated_extracted['new_date'].map(lambda x: x.year)
        df_concatenated_extracted["day_name"] = df_concatenated_extracted['new_date'].map(lambda x: x.day_name())
        df_concatenated_extracted.drop(axis=1, columns =['date_de_tirage','jour_de_tirage'], inplace=True)
    else:
        print("#2: difference between web scrap and url defaut")
    


else:
    print("#1:A error to read main url was issued")
    

