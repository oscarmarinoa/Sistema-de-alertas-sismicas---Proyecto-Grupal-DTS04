#LIBRERIAS NECESARIAS:
#Para utilizar API
import requests
#Para realizar la estructura tabular
import pandas as pd

#ETL:
#para normalizar strings
from unicodedata import normalize
#para normalizar incluyendo la ñ
import re 
#hacer los calendarios de iteración
from dateutil.rrule import rrule, DAILY , MONTHLY

#Para append los datos a ingestar en la tabla
#from sqlalchemy import create_engine

#Web Scraping
from bs4 import BeautifulSoup

from airflow.models import DAG
import datetime as dt
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

#Web scraping
#Permiso de la web
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
#desactivamos los request
disable_warnings(InsecureRequestWarning)


usa = 1
japon = 2
chile = 3



'''================================ USA ==========================='''

def limpieza_general_tabla(df):
    '''
    Función: limpieza de cadenas de string
    Entrada: Data Frame a normalizar
    Devuelve:  el df ingestado con normalizaciones
    '''
    #Vemos duplicados y existen los eliminamos
    df.drop_duplicates(inplace=True) 

    #Acomodamos el indice
    df.reset_index(drop=True, inplace=True)
  
    #recorremos cada columna del dataset con un bucle
    for c in df.columns:         
        #Detectamos las columnas que son string 
        if df[c].dtype == 'object':

            #ponemos todo en minúsculas
            df[c]=df[c].str.lower() 
            df[c]=df[c].apply(lambda x:x.strip() if type(x)!=float else x)

            #creamos una lista de valores a reemplazar por vacío
            lista_simbolos=['!',',',';','-','.',' ?','? ','?',':']
            for elemento in lista_simbolos:
                df[c]=df[c].apply(lambda x:x.replace(elemento ,'')if type(x)!=float else x)                  

            #creamos una lista de valores a reemplazar por espacio
            lista_simbolos=['_','  ']
            for elemento in lista_simbolos:
                df[c] = df[c].apply(lambda x:x.replace(elemento ,' ')if type(x) != float else x)                  

        #sacamos los acentos
        df[c] = df[c].apply(lambda x: normalize( 'NFC', re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", x), 0, re.I))
                                        if type(x)== str and x!= 0 and x!= 'NaN'
                                        else x)

        if c == 'place':
            lista_palabras = [' of ',' sw ',' w ',' n ']
            for elemento in lista_palabras:
                df[c] = df[c].apply(lambda x:x.replace(elemento ,' ')if type(x) != float else x)

            #reemplazamos los '' por 'sin dato'
            df[c] = df[c].apply(lambda x: 'sin dato' if type(x) == str and x == '' else x)

            #sacamos los que no tengan el pais que buscamos
            #df = df[df.place.str.contains('japan|chile')|df.pais.str.contains('usa')] 

            #los eliminamos de place
            #lista_simbolos=['japan','chile']
            #for elemento in lista_simbolos:
                #df[c] = df[c].apply(lambda x:x.replace(elemento ,'') if type(x) != float else x)

        #detectamos NaN
        #df[c] = df[c].apply(lambda x: None if type(x) == str and x == '' else x)  

    return df




def procesarDatos(url):
    '''
    Limpia y trasnforma los datos de la API
    -> DataFrame
    '''
    # Obtenemos los datos
    resp = requests.get(url).json()

    # Guardamos los datos en formato diccionario
    datos = {'mag':[],'place':[],'time':[],'url':[],'tsunami':[],'title':[],'lng':[],'lat':[],'deepth':[]}

    #recorremos la catidad de "filas" que tiene
    cant_reg = len(resp['features'])
    for i in range(cant_reg):
        mag = resp['features'][i]['properties']['mag']
        place = resp['features'][i]['properties']['place']
        time = resp['features'][i]['properties']['time']
        url = resp['features'][i]['properties']['url']
        tsunami = resp['features'][i]['properties']['tsunami']
        title = resp['features'][i]['properties']['title']
        lng = resp['features'][i]['geometry']['coordinates'][0]
        lat = resp['features'][i]['geometry']['coordinates'][1]
        deepth = resp['features'][i]['geometry']['coordinates'][2]
        peligro = 1

        # Vemos que no haya nulos para evitar errores al armar la cadena
        if mag is None:
            mag = 0
        if place is None:
            place = 'Sin dato'
        if time is None:
            time = '1900-01-01 00:00:00.000'
        else:
            time = dt.datetime.fromtimestamp(time//1000).strftime('%Y-%m-%d %H:%M:%S.%f')
            time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
            time = str(time)
            time = time[2 : -2]
        if url is None:
            url = 'Sin dato'
        if tsunami is None:
            tsunami = -1
        if title is None:
            title = 'Sin dato'
        if lng is None:
            lng = 0
        if lat is None:
            lat = 0
        if deepth is None:
            deepth = 0

        # Cargamos el diccionario
        datos['mag'].append(mag)
        datos['place'].append(place)
        datos['time'].append(time)
        datos['url'].append(url)
        datos['tsunami'].append(tsunami)
        datos['title'].append(title)
        datos['lng'].append(lng)
        datos['lat'].append(lat)
        datos['deepth'].append(deepth)

    # Convertimos el diccionario a DataFrame
    df_crudo = pd.DataFrame(datos)

    # Limpiamos los datos
    df_crudo = limpieza_general_tabla(df_crudo)

    # Agregamos la columna idpais y peligro hardcodeada
    df_crudo['idpais'] = usa
    df_crudo['peligro'] = -1

    return df_crudo




def consultarAPIUsa():
    '''
    Consulta la API de USA
    -> DataFrame
    '''
    # Definimos las fechas desde y hasta para la url
    fecha_hasta = dt.datetime.today() - dt.timedelta(days=1)
    fecha_desde = fecha_hasta - dt.timedelta(days=1)
    
    # Formateamos las fechas
    fecha_desde = dt.datetime.strftime(fecha_desde, '%Y-%m-%d')
    fecha_hasta = dt.datetime.strftime(fecha_hasta, '%Y-%m-%d')

    # armamos la url
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={fecha_desde}&endtime={fecha_hasta}&jsonerror=true'

    # Obtenemos el DataFrame ya procesado
    df_procesado = procesarDatos(url)

    return df_procesado




def extraerUsa():
    '''
    Extrae los datos de USA del mes actual
    y nos quedamos con los del día de ayer, si los hay
    '''
    df_ = consultarAPIUsa()

    # Creamos las listas para armar la cadena sql
    idpais = list(df_['idpais'])
    mag = list(df_['mag'])
    place = list(df_['place'])
    time = list(df_['time'])
    url = list(df_['url'])
    tsunami = list(df_['tsunami'])
    title = list(df_['title'])
    lng = list(df_['lng'])
    lat = list(df_['lat'])
    deepth = list(df_['deepth'])
    peligro = list(df_['peligro'])

    # Armamos la cadena
    cadena = list(zip(idpais, mag, place, time, url, tsunami, title, lng, lat, deepth,peligro))
    cadena = str(cadena)
    cadena = cadena[1 : -1]

    if not df_.empty:
        cadena = '''INSERT INTO usa \
                    (idpais, mag, place, time, url, tsunami, title, lng, lat, deepth, peligro) \
                    VALUES''' + cadena + ';'
    else:
        cadena = 'SELECT COUNT(*) FROM pais;'

    return cadena








'''================================ JAPÓN ==========================='''

def get_url(date):
    '''
    Función:Generar la url custom para la fecha y los datos para esa fecha
    Entrada: Toma como ingesta la fecha en formato %YYYY%mm%dd, ej 20221102
    Salida: Devuelve la url para esa fecha y las filas de la tabla obtenida para esa fecha
    '''
    # Agregamos "0" si el número de mes es un solo dígito
    mes = str(date.month)
    if len(mes) == 1:
        mes = '0' + mes

    #url
    url = f'https://www.hinet.bosai.go.jp/AQUA/aqua_catalogue.php?y={date.year}&m={mes}&LANG=en'
    #hacemos la request
    page = requests.get(url)
    #leemos el html
    soup = BeautifulSoup(page.content,"html.parser")
    #Pasamos a filas
    rows1 = soup.find("table", attrs={"class":"base"}).find_all("tr")
    
    return url, rows1




def historicos_japon(url, rows1):
    '''
    Función:
    Entrada: Toma como ingesta la url para una fecha y las filas
    Salida: Devuelve un df con todos los sismos de japón para todo el mes de esa fecha
    '''
    #creo dicc vacio
    datos = {'mag':[],'place':[],'time':[],'url':[],'tsunami':[],'title':[],'lng':[],'lat':[],'deepth':[]}
    for index in range(5,len(rows1) - 1):
        datos['mag'].append(float(rows1[index].find_all("td")[5].get_text()))
        datos['place'].append(rows1[index].find_all("td")[1].get_text())

        time = dt.datetime.strptime(rows1[index].find_all("td")[0].get_text(),'%Y-%m-%d %H:%M:%S')
        time = str(time)
        time = time[2 : -2]
        datos['time'].append(time)

        datos['url'].append(url)
        datos['tsunami'].append(-1)
        datos['title'].append('Sin dato')

        datos['lng'].append(float(rows1[index].find_all("td")[3].get_text()[:-1]))
        datos['lat'].append(float(rows1[index].find_all("td")[2].get_text()[:-1]))
        datos['deepth'].append(float(rows1[index].find_all("td")[4].get_text().split('km')[0]))

    for elemento in datos:
        len(datos[elemento])

    df_japon = pd.DataFrame(datos)

    return df_japon




def carga_historica_japon():
    '''
    Función cargar datos de chile en postgres y hacer csv de backup
    Entrada: Fecha de ingreso en formato date, fecha de fin de la carga en formato date
    Salida: Notificación de finalizada la carga
    '''
    fecha = dt.datetime.today()

    url, rows1 = get_url(fecha)

    df = historicos_japon(url, rows1)

    df = limpieza_general_tabla(df)

    df.insert(loc = 0, column = 'idpais', value = japon)
    df['peligro'] = -1

    return df




def extraerJapon():
    '''
    Extrae los datos de Japón del mes actual
    y nos quedamos con los del día de ayer, si los hay
    '''
    df_ = carga_historica_japon()

    # Eliminamos los que no corresponden al día solicitado, dado que
    # la API de Japón devuelve todo el mes aunque se especifique el día
    hoy = dt.datetime.today() - dt.timedelta(days=2)
    hoy = str(hoy.day)
    df_mask = df_['time'].apply(lambda x: x[4:6] == hoy)
    df_ = df_[df_mask]


    # Creamos las listas para armar la cadena sql
    idpais = list(df_['idpais'])
    mag = list(df_['mag'])
    place = list(df_['place'])
    time = list(df_['time'])
    url = list(df_['url'])
    tsunami = list(df_['tsunami'])
    title = list(df_['title'])
    lng = list(df_['lng'])
    lat = list(df_['lat'])
    deepth = list(df_['deepth'])
    peligro = list(df_['peligro'])

    # Armamos la cadena
    cadena = list(zip(idpais, mag, place, time, url, tsunami, title, lng, lat, deepth,peligro))
    cadena = str(cadena)
    cadena = cadena[1 : -1]

    if not df_.empty:
        cadena = """INSERT INTO japon \
                    (idpais, mag, place, time, url, tsunami, title, lng, lat, deepth, peligro) \
                    VALUES \
                    """ + cadena + ';'
    else:
        cadena = 'SELECT COUNT(*) FROM pais'

    return cadena







'''================================ CHILE ==========================='''

def get_url_chile(dt):
    year = dt.strftime("%Y")
    month = dt.strftime("%m")
    day = dt.strftime('%Y%m%d')

    url = f"https://www.sismologia.cl/sismicidad/catalogo/{year}/{month}/{day}.html"
    urlx = requests.get(url)
    soup = BeautifulSoup(urlx.content,"html.parser")
    if soup is not None:
        rows = soup.find("table", attrs={"class":"sismologia detalle"}).find_all("tr")
        return  url, rows
    else:
        return url, rows




def datos_chile(url, rows):
    #creo dicc vacio
    datos = {'mag':[],'place':[],'time':[],'url':[],'tsunami':[],'title':[],'lng':[],'lat':[],'deepth':[]}
    for index, i in enumerate(rows):
        if index == 0:
            pass
        else:
            datos['mag'].append(float(rows[index].find_all("td")[-1].get_text()[:-3]))
            datos['place'].append(rows[index].find_all("td")[0].get_text()[19:])

            time = dt.datetime.strptime(rows[index].find_all("td")[1].get_text(),'%Y-%m-%d %H:%M:%S')
            time = str(time)
            time = time[2 : -2]
            datos['time'].append(time)


            datos['url'].append(url)
            datos['tsunami'].append(-1)
            datos['title'].append('Sin dato')

            datos['lat'].append(float(rows[index].find_all("td")[2].get_text()[:7]))
            datos['lng'].append(float(rows[index].find_all("td")[2].get_text()[-7:]))
            datos['deepth'].append(float(rows[index].find_all("td")[3].get_text().split()[0]))

    for elemento in datos:
        len(datos[elemento])

    df_chile = pd.DataFrame(datos)

    return df_chile




def carga_historica_chile():
    '''
    Función cargar datos de chile en postgres y hacer csv de backup
    Entrada: Fecha de ingreso en formato date, fecha de fin de la carga en formato date
    Salida: Notificación de finalizada la carga
    '''
    fecha = dt.datetime.today() - dt.timedelta(days=2)

    url, rows = get_url_chile(fecha)    

    df = datos_chile(url, rows)
    df = limpieza_general_tabla(df)
    df.insert(loc = 0, column = 'idpais', value = chile)
    df['peligro'] = -1

    return df




def extraerChile():
    '''
    Extrae los datos de Chile del mes actual
    y nos quedamos con los del día de ayer, si los hay
    '''
    df_ = carga_historica_chile()

    '''Rango de latitud y longitud de Chile utilizados para eliminar puntos erroneos'''
    df_ = df_[(df_['lat'] > -50.0) & (df_['lat'] < -18.0) & (df_['lng'] > -75.0) & (df_['lng'] < -60.0)]


    # Creamos las listas para armar la cadena sql
    idpais = list(df_['idpais'])
    mag = list(df_['mag'])
    place = list(df_['place'])
    time = list(df_['time'])
    url = list(df_['url'])
    tsunami = list(df_['tsunami'])
    title = list(df_['title'])
    lng = list(df_['lng'])
    lat = list(df_['lat'])
    deepth = list(df_['deepth'])
    peligro = list(df_['peligro'])

    # Armamos la cadena
    cadena = list(zip(idpais, mag, place, time, url, tsunami, title, lng, lat, deepth,peligro))
    cadena = str(cadena)
    cadena = cadena[1 : -1]

    if not df_.empty:
        cadena = """INSERT INTO chile \
                    (idpais, mag, place, time, url, tsunami, title, lng, lat, deepth, peligro) \
                    VALUES \
                    """ + cadena + ';'
    else:
        cadena = 'SELECT COUNT(*) FROM pais'



    return cadena








'''================================ DAGs ==========================='''
#Creamos el DAG y vamos relacionando las tareas con las funciones correspondientes
with DAG(dag_id='ETL_Sismos',
         start_date = dt.datetime(2022, 11, 1),
         schedule_interval = '@daily',
         default_args = {'retries': 2,
                         'owner': 'Earth Data'},
         catchup = False
) as dag:

    task_extraer_usa = PythonOperator(
        task_id='extraer_usa',
        python_callable=extraerUsa,
        provide_context=True,
    )

    task_extraer_japon = PythonOperator(
        task_id='extraer_japon',
        python_callable=extraerJapon,
        provide_context=True
    )

    task_extraer_chile = PythonOperator(
        task_id='extraer_chile',
        python_callable=extraerChile,
        #Provide_context habilita que se pase la información obtenida de esta tarea a la siguiente
        provide_context=True
    )

    task_guardar_usa = PostgresOperator(
        task_id='guardar_usa',
        #Nombre que le pusimos a la conexión de airflow con docker o gcp
        postgres_conn_id='sismosdb_id',
        #ti.xcom_pull nos permite pasar contenido entre las tareas
        sql = "{{ti.xcom_pull(task_ids='extraer_usa')}}"
    )

    task_guardar_japon = PostgresOperator(
        task_id='guardar_japon',
        postgres_conn_id='sismosdb_id',
        sql = "{{ti.xcom_pull(task_ids='extraer_japon')}}"
    )

    task_guardar_chile = PostgresOperator(
        task_id='guardar_chile',
        postgres_conn_id='sismosdb_id',
        sql = "{{ti.xcom_pull(task_ids='extraer_chile')}}"
    )

#Ejecutamos las tareas de manera secuencial
task_extraer_usa >> task_guardar_usa >> \
task_extraer_japon >> task_guardar_japon >> \
task_extraer_chile >> task_guardar_chile
