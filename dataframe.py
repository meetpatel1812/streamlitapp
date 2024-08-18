import streamlit as st
import pandas as pd
file_path = r"https://1drv.ms/x/s!ApEp4lqnmodmhnda293x2jLaGTtP?e=gYKaje&nav=MTVfezAwMDAwMDAwLTAwMDEtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMH0"
df = pd.read_excel(file_path, engine='openpyxl')
st.dataframe(df)
