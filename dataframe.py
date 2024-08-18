import streamlit as st
import pandas as pd

df = pd.read_excel("test.xlsx", engine='openpyxl')
st.dataframe(df)