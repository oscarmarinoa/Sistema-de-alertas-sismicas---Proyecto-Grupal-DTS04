'''
Página principal de Streamlit
'''

# Importaciones
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import streamlit as st
import pydeck as pdk
from streamlit_metrics import metric, metric_row
import streamlit.components.v1 as components
import folium as folium
import leafmap as leafmap
#import leafmap.foliumap as lf
from streamlit_folium import st_folium, folium_static
import matplotlib.colors as colors
import branca
import branca.colormap as cm
import matplotlib.cm as cm2
from sklearn.cluster import KMeans
import datetime    



def configPage():
    '''
    Configura la pagina de Streamlit
    '''
    #configuraciones de la página
    st.set_page_config(
        page_title="Earth Data",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded")

    #Título principál de la página
    st.title("EARTH DATA")        


def cargarDatos():
    global df
    cone = create_engine(
                    'postgresql://airflow:airflow@localhost:5432/sismosdb', 
                    pool_size=50, 
                    max_overflow=0)

    qry = 'SELECT * FROM sismos;'
    df = pd.read_sql(sql=qry, con=cone)

    # minlatitude=23.300000
    # maxlatitude=69.400000
    # minlongitude=-160.000000
    # maxlongitude=-69.500000
    
    # Eliminamos los registros distorsionados de USA
    mask_1 = (df['idpais'] == 1) & \
                ((df['lat'] > 20.0) & (df['lat'] < 70.0) & (df['lng'] > -155.0) & (df['lng'] < -65.0))

    mask_2 = df['idpais'] == 2
    mask_3 = df['idpais'] == 3

    df = df[mask_1 | mask_2 | mask_3]

    # Entrenamos el modelo
    x = df[['mag', 'deepth']]
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(x)
    df['peligro'] = kmeans.labels_

    df = df.rename(columns={'lng':'lon'})


def main():
    configPage()
    global df

    val_pais = 0
    val_int = 2
    
    # Acciones previas
    cargarDatos()

    # Valores de seteo
    fecha_desde = df['time'].min()
    fecha_hasta = df['time'].max()
    fecha_max_sel = fecha_hasta

    paises = ['Todos', 'USA', 'Japón', 'Chile']

    intensidades = ['Fuerte', 'Media', 'Suave']

    # Contenedor principal
    c = st.container()
    
    with st.sidebar:
        # título
        st.header(('¿Qué te gustaría ver?'))

        # Filtro de fechas
        fecha_min_sel = st.date_input(
            label='Fecha desde:',
            value=fecha_desde,
            min_value=fecha_desde,
            max_value=fecha_max_sel
        )
        
        fecha_max_sel = st.date_input(
            label='Fecha hasta:',
            value=fecha_hasta,
            min_value=fecha_min_sel,
            max_value=fecha_hasta
        )

        pais = st.radio('País:', paises)
        if pais == 'Todos':
            val_pais = 0
        if pais == 'USA':
            val_pais = 1
        if pais == 'Japón':
            val_pais = 2
        if pais == 'Chile':
            val_pais = 3

        color = [255, 0, 0]
        intensidad = st.radio('Intensidad:', intensidades)
        if intensidad == 'Fuerte':
            val_int = 2
            color = [255, 0, 0]
        if intensidad == 'Media':
            val_int = 1
            color = [255, 255, 0]
        if intensidad == 'Suave':
            val_int = 0
            color = [0, 255, 0 ]


        # Mostramos los datos filtrados
        if val_pais != 0:
            datos = df[(df['idpais'] == val_pais) &
                                       (df['peligro'] == val_int) &
                                       (df['time'].dt.date >= fecha_min_sel) &
                                       (df['time'].dt.date <= fecha_max_sel)
                                       ]
        else:
            datos = df[(df['peligro'] == val_int) &
                                       (df['time'].dt.date >= fecha_min_sel) &
                                       (df['time'].dt.date <= fecha_max_sel)
                                       ]
                                    
          
        c.map(data=datos[['lat', 'lon']])

        csv = datos.to_csv(index=False).encode('utf-8')

        c.download_button(
            "Descargar Datos Filtrados",
            csv,
            "sismos_filtro.csv",
            "text/csv",
            key='download-csv'
            )
        
                

    layer = pdk.Layer(
        "ScatterplotLayer",
        datos,
        pickable=True,
        opacity=0.6,
        filled=True,
        radius_scale=1,
        radius_min_pixels=3,
        radius_max_pixels=6,
        line_width_min_pixels=0.01,
        get_position='[lon, lat]',
        get_fill_color=color,
        get_line_color=[0, 0, 0],
    )
    #zoom=13, min_zoom= 10, max_zoom=30
    # Set the viewport location
    view_state = pdk.ViewState(latitude=20, longitude=-100, zoom=4)
    
    #mapbox://styles/mapbox/dark-v11
    #mapbox://styles/mapbox/navigation-day-v1
    #mapbox://styles/mapbox/streets-v12
    #mapbox://styles/mapbox/outdoors-v12
    #mapbox://styles/mapbox/light-v11
    #mapbox://styles/mapbox/satellite-v9
    #mapbox://styles/mapbox/satellite-streets-v12
    #mapbox://styles/mapbox/navigation-day-v1
    # Render
    r = pdk.Deck(layers=[layer], map_style='mapbox://styles/mapbox/dark-v11',
                initial_view_state=view_state, tooltip={"html": "<b>Magnitud: </b> {mag} <br /> "
                                                                "<b>Longitude: </b> {lon} <br /> "
                                                                "<b>Latitude: </b>{lat} <br /> "
                                                                "<b> Intensidad: </b>{peligro}"})
    r


if __name__ == '__main__':
    main()

    
  