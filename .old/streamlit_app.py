import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)

client=gspread.authorize(credentials)





sheet_key = st.secrets["private_gsheets_key"]

sheet = client.open_by_key(sheet_key)

df = pd.DataFrame(sheet.worksheet('TIME').get_values())
max_valid_col = 10
# Mantém apenas as primeiras 10 colunas
df = df.iloc[:, :max_valid_col]
# Usa a primeira linha como cabeçalho
df.columns = df.iloc[0]
# Descarta a primeira linha
df = df[1:]


st.write(df)