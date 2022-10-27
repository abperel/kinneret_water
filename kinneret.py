# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:39:28 2022

@author: aronp
"""
from scipy.stats.stats import pearsonr
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.write('# EDA Lake Kinneret level vs Cl')


st.subheader("""This is an EDA to compare the water level with Cl level of lake Kinneret in Israel. \n - The first chart is a Time Series of water and cl level against time.\n - The second chart shows the relation between the levels and cl.
        """)

# Loading the data

url = "https://data.gov.il/api/3/action/datastore_search?resource_id=b1d290c4-220b-494d-8376-0465789e972b&limit=99999"

r = requests.get(url)
dataset_kinneret_cl = (r.json())

df_kinneret_cl = pd.DataFrame(dataset_kinneret_cl['result']['records'])

url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=2de7b543-e13d-4e7e-b4c8-56071bc4d3c8&limit=99999'

r = requests.get(url)
dataset_kinneret_level = (r.json())

df_kinneret_cl["Kinneret Cl Level"] = df_kinneret_cl["תוצאה"].astype('float64')
df_kinneret_cl["Survey_Date"] = pd.to_datetime(
    df_kinneret_cl["תאריך ניטור"], format="%d/%m/%Y")

df_kinneret_cl.drop(
    ['_id', 'עומק הדגימה במטרים', 'תוצאה'], inplace=True, axis=1)

df_kinneret_cl['month'] = pd.to_datetime(
    df_kinneret_cl["Survey_Date"]).dt.month
df_kinneret_cl['year'] = pd.to_datetime(df_kinneret_cl["Survey_Date"]).dt.year
df_kinneret_cl_average = df_kinneret_cl.groupby(
    ['year', 'month'], as_index=False).mean()


filtered_kinneret = (dataset_kinneret_level['result']['records'])
df_kinneret = pd.DataFrame(filtered_kinneret)

df_kinneret['Kinneret_Level'] = df_kinneret['Kinneret_Level'].astype('float64')
df_kinneret["Survey_Date"] = pd.to_datetime(
    df_kinneret["Survey_Date"], format="%Y%m%dT%H:%M:%S")

df_kinneret.drop('_id', inplace=True, axis=1)

print(df_kinneret)
df_kinneret['month'] = pd.to_datetime(df_kinneret["Survey_Date"]).dt.month
df_kinneret['year'] = pd.to_datetime(df_kinneret["Survey_Date"]).dt.year
print(df_kinneret)

df_kinneret_average = df_kinneret.groupby(
    ['year', 'month'], as_index=False).mean(numeric_only=True)
print(df_kinneret_average)


merged_df = pd.merge(df_kinneret_average, df_kinneret_cl_average, how='inner')
merged_df['DATE'] = pd.to_datetime(merged_df[['year', 'month']].assign(DAY=1))
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=merged_df['DATE'], y=merged_df.loc[:,
                                                    "Kinneret Cl Level"], name="Kinneret Cl Level(mg/l)"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=merged_df['DATE'], y=merged_df.loc[:,
                                                    'Kinneret_Level'], name="Kinneret Level(m)"),
    secondary_y=True,
)

fig.update_layout(legend=dict(orientation="h",
                              yanchor="top",
                              y=1.11,
                              xanchor="left",
                              x=0.01
                              ))
fig.update_layout(
    title="Time Series (Kinneret level and Cl)",
    xaxis_title="Date",
    yaxis_title="Cl level(mg/l)")

fig.update_yaxes(title_text="Level(m)", secondary_y=True)
# fig.update_xaxes
st.write(fig)

st.text('It can be noticed that there is some kind of an opposite (mirror) trend between the\nwater and cl levels, this could be confirmed by looking at their correlation (next).')


fig3 = px.scatter(merged_df, x="Kinneret_Level", y="Kinneret Cl Level",
                  trendline="ols", color_discrete_sequence=['green'],
                  title="Kinneret level vs Cl")
fig3.update_layout(

    xaxis_title="Level(m)",
    yaxis_title="Cl level(mg/l)")
st.write(fig3)


st.write(pearsonr(merged_df.loc[:, 'Kinneret_Level'],
         merged_df.loc[:, 'Kinneret Cl Level']))
st.text('From here it can be seen that there is an inverse correlation between the level\nof water and Cl')

print(' ')
st.markdown('**Acknowledgements:** The data is obtained with an API call from the Israeli government database site: https://info.data.gov.il/')
