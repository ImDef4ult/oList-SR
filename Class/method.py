import pandas as pd
import pickle
from surprise import SVD
import numpy as np
import random
import streamlit as st
from statistics import mode


import warnings
warnings.filterwarnings("ignore")

def LogIn(userName, passUser):
    query = Users.loc[Users['customer_id'] == userName]
    if query is not None:
        if query['password'].to_string(index=False).strip() == passUser:
            return True
        else:
            return False
    else:
        return False

def get_UserRev(username):
    Tmp = Rev[Rev['customer_id'] == username]
    del Tmp['customer_id']
    Tmp = Tmp[['product_id', 'review_score', 'seller_id']]
    return Tmp

def get_ProductDetail(username, product_id):
    details = Rev[(Rev['customer_id'] == username) & (Rev['product_id'] == product_id)]
    cat = Products[Products['product_id'] == product_id]['product_category_name'].values[0]
    return details, cat

def get_user_behavior(username):
    cat_list = []
    user_cat = Rev[Rev['customer_id'] == username]['product_id'].values
    for item in user_cat:
        item_cat = Products[Products['product_id'] == item]['product_category_name'].values[0]
        cat_list.append(item_cat)
    return mode(cat_list)

def getItemsReco(username):
    user_Test = Cf_Df.loc[Cf_Df['customer_id'] == username, 'product_id']
    product_to_predict = np.setdiff1d(unique_ids,user_Test)
    return product_to_predict

def getSVDReco(username):
    my_recs = []
    items = getItemsReco(username)
    for iid in items:
        my_recs.append((iid, SVD.predict(uid = username, iid = iid).est))
    Result = pd.DataFrame(my_recs, columns=['product_id', 'predictions']).sort_values('predictions', ascending=False).head(10)
    #Final_Result = TranslateReco(Result, state, city, cat)
    return Result

def getProductDetail(product_id):
    Result = Products[Products['product_id'] == product_id]
    return Result

# Cargue de usuarios
try:
    Users = pd.read_csv('Data/Df_Users.csv')
except Exception as Ex:
    print(f'Error al cargar Usarios: {Ex}')
print('Users Loaded! ')

# Cargue de reviews
try:
    Rev = pd.read_csv('Data/Df_Rev_v3.csv')
    del Rev['order_id']
except Exception as Ex:
    print(f'Error al cargar reviews: {Ex}')
print('Revs Loaded! ')

# Cargue de productos
try:
    Products = pd.read_csv('Data/olist_products_dataset.csv')
except Exception as Ex:
    print(f'Error al cargar Productos: {Ex}')
print('Prod Loaded! ')

# Cargue de modelo SVD
try:
    SVD = pickle.load(open('Data/Models/SVD_BA.pkl', 'rb'))
except Exception as Ex:
    print(f'Error al cargar el modelo: {Ex}')
print('SVD Model Loaded! ')

# Cargue de DF para el Modelo
try:
    Cf_Df = pd.read_csv('Data/CF_Df.csv')
    unique_ids = Cf_Df['product_id'].unique()
except Exception as Ex:
    print(f'Error al cargar reviews: {Ex}')
print('Revs Loaded! ')

print('All loaded!')
