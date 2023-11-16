# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:57:00 2023

@author: Josa -- josageof@gmail.com
"""

import streamlit as st
import pydeck as pdk


def track_map(cat_mbes_gdf, cat_sss_gdf, cat_sbp_gdf, cat_mbes_gdf_prod, cat_sss_gdf_prod, cat_sbp_gdf_prod):

    ## MBES
    mbes_lines = pdk.Layer(
        "GeoJsonLayer",
        cat_mbes_gdf,
        pickable=True,
        opacity=1,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_min_pixels=15,
        get_line_color="[255, 255, 255, 255]",
        get_fill_color="[255, 255, 255, 255]",
        )
    mbes_prod = pdk.Layer(
        "GeoJsonLayer",
        cat_mbes_gdf_prod,
        # pickable=True,
        opacity=1,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_min_pixels=15,
        get_line_color="[255, 0, 0, 255]",
        get_fill_color="[255, 0, 0, 255]",
        )

    ## SSS
    sss_lines = pdk.Layer(
        "GeoJsonLayer",
        cat_sss_gdf,
        pickable=True,
        opacity=1,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_min_pixels=10,
        get_line_color="[255, 255, 255, 255]",
        get_fill_color="[255, 255, 255, 255]",
        )
    sss_prod = pdk.Layer(
        "GeoJsonLayer",
        cat_sss_gdf_prod,
        # pickable=True,
        opacity=1,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_min_pixels=10,
        get_line_color="[255,165,0, 255]",
        get_fill_color="[255,165,0, 255]",
        )

    ## SBP
    sbp_lines = pdk.Layer(
        "GeoJsonLayer",
        cat_sbp_gdf,
        pickable=True,
        opacity=1,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_min_pixels=5,
        get_line_color="[255, 255, 255, 255]",
        get_fill_color="[255, 255, 255, 255]",
        )
    sbp_prod = pdk.Layer(
        "GeoJsonLayer",
        cat_sbp_gdf_prod,
        # pickable=True,
        opacity=1,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_min_pixels=5,
        get_line_color="[0, 128, 0, 255]",
        get_fill_color="[0, 128, 0, 255]",
        )

    initial_view = pdk.ViewState(
        latitude=-23, 
        longitude=-43, 
        zoom=6.5, 
        max_zoom=18,
        pitch=0, 
        bearing=0,
        wrapLongitude=True
    )

    m = pdk.Deck(
        initial_view_state=initial_view,
        # map_style=None,
        map_style="mapbox://styles/mapbox/satellite-streets-v12", 
        layers=[
                mbes_lines, mbes_prod,
                sss_lines, sss_prod,
                sbp_lines, sbp_prod,
                ],
        tooltip={"html": "<b>{Linha}</b>" + "<br>" +
                 ("Bloco: {Bloco}" if "{Bloco}" else "")
                 },
    )

    st.pydeck_chart(m, use_container_width=True)