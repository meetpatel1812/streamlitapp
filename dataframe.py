import streamlit as st
import pandas as pd
file_path = r"https://onedrive.live.com/edit?action=editnew&id=66879AA75AE22991!887&resid=66879AA75AE22991!887&ithint=file%2cxlsx&ct=1723967409801&wdNewAndOpenCt=1723967409400&wdOrigin=OFFICECOM-WEB.START.NEW&wdPreviousSessionSrc=HarmonyWeb&wdPreviousSession=d5409723-8c54-4750-98ff-a8068f404418&wdo=2&cid=66879aa75ae22991"
df = pd.read_excel(file_path, engine='openpyxl')
st.dataframe(df)
