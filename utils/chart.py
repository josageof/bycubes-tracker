# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:57:00 2023

@author: Josa -- josageof@gmail.com
"""

import streamlit as st
import plotly.graph_objs as go


def area_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        name="Navegação",
        x=df['data'], 
        y=df['navegação'],
        text=df['navegação'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(25, 211, 243, 1.0)',
            line=dict(color='rgba(21, 114, 130, 1.0)', width=2)
        )
    ))
    
    fig.add_trace(go.Scatter(
        name="Mobilização",
        x=df['data'], 
        y=df['mobilização'],
        text=df['mobilização'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(0, 204, 150, 1.0)',
            line=dict(color='rgba(8, 110, 83, 1.0)', width=2)
        )
    ))
    
    fig.add_trace(go.Scatter(
        name="Aquisição",
        x=df['data'], 
        y=df['aquisição'],
        text=df['aquisição'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(99, 110, 250, 1.0)',
            line=dict(color='rgba(58, 63, 133, 1.0)', width=2)
        )
    ))
    
    fig.add_trace(go.Scatter(
        name="Reaquisição",
        x=df['data'], 
        y=df['reaquisição'],
        text=df['reaquisição'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(171, 99, 250, 1.0)',
            line=dict(color='rgba(94, 58, 133, 1.0)', width=2)
        )
    ))
    
    fig.add_trace(go.Scatter(
        name="Standby",
        x=df['data'], 
        y=df['standby'],
        text=df['standby'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(255, 161, 90, 1.0)',
            line=dict(color='rgba(136, 89, 53, 1.0)', width=2)
        )
    ))
    
    fig.add_trace(go.Scatter(
        name="Downtime",
        x=df['data'], 
        y=df['downtime'],
        text=df['downtime'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(239, 85, 59, 1.0)',
            line=dict(color='rgba(128, 51, 38, 1.0)', width=2)
        )
    ))

    fig.add_trace(go.Scatter(
        name="fundeio",
        x=df['data'], 
        y=df['fundeio'],
        text=df['fundeio'],
        mode='lines',
        stackgroup='one',
        textfont_color='white',
        marker=dict(
            color='rgba(77, 77, 77, 1.0)',
            line=dict(color='rgba(77, 77, 77, 1.0)', width=2)
        )
    ))
    
    fig.update_layout(xaxis=dict(dtick="D1"))
    
    fig.update_layout(legend=dict(orientation="h",
                                  x=1.0,
                                  y=1.0,
                                  xanchor='right',
                                  yanchor='bottom'),
                      legend_traceorder="normal")
    
    fig.update_layout({"title": '',
                        "xaxis": {"title": "Dia"},
                        "yaxis": {"title": "Tempo"},
                        "showlegend": True},
                      titlefont=dict(size=24),
                      template="plotly_dark")
    
    fig.update_layout(margin=dict(l=75, r=15, t=0, b=0),
                      autosize=False, height=500)
    
    return st.plotly_chart(fig, use_container_width=True, height=800)
