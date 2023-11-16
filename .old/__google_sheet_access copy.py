# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:28:12 2023

@author: Josa -- josageof@gmail.com
"""

## pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

# from IPython import get_ipython
# get_ipython().run_line_magic('reset', '-f')

# from __future__ import print_function

import os.path
import pandas as pd
import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

token_file = 'utils/egs/token.json'
# credentials_file = 'utils/egs/credentials.json'

def fetch_gsheet_data(spreadsheet_id, range_name):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):

        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        # creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open(token_file, 'w') as token:
    #         token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        #!!! Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        else:
            data = pd.DataFrame(values[1:], columns=values[0])
            ## substitui celulas com espaços por None
            data = data.replace(r'^\s*$', None, regex=True)
            # Identificar os índices das linhas que contêm a string "#VALUE!" em qualquer célula
            indices_a_excluir = data[data.apply(lambda row: "#VALUE!" in row.values, axis=1)].index
            # Deletar as linhas identificadas acima
            data = data.drop(indices_a_excluir)
            ## tolera até 5 linhas None
            return data.dropna(thresh=1)
    
    except HttpError as err:
        print(err)

