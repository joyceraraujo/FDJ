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


# #--------------------FUNCTIONS TO BE USED--------------------#  
# def download_files_six(url,path): #function to download the files by using the library six
    
#     r = requests.get(url, stream=True)  
#     z = zipfile.ZipFile(six.BytesIO(r.content)) #get the content of the url. In python 3, these informations are bytes not string as in Python2
#     z.extractall(path) #extract the files that are ziped

# def download_files_io(url,path):#function to download the files by using the library io
#     r = requests.get(url, stream=True)
#     z = zipfile.ZipFile(io.BytesIO(r.content))    
#     z.extractall(path)
def download_files_six(url,path): #function to download the files by using the library six
    
    r = requests.get(url, stream=True)  
    z = zipfile.ZipFile(six.BytesIO(r.content)) #get the content of the url. In python 3, these informations are bytes not string as in Python2
    z.extractall(path) #extract the files that are ziped

def download_files_io(url,path):#function to download the files by using the library io
    r = requests.get(url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))    
    z.extractall(path)
       
def try_open_url(url):
    try:
        page = requests.get(url) 
        flag = 1
        
    except:
        flag = 0
        page = []
    return page, flag   
    
# sub_urls_defaut = [#urls to download the files from FDJ website:
#        "https://media.fdj.fr/static/csv/loto/loto_197605.zip",
#        "https://media.fdj.fr/static/csv/loto/loto_200810.zip",
#        "https://media.fdj.fr/static/csv/loto/loto_201703.zip",
#        "https://media.fdj.fr/static/csv/loto/loto_201902.zip",
#        "https://media.fdj.fr/static/csv/loto/loto_201911.zip",
#        ]

# meu log precisa comparar essas urls defaut com as urls obtidas via scrap para  eu sempre saber se a fdj decidiu colocar um arquivo novo"
main_url = "https://www.fdj.fr/jeux-de-tirage/loto/resultats/" 

page, flag_main_url = try_open_url(main_url) # leitura da url principal
   
data = page.text
soup = BeautifulSoup(data, features="html.parser")   

dict_references = dict()
sub_urls_from_scrap= []

for link in soup.find_all('a',{"class":"history-result_item"}, href=True):
         sub_url = link['href']
         ref = link['data-tracking-click'].split("::")[-2::]
         
         # if "loto/loto_" in sub_url:
             
         sub_urls_from_scrap.append(sub_url)
         df = pd.read_csv(sub_url, compression="zip", sep=';')
         print(sub_url)
         dict_references[tuple(ref)] = df
         print(df.columns[0:11])
         


            

# t = time.time()
# data_path = "/home/joyce/DATA SCIENCE/JEUX LOTO FRANCE/INPUT/"
# for url in sub_urls_from_scrap:
    
#     download_files_io(url,data_path)

# elapsed = time.time() - t  #estimating time to execute      
# # print("BY USING io")
# print(elapsed) 



# list_name_game = [] #an empty list to keep the files names (extrated from the zip files that have been downloaded)
# for file in os.listdir(data_path):
#         list_name_game.append(file.split(".")[0]) #only the name, without extension