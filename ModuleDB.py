#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 22:21:51 2021

@author: joyce
"""


from pymongo import MongoClient
#Funcoes para criaçao e atualizacao das informacoes do banco de dados NoSQL no MongoDB
    
def create_open_db(url_db,nomDB): #esta funçao cria ou carrega um db
       
    db = MongoClient(url_db)[nomDB] 
    

    return db



def insert_main_db(db,nomCollectionsDB,df):
    
    db[nomCollectionsDB].insert_many(df.to_dict('records'))

