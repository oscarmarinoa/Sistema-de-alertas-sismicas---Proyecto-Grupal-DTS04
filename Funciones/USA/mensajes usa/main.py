
from sismos import consultarAPIUsa
import pywhatkit
from datetime import datetime as dt
id_grupo='I0bdo1JQv7H6NZMS0oolQV'


def main(request):

    try:
        # Request dolar data
        sismo_data = consultarAPIUsa()

        # Check is the created dataframe is not empty
        if sismo_data  is None or len(sismo_data ) == 0:
            print('No content, table has 0 rows')
            return ('No content, table has 0 rows', 204)

        # Save on Google Big Query
        print("sending what....")

        for elemento in range (0, len(sismo_data)):
            lugar=sismo_data['place'][elemento]
            magnitud=lugar=sismo_data['mag'][elemento]
            web='poner streamlite'
            fecha= dt.today()
            
            
            mensaje=f'Ha ocurrido un sismo en los últimos diez minutos en {lugar} de {magnitud} para más información ingresa a nuestra web'
            pywhatkit.sendwhatmsg_to_group_instantly(id_grupo,mensaje,fecha.minute,fecha.second)

    except Exception as e:
        error_message = "Error uploading data: {}".format(e)
        print('[ERROR] ' + error_message)
        return (error_message, '400')