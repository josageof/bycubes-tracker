# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:57:00 2023

@author: Josa -- josageof@gmail.com
"""


def comp_title():

    # Contêiner do título
    container_style = """
        background-color: #0E1117;
        border: 15px solid white;
        border-radius: 5px;
        padding: 15px 30px 20px 30px;
        width: 50%;
        position: absolute;
        left: 25%;
        margin-top: 31vh;
        text-align: center;
    """

    # Cria o HTML com o título
    html = f"""
        <div style="{container_style}">
            <h1 style="color: white;">📅 TR2022027 Tracker 📊</h1>
        </div>
    """
    return html


def comp_resume(cor, total, acq, qc, pro):
    # Títulos e valores
    titulos = ["Total de Linhas:", "Linhas Adquiridas:", "Aprovadas QC:", "Aprovadas Pro:"]
    valores = [str(total), str(acq), str(qc), str(pro)]
    
    # Criar o HTML com duas colunas
    html = """
        <div style="display: flex; justify-content: space-between; padding:15px 30px; font-size: 14px">
            <div style="flex: 3">
                <div>{}</div>
                <div>{}</div>
                <div>{}</div>
                <div>{}</div>
            </div>
            <div style="flex: 1; font-weight: bold; color: {};">
                <div>{}</div>
                <div>{}</div>
                <div>{}</div>
                <div>{}</div>
            </div>
        </div>
    """.format(*titulos, cor, *valores)
    return html


def progress_bar(qde_mbes_mts, qde_sss_mts, qde_sbp_mts, pro_mbes_mts, pro_sss_mts, pro_sbp_mts):

    mbes_prog = int((pro_mbes_mts/qde_mbes_mts)*100)
    sss_prog = int((pro_sss_mts/qde_sss_mts)*100)
    sbp_prog = int((pro_sbp_mts/qde_sbp_mts)*100)

    # Função para criar o estilo da barra de progresso
    def barra_style(progresso, cor):
        return f"""
            width: {progresso}%; 
            height: 2px; 
            background-color: {cor}; 
            position: relative;
        """

    # Contêiner da barra de progresso
    container_style = """
        position: relative;
        padding: 20px 30px 30px 30px;
    """

    # HTML para a barra de progresso
    html = f"""
        <div style="{container_style}">
            <div style="{barra_style(mbes_prog, '#ff0000')}"></div>
            MBES &nbsp;&nbsp; - &nbsp;&nbsp; {int(pro_mbes_mts/1000)} de {int(qde_mbes_mts/1000)} km &nbsp;&nbsp; - &nbsp;&nbsp; {mbes_prog} %
            <div style="{barra_style(sss_prog, '#ffa500')}"></div>
            SSS &nbsp;&nbsp; - &nbsp;&nbsp; {int(pro_sss_mts/1000)} de {int(qde_sss_mts/1000)} km &nbsp;&nbsp; - &nbsp;&nbsp; {sss_prog} %
            <div style="{barra_style(sbp_prog, '#008000')}"></div>
            SBP &nbsp;&nbsp; - &nbsp;&nbsp; {int(pro_sbp_mts/1000)} de {int(qde_sbp_mts/1000)} km &nbsp;&nbsp; - &nbsp;&nbsp; {sbp_prog} %
        </div>
    """
    return html
