import requests
import pandas as pd
from unicodedata import normalize
import re 
import datetime as dt
#Web Scraping
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

#Web scraping
#Permiso de la web
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
#desactivamos los request
disable_warnings(InsecureRequestWarning)

def limpieza_general_tabla(df):
    df.drop_duplicates(inplace=True) 
    df.reset_index(drop=True, inplace=True)
    for c in df.columns:         
        if df[c].dtype == 'object':
            df[c]=df[c].str.lower() 
            #df[c]=df[c].apply(lambda x:x.strip() if type(x)!=float else x)              
        df[c] = df[c].apply(lambda x: normalize( 'NFC', re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", x), 0, re.I))
                                        if type(x)== str and x!= 0 and x!= 'NaN'
                                        else x)
        df[c] = df[c].apply(lambda x: 'sin dato' if type(x) == str and x == '' else x)
        df = df[df['mag'] != 0]
        df = df[df['depth'] != 0]
    return df  
  
chile = 2

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
    datos = {'mag':[],'place':[],'time':[],'url':[],'tsunami':[],'title':[],'lng':[],'lat':[],'depth':[]}
    for index, i in enumerate(rows):
        if index == 0:
            pass
        else:
            datos['mag'].append(float(rows[index].find_all("td")[-1].get_text()[:-3]))
            datos['place'].append(rows[index].find_all("td")[0].get_text()[19:])

            datos['time'].append(dt.datetime.strptime(rows[index].find_all("td")[1].get_text(),'%Y-%m-%d %H:%M:%S'))

            datos['url'].append(url)
            datos['tsunami'].append(-1)
            datos['title'].append('Sin dato')

            datos['lat'].append(float(rows[index].find_all("td")[2].get_text()[:7]))
            datos['lng'].append(float(rows[index].find_all("td")[2].get_text()[-7:]))
            datos['depth'].append(float(rows[index].find_all("td")[3].get_text().split()[0]))

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
    df['year']=df.time.apply(lambda x: x.year)
    df['month']=df.time.apply(lambda x: x.month)
    df['day']=df.time.apply(lambda x: x.day)

    return df

def extraerChile():
    '''
    Extrae los datos de Chile del mes actual
    y nos quedamos con los del día de ayer, si los hay
    '''
    df_ = carga_historica_chile()

    '''Rango de latitud y longitud de Chile utilizados para eliminar puntos erroneos'''
    df_ = df_[(df_['lat'] > -50.0) & (df_['lat'] < -18.0) & (df_['lng'] > -75.0) & (df_['lng'] < -60.0)]
    return df_



