'''
Gráficos estadísticos
'''




# Importaciones
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from streamlit_metrics import metric, metric_row
import streamlit.components.v1 as components
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt




# Variables globales
df = pd.DataFrame()




def configPage():
    '''
    Configura la pagina de Streamlit
    '''
    #configuraciones de la página
    st.set_page_config(
        page_title="EARTH DATA",
        layout="wide",
        initial_sidebar_state="expanded")

            
    page = """
    <style>
        [data-testid="stMetricLabel"] {
            color: #aaaaff;
            font-size: 25px;
            text-align: center;
        }

        [data-testid="metric-container"] {
            color: #ccccff;
            border-style: solid;
            border-radius: 20px;
            padding-left: 20px;
            padding-top: 10px;
        }
    </style>
    """
    st.markdown(page, unsafe_allow_html=True)
        



def cargarDatos():
    global df
    cone = create_engine(
                    'postgresql://airflow:airflow@localhost:5432/sismosdb', 
                    pool_size=50, 
                    max_overflow=0)

    qry = 'SELECT * FROM sismos;'
    df = pd.read_sql(sql=qry, con=cone)
    
    # Eliminamos los registros distorsionados de USA
    mask_1 = (df['idpais'] == 1) & \
                ((df['lat'] > 20.0) & (df['lat'] < 70.0) & (df['lng'] > -155.0) & (df['lng'] < -65.0))

    mask_2 = df['idpais'] == 2
    mask_3 = df['idpais'] == 3

    df = df[mask_1 | mask_2 | mask_3]

    df = df[df['mag'] != 0]

    df = df[df['deepth'] != 0]

    df['mag / deepth por mes'] = df['mag'] / df['deepth'].abs()

    # Entrenamos el modelo
    x = df[['mag', 'deepth']]
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(x)
    df['peligro'] = kmeans.labels_

    df = df.rename(columns={'lng':'lon'})




def main():
    global df

    configPage()
    cargarDatos()

    # Datos para los pie
    df_usa = df[df['idpais'] == 1]
    usa_0 = df_usa[df_usa['peligro'] == 0].shape[0]
    usa_1 = df_usa[df_usa['peligro'] == 1].shape[0]
    usa_2 = df_usa[df_usa['peligro'] == 2].shape[0]

    df_japon = df[df['idpais'] == 2]
    japon_0 = df_japon[df_japon['peligro'] == 0].shape[0]
    japon_1 = df_japon[df_japon['peligro'] == 1].shape[0]
    japon_2 = df_japon[df_japon['peligro'] == 2].shape[0]

    df_chile = df[df['idpais'] == 3]
    chile_0 = df_chile[df_chile['peligro'] == 0].shape[0]
    chile_1 = df_chile[df_chile['peligro'] == 1].shape[0]
    chile_2 = df_chile[df_chile['peligro'] == 2].shape[0]

    colA, colB, colC, colD, colE = st.columns([2.5, 1, 2.5, 1, 2.5])


    # USA
    with colA:
        st.metric('Máxima magnitud USA', df['mag'][df['idpais'] == 1].max())

        fig_1, ax_1 = plt.subplots()
        ax_1.set_title('Intensidades USA')
        ax_1.pie([usa_0, usa_1, usa_2], 
                  labels=['Suaves', 'Medios', 'Fuertes'], 
                  colors=['green', 'yellow', 'red'])

        fig_1.set_facecolor('black')
        st.pyplot(fig_1)

        st.line_chart(df_usa['mag / deepth por mes'].groupby(df_usa['time'].dt.month).max())


    # Japón
    with colC:
        st.metric('Máxima magnitud Japón', df['mag'][df['idpais'] == 2].max())

        fig_2, ax_2 = plt.subplots()
        ax_2.set_title('Intensidades Japón')
        ax_2.pie([japon_0, japon_1, japon_2], 
                  labels=['Suaves', 'Medios', 'Fuertes'],
                  colors=['green', 'yellow', 'red'])

        fig_2.set_facecolor('black')
        st.pyplot(fig_2)

        st.line_chart(df_japon['mag / deepth por mes'].groupby(df_japon['time'].dt.month).max())



    # Chile
    with colE:
        st.metric('Máxima magnitud Chile', df['mag'][df['idpais'] == 3].max())

        fig_3, ax_3 = plt.subplots()
        ax_3.set_title('Intensidades Chile')
        ax_3.pie([chile_0, chile_1, chile_2], 
                 labels=['Suaves', 'Medios', 'Fuertes'], 
                 colors=['green', 'yellow', 'red'])

        fig_3.set_facecolor('black')
        st.pyplot(fig_3)

        st.line_chart(df_chile['mag / deepth por mes'].groupby(df_chile['time'].dt.month).max())


if __name__ == '__main__':
    main()
