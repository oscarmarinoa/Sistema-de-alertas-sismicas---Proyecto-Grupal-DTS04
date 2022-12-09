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
  
japon = 3

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
    datos = {'mag':[],'place':[],'time':[],'url':[],'tsunami':[],'title':[],'lng':[],'lat':[],'depth':[]}
    for index in range(5,len(rows1) - 1):
        datos['mag'].append(float(rows1[index].find_all("td")[5].get_text()))
        datos['place'].append(rows1[index].find_all("td")[1].get_text())

        time = dt.datetime.strptime(rows1[index].find_all("td")[0].get_text(),'%Y-%m-%d %H:%M:%S')
        datos['time'].append(time)

        datos['url'].append(url)
        datos['tsunami'].append(-1)
        datos['title'].append('Sin dato')

        datos['lng'].append(float(rows1[index].find_all("td")[3].get_text()[:-1]))
        datos['lat'].append(float(rows1[index].find_all("td")[2].get_text()[:-1]))
        datos['depth'].append(float(rows1[index].find_all("td")[4].get_text().split('km')[0]))

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
    df['year']=df.time.apply(lambda x: x.year)
    df['month']=df.time.apply(lambda x: x.month)
    df['day']=df.time.apply(lambda x: x.day)

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
    df_mask = df_['time'].apply(lambda x: x.day == hoy)
    df_ = df_[df_mask]
    return df_
