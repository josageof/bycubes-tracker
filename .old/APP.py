# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:57:00 2023

@author: Josa -- josageof@gmail.com
"""

import hmac

# import math
import pandas as pd
import geopandas as gpd
import streamlit as st

from utils.map import track_map
from utils.chart import area_chart
from utils.google_sheet_access import fetch_gsheet_data
from utils.components import comp_title, comp_resume, progress_bar

import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    layout="wide",
    page_title="byCubes Tracker",
    page_icon="🗺️",
)

# %%===========================================================================
# !!! DEFINITIONS

# Local CSS
def local_css(css_name):
    with open(css_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")


# def calcular_bloco(LAYER):
#     if LAYER.startswith("Unknown"):
#         pass
#     else:
#         partes = LAYER.replace(' ', '').split('-')
#         numero = int(partes[-1])
#         return math.ceil(numero / 3)


# @st.cache_data
def get_geo_data(*args):
    gdf_list = []
    for file in args:
        try:
            ## Cria uma lista com as gdfs passadas
            gdf_list.append(gpd.read_file(file))
        except Exception as e:
            print(f"Erro ao ler o arquivo {file}: {e}")
    if gdf_list:
        cat_gdf = pd.concat(gdf_list, ignore_index=True)
        ## Calcula Bloco baseado na Linha
        # cat_gdf['Bloco'] = cat_gdf['LAYER'].apply(calcular_bloco)
        if 'Bloco' not in cat_gdf.columns:
            cat_gdf['Bloco'] = cat_gdf['LAYER'].str.extract(r'- (\d+) -')
        ## Padroniza a coluna 'Linha' para remover zeros à esquerda
        cat_gdf['_Linha'] = cat_gdf['Linha'].str.replace(r'0', '', regex=True)
        return cat_gdf
    else:
        return None

## Converte comprimentos para metros removendo unidades ('m' ou 'km').
def length_to_meters(comprimento):

    valor = float(str(comprimento).replace(' km', '').replace(' m', ''))
    if 'km' in str(comprimento):
        valor *= 1000

    return valor


## Processa os dados de duração vindos do RDO
def rdo_data_proc(df):
    # Converte a coluna data para date
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y").dt.date
    # Preenche os valores nan com zeros
    df.iloc[:, 1:9] = df.iloc[:, 1:9].fillna("0:00")
    # Converte colunas de tempo para o formato desejado (HH:MM)
    for col in df.columns[1:9]:
        df[col] = pd.to_datetime(df[col], format="%H:%M", errors='coerce') - pd.to_datetime("1900-01-01 00:00")
        # df[col] = pd.to_datetime(df[col], format="%H:%M:%S")
        # df[col] = df[col].dt.strftime('%H:%M')
    return df


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    ## Componente de título
    st.markdown(comp_title(), unsafe_allow_html=True)

    # O componente st.text_input será renderizado dentro da div
    st.text_input("Digite sua palavra-chave:", type="password", on_change=password_entered, key="password", )

    if "password_correct" in st.session_state:
        st.error("😕 Palavra-chave incorreta")
    return False


# %%===========================================================================
# !!! DATA

#!!! --- GEODATA ---
## Importa os dados geo dos shapefiles
cat_mbes_gdf = get_geo_data(
    "data/RT2/TR2022027_Pre-Plot_C2_RT2_MBE.shp", 
    "data/RT3/TR2022027_Pre-Plot_C2_RT3_MBE.shp",
    "data/MEX/TR2022027_Pre-Plot_C2_MEX_MBE.shp",
    "data/PR1/TR2022027_Pre-Plot_C2_PR1_MBE.shp"
    )
cat_sss_gdf = get_geo_data(
    "data/RT2/TR2022027_Pre-Plot_C2_RT2_S.shp", 
    "data/RT3/TR2022027_Pre-Plot_C2_RT3_S.shp",
    "data/MEX/TR2022027_Pre-Plot_C2_MEX_S.shp",
    )
cat_sbp_gdf = get_geo_data(
    "data/RT2/TR2022027_Pre-Plot_C2_RT2_R.shp", 
    "data/RT3/TR2022027_Pre-Plot_C2_RT3_R.shp",
    "data/MEX/TR2022027_Pre-Plot_C2_MEX_R.shp",
    )

## Quantidades total de linhas (MBES, SSS, SBP)
qde_mbes_lines = len(cat_mbes_gdf)
qde_sss_lines = len(cat_sss_gdf)
qde_sbp_lines = len(cat_sbp_gdf)

## Quantidades total de metros (MBES, SSS, SBP)
cat_mbes_gdf['LENGTH'] = cat_mbes_gdf['LENGTH'].apply(length_to_meters)
cat_sss_gdf['LENGTH'] = cat_sss_gdf['LENGTH'].apply(length_to_meters)
cat_sbp_gdf['LENGTH'] = cat_sbp_gdf['LENGTH'].apply(length_to_meters)
qde_mbes_mts = cat_mbes_gdf['LENGTH'].sum()
qde_sss_mts = cat_sss_gdf['LENGTH'].sum()
qde_sbp_mts = cat_sbp_gdf['LENGTH'].sum()


# @st.cache_data(ttl=60)
def load_prod_data():
    sh_key = st.secrets["private_gsheets_key"]
    gcp_creds = st.secrets["gcp_service_account"]
    df_rdo_times = fetch_gsheet_data(gcp_creds, sh_key, "TIME", 10)
    df_prod_rt2 = fetch_gsheet_data(gcp_creds, sh_key, "RT2", 10)
    df_prod_rt3 = fetch_gsheet_data(gcp_creds, sh_key, "RT3", 10)
    df_prod_mex = fetch_gsheet_data(gcp_creds, sh_key, "MEX", 10)
    df_prod_pr1 = fetch_gsheet_data(gcp_creds, sh_key, "PR1", 10)
    return df_rdo_times, df_prod_rt2, df_prod_rt3, df_prod_mex, df_prod_pr1



#!!! --- PRODUCAO ---
## Importa os dados de produção da planilha google "__PRODUCAO_PIDR1_C2__"
try:
    df_rdo_times, df_prod_rt2, df_prod_rt3, df_prod_mex, df_prod_pr1 = load_prod_data()
except:
    st.warning('Você excedeu a cota de uso do Google Cloud API. Espere 3 minutos e tente novamente.')
    st.stop()

## Concatena as df de produção
cat_df_prod = pd.concat([df_prod_rt2, 
                         df_prod_rt3, 
                         df_prod_mex, 
                         df_prod_pr1], ignore_index=True)

## Padroniza a coluna 'Linha' para remover zeros à esquerda
# cat_df_prod['_Linha'] = cat_df_prod['Linha'].str.replace(r'(?<=\D)0', '', regex=True)

## Separa apenas as linha Aquisitadas
df_aquisicao = cat_df_prod[cat_df_prod['Aquisição'] != ""]
df_aquisicao.reset_index(drop=True, inplace=True)

## Separa as linhas Aquisitadas por método
df_aquisicao_mbes = df_aquisicao[df_aquisicao['Método'] == 'MBES']
df_aquisicao_sss = df_aquisicao[df_aquisicao['Método'] == 'SSS']
df_aquisicao_sbp = df_aquisicao[df_aquisicao['Método'] == 'SBP']

## Separa os gdf apenas dos trecho produzidos para cada método
cat_mbes_gdf_prod = cat_mbes_gdf.merge(df_aquisicao_mbes, on='Linha', how='inner')
cat_sss_gdf_prod = cat_sss_gdf.merge(df_aquisicao_sss, on='Linha', how='inner')
cat_sbp_gdf_prod = cat_sbp_gdf.merge(df_aquisicao_sbp, on='Linha', how='inner')


## Se há alguma produção...
if len(cat_mbes_gdf_prod):
    ## Aquisição de dados (MBES)
    cat_mbes_gdf_prod['Aquisição'] = pd.to_datetime(cat_mbes_gdf_prod['Aquisição'], format='%d/%m/%Y')

    ## Penúltimo dia de produção se houve mais que um
    if len(cat_mbes_gdf_prod) == 1:
        prelast_mbes_acq_day = cat_mbes_gdf_prod['Aquisição'].max()
    else:
        prelast_mbes_acq_day = cat_mbes_gdf_prod['Aquisição'].sort_values().unique()[-2]

    ## Último dia de produção
    last_mbes_acq_day = cat_mbes_gdf_prod['Aquisição'].max()
    last_mbes_acq_day_form = last_mbes_acq_day.strftime('%d/%m/%Y')

    ## Produção do penúltimo dia (MBES)
    prod_prelast_mbes_acq_day = (cat_mbes_gdf_prod['Aquisição'] == prelast_mbes_acq_day).sum()

    ## Produção do último dia (MBES)
    prod_last_mbes_acq_day = (cat_mbes_gdf_prod['Aquisição'] == last_mbes_acq_day).sum()

    ## Diferença de produção entre último e penultimo dia (MBES)
    diff_prod_mbes = prod_last_mbes_acq_day - prod_prelast_mbes_acq_day

    ## Quantidades de linhas adquiridas (MBES)
    qde_mbes_lines_acq = cat_mbes_gdf_prod['Aquisição'].apply(lambda x: x != '').sum()

    ## Quantidades de linhas aprovadas QC (MBES)
    qde_mbes_lines_qc = cat_mbes_gdf_prod['Aprovação QC'].apply(lambda x: x != '').sum()

    ## Quantidades de linhas aprovadas Pro (MBES)
    qde_mbes_lines_pro = cat_mbes_gdf_prod['Aprovação Pro'].apply(lambda x: x != '').sum()

    ## Quantidades de metros adquiridos (MBES)
    prod_mbes_mts = cat_mbes_gdf_prod['LENGTH'].sum()
else:
    last_mbes_acq_day_form = " "
    prod_last_mbes_acq_day = 0
    diff_prod_mbes = 0
    qde_mbes_lines_acq = 0
    qde_mbes_lines_qc = 0
    qde_mbes_lines_pro = 0
    prod_mbes_mts = 0


## Se há alguma produção...
if len(cat_sss_gdf_prod):
    ## Aquisição de dados (SSS)
    cat_sss_gdf_prod['Aquisição'] = pd.to_datetime(cat_sss_gdf_prod['Aquisição'], format='%d/%m/%Y')

    ## Penúltimo dia de produção se houve mais que um
    if len(cat_sss_gdf_prod) == 1:
        prelast_sss_acq_day = cat_sss_gdf_prod['Aquisição'].max()
    else:
        prelast_sss_acq_day = cat_sss_gdf_prod['Aquisição'].sort_values().unique()[-2]

    ## Último dia de produção
    last_sss_acq_day = cat_sss_gdf_prod['Aquisição'].max()
    last_sss_acq_day_form = last_sss_acq_day.strftime('%d/%m/%Y')

    ## Produção do penúltimo dia (SSS)
    prod_prelast_sss_acq_day = (cat_sss_gdf_prod['Aquisição'] == prelast_sss_acq_day).sum()

    ## Produção do último dia (SSS)
    prod_last_sss_acq_day = (cat_sss_gdf_prod['Aquisição'] == last_sss_acq_day).sum()

    ## Diferença de produção entre último e penultimo dia (SSS)
    diff_prod_sss = prod_last_sss_acq_day - prod_prelast_sss_acq_day

    ## Quantidades de linhas adquiridas (SSS)
    qde_sss_lines_acq = cat_sss_gdf_prod['Aquisição'].apply(lambda x: x != '').sum()

    ## Quantidades de linhas aprovadas QC (SSS)
    qde_sss_lines_qc = cat_sss_gdf_prod['Aprovação QC'].apply(lambda x: x != '').sum()

    ## Quantidades de linhas aprovadas Pro (SSS)
    qde_sss_lines_pro = cat_sss_gdf_prod['Aprovação Pro'].apply(lambda x: x != '').sum()

    ## Quantidades de metros adquiridos (SSS)
    prod_sss_mts = cat_sss_gdf_prod['LENGTH'].sum()
else:
    last_sss_acq_day_form = " "
    prod_last_sss_acq_day = 0
    diff_prod_sss = 0
    qde_sss_lines_acq = 0
    qde_sss_lines_qc = 0
    qde_sss_lines_pro = 0
    prod_sss_mts = 0


## Se há alguma produção...
if len(cat_sbp_gdf_prod):
    ## Aquisição de dados (SBP)
    cat_sbp_gdf_prod['Aquisição'] = pd.to_datetime(cat_sbp_gdf_prod['Aquisição'], format='%d/%m/%Y')

    ## Penúltimo dia de produção se houve mais que um
    if len(cat_sbp_gdf_prod) == 1:
        prelast_sbp_acq_day = cat_sbp_gdf_prod['Aquisição'].max()
    else:
        prelast_sbp_acq_day = cat_sbp_gdf_prod['Aquisição'].sort_values().unique()[-2]

    ## Último dia de produção
    last_sbp_acq_day = cat_sbp_gdf_prod['Aquisição'].max()
    last_sbp_acq_day_form = last_sbp_acq_day.strftime('%d/%m/%Y')

    ## Produção do penúltimo dia (SBP)
    prod_prelast_sbp_acq_day = (cat_sbp_gdf_prod['Aquisição'] == prelast_sbp_acq_day).sum()

    ## Produção do último dia (SBP)
    prod_last_sbp_acq_day = (cat_sbp_gdf_prod['Aquisição'] == last_sbp_acq_day).sum()

    ## Diferença de produção entre último e penultimo dia (SBP)
    diff_prod_sbp = prod_last_sbp_acq_day - prod_prelast_sbp_acq_day

    ## Quantidades de linhas adquiridas (SBP)
    qde_sbp_lines_acq = cat_sbp_gdf_prod['Aquisição'].apply(lambda x: x != '').sum()

    ## Quantidades de linhas aprovadas QC (SBP)
    qde_sbp_lines_qc = cat_sbp_gdf_prod['Aprovação QC'].apply(lambda x: x != '').sum()

    ## Quantidades de linhas aprovadas Pro (SBP)
    qde_sbp_lines_pro = cat_sbp_gdf_prod['Aprovação Pro'].apply(lambda x: x != '').sum()

    ## Quantidades de metros adquiridos (SBP)
    prod_sbp_mts = cat_sbp_gdf_prod['LENGTH'].sum()

else:
    last_sbp_acq_day_form = " "
    prod_last_sbp_acq_day = 0
    diff_prod_sbp = 0
    qde_sbp_lines_acq = 0
    qde_sbp_lines_qc = 0
    qde_sbp_lines_pro = 0
    prod_sbp_mts = 0



# %%===========================================================================
# !!! PAGE

# --- CHECK AUTHENTICATION ---
if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# --- HEADER ---
APP_TITLE = "Projeto TR2022027_Petrobras_Geofisica (Campanha 2)"
st.markdown(f"<h1 style='text-align: center;'>{APP_TITLE}</h1>", unsafe_allow_html=True)

# --- BODY ---
with st.container():
    column1, column2, column3, column4, column5, column6 = st.columns((1,1,1,1,1,1))
    column1.metric(label=f"Aquisição MBES ({last_mbes_acq_day_form})", value=f"{prod_last_mbes_acq_day} Linhas", delta=f"{diff_prod_mbes}")
    column2.markdown(comp_resume("#FF0000", 
                                 qde_mbes_lines, 
                                 qde_mbes_lines_acq, 
                                 qde_mbes_lines_qc, 
                                 qde_mbes_lines_pro,
                                 ), unsafe_allow_html=True)
    column3.metric(label=f"Aquisição SSS ({last_sss_acq_day_form})", value=f"{prod_last_sss_acq_day} Linhas", delta=f"{diff_prod_sss}")
    column4.markdown(comp_resume("#FFA500", 
                                 qde_sss_lines, 
                                 qde_sss_lines_acq, 
                                 qde_sss_lines_qc, 
                                 qde_sss_lines_pro,
                                 ), unsafe_allow_html=True)
    column5.metric(label=f"Aquisição SBP ({last_sbp_acq_day_form})", value=f"{prod_last_sbp_acq_day} Linhas", delta=f"{diff_prod_sbp}")
    column6.markdown(comp_resume("#008000", 
                                 qde_sbp_lines, 
                                 qde_sbp_lines_acq, 
                                 qde_sbp_lines_qc, 
                                 qde_sbp_lines_pro,
                                 ), unsafe_allow_html=True)

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        ## Track map
        track_map(cat_mbes_gdf, cat_sss_gdf, cat_sbp_gdf, 
                  cat_mbes_gdf_prod, cat_sss_gdf_prod, cat_sbp_gdf_prod)
    with right_column:
        ## Time chart
        area_chart(rdo_data_proc(df_rdo_times))

# --- BODY ---
# st.markdown(progress_bar(qde_mbes_mts, qde_sss_mts, qde_sbp_mts, 
#                          prod_mbes_mts, prod_sss_mts, prod_sbp_mts), unsafe_allow_html=True)

with st.container():
    left_col, right_col = st.columns((9,1))
    with left_col:
        st.markdown(progress_bar(qde_mbes_mts, qde_sss_mts, qde_sbp_mts, 
                                 prod_mbes_mts, prod_sss_mts, prod_sbp_mts), unsafe_allow_html=True)
    with right_col:
        if st.button("Rerun"):
            st.rerun()