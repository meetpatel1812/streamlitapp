import streamlit as st
import pandas as pd

df = pd.read_excel("https://1drv.ms/x/s!ApEp4lqnmodmhnda293x2jLaGTtP?e=gYKaje&nav=MTVfezAwMDAwMDAwLTAwMDEtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMH0", engine='openpyxl')
st.dataframe(df)
