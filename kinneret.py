# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:39:28 2022

@author: aronp
"""
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import requests
import plotly.express as px

st.write('# Welcome')


# Loading the data

url = "https://data.gov.il/api/3/action/datastore_search?resource_id=b1d290c4-220b-494d-8376-0465789e972b&limit=99999"

r = requests.get(url)
dataset_kinneret_cl = (r.json())

df_kinneret_cl = pd.DataFrame(dataset_kinneret_cl['result']['records'])

url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=2de7b543-e13d-4e7e-b4c8-56071bc4d3c8&limit=5'

r = requests.get(url)
dataset_kinneret_cl = (r.json())

df_kinneret_cl["Kinneret Cl Level"] = df_kinneret_cl["תוצאה"].astype('float64')
df_kinneret_cl["Survey_Date"] = pd.to_datetime(
    df_kinneret_cl["תאריך ניטור"], format="%d/%m/%Y")

df_kinneret_cl['month'] = pd.to_datetime(
    df_kinneret_cl["Survey_Date"]).dt.month
df_kinneret_cl['year'] = pd.to_datetime(df_kinneret_cl["Survey_Date"]).dt.year
df_kinneret_cl_average = df_kinneret_cl.groupby(
    ['year', 'month'], as_index=False).mean()
#df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df_kinneret_cl, x="Survey_Date",
              y="Kinneret Cl Level", title='Kinneret Cl Level')
#sns.lineplot(x=df_kinneret_cl["Survey_Date"], y=df_kinneret_cl.loc[:,"Kinneret Cl Level"])
st.write(fig)
