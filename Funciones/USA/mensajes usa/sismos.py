import requests
import pandas as pd
from unicodedata import normalize
import re 
import datetime as dt
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
dic={'usa':1 , 'chile':2,'japon':3}
def procesarDatos(url):
    resp = requests.get(url).json()
    datos = {'mag':[],'place':[],'time':[],'url':[],'tsunami':[],'title':[],'lng':[],'lat':[],'depth':[]}
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
        depth = resp['features'][i]['geometry']['coordinates'][2]
        relleno_cero=['mag','lng','lat','depth']
        for elemento in relleno_cero:
            if elemento is None:
                elemento = 0
        relleno_sin_dato=['place','url','title']
        for elemento in relleno_sin_dato:
            if elemento is None:
                elemento = 'Sin dato'
        if time is None:
            time = dt.datetime(1900,1,1)
        else:
            time = dt.datetime.fromtimestamp(time//1000).strftime('%Y-%m-%d %H:%M:%S')
            time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        if tsunami is None:
            tsunami = -1
        datos['mag'].append(mag)
        datos['place'].append(place)
        datos['time'].append(time)
        datos['url'].append(url)
        datos['tsunami'].append(tsunami)
        datos['title'].append(title)
        datos['lng'].append(lng)
        datos['lat'].append(lat)
        datos['depth'].append(depth)
    df_crudo = pd.DataFrame(datos)
    df_crudo = limpieza_general_tabla(df_crudo)
    df_crudo['idpais'] =dic['usa']    
    df_crudo['peligro'] = -1
    df_crudo['year']=df_crudo.time.apply(lambda x: x.year)
    df_crudo['month']=df_crudo.time.apply(lambda x: x.month)
    df_crudo['day']=df_crudo.time.apply(lambda x: x.day)
    df_crudo.place= df_crudo.place.replace(to_replace=r'ca$', value='canada', regex=True)
    return df_crudo
def consultarAPIUsa():
    fecha_desde= dt.datetime.today() - dt.timedelta(minutes=10)
    fecha_hasta = dt.datetime.today()
    url = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={fecha_desde}&endtime={fecha_hasta}&minlatitude=23.300000&maxlatitude=69.400000&minlongitude=-160.000000&maxlongitude=-69.500000&jsonerror=true'
    df_procesado = procesarDatos(url)
    if not df_procesado.empty:
        df_procesado=df_procesado[df_procesado['mag']>1]
        return(df_procesado)

len(consultarAPIUsa())
