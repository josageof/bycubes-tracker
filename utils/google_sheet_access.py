# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:28:12 2023

@author: Josa -- josageof@gmail.com
"""

import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread


def fetch_gsheet_data(gcp_creds, sheet_key, worksheet, max_col):

    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        gcp_creds,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
        ],
    )
    client=gspread.authorize(credentials)


    sheet = client.open_by_key(sheet_key)
    df = pd.DataFrame(sheet.worksheet(worksheet).get_values())

    # Mantém apenas as primeiras 10 colunas
    df = df.iloc[:, :max_col]
    # Usa a primeira linha como cabeçalho
    df.columns = df.iloc[0]
    # Descarta a primeira linha
    df = df[1:]
    return df
