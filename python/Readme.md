## Repositorios:
* scripts_datasets.ipynb : Contiene el código necesario para obtener los datos de las diferentes fuentes de información, la creación de una base de datos local en Postgres y la ingesta de la misma.

# Fuentes de información:
## USGS 
Corresponde con el Servicio Geológico de Estados Unidos. Se utilizó esta API para recolectar información relacionada con eventos sísmicos y de tsunamis para los paises de interés.
* [Documentación API USGS](https://earthquake.usgs.gov/fdsnws/event/1/)
* [Diccionario API USGS](https://earthquake.usgs.gov/data/comcat/index.php#tsunami)
* [Rango de fechas/formatos disponibles por catálogo](https://earthquake.usgs.gov/data/comcat/catalog/us/)
* [FDSN	Web	Service	Specifications](http://www.fdsn.org/webservices/FDSN-WS-Specifications-1.0.pdf)

## JAPON
#### Fuente:
https://www.jma.go.jp/jma/index.html
#### Place APIS:
https://www.p2pquake.net/
#### Documentación de API JSON:
https://www.p2pquake.net/json_api_v2/
#### Ejemplo de archivo JSON:
![Ejemplo JSON](https://user-images.githubusercontent.com/104787036/203128755-af6ed777-dfcd-4df5-bc67-ba593bfa9443.JPG)

## NOAA
Como fuente de información adicional se utilizaron los datos obtenidos de la API de la Oficina Nacional de Administración Oceánica y Atmosférica (NOAA). De esta se extraen datos referentes a sismos de los 3 paises, tsunamis y localización de volcanes.
* [Documentación API NOAA](https://www.ngdc.noaa.gov/hazel/view/swagger#/)
* [Diccionario API NOAA](https://www.ngdc.noaa.gov/hazel/view/about)

# Diccionario de datos:
Explicación detallada del contenido de los datos y su formato.

#### Tabla Sismos: 
  | **Característica** | **Descripción** | **Medida** | **Formato** |
  | --- | --- | --- | --- |
  | idpais | Código único que identifica el país en el cual se originó el sismo. | N/A | int |
  | mag | Magnitud del sismo sucedido. | Medida en escala de magnitud de Richter* | float |
  | time | Fecha del evento sísmico. <sub>Incluye horas, minutos y segundos.</sub> | N/A | datetime |
  | url | Url del sitio web donde se encuentra información detallada del sismo. | N/A | str |
  | tsunami | Booleano que indica si ocurrió o no un tsunami asociado al sismo: <sub>1 = Si, 0 = No.</sub> | N/A | int |
  | title | Descripción detallada del evento sísmico. | N/A | str |
  | lng | Coordenada geográfica Este del evento sísmico. <sub>(Longitud)</sub> | Grados decimales | float |
  | lat | Coordenada geográfica Norte del evento sísmico. <sub>(Latitud)</sub> | Grados decimales | float |
  | deepth | Profundidad a la cual se originó el sismo <sub>(Hipocentro).</sub> | Kilómetros | int |
 
 * <sub>N/A: No aplica</sub>
 * <sub>[Escala de Richter USGS](https://www.usgs.gov/faqs/moment-magnitude-richter-scale-what-are-different-magnitude-scales-and-why-are-there-so-many)
 
 #### Tabla Tsunamis:
  | **Característica** | **Descripción** | **Medida** | **Formato** |
  | --- | --- | --- | --- |
  | idpais | Código único que identifica el país en el cual se localiza el volcán. | N/A | int |
  | nombre | Magnitud del sismo sucedido. | Medida en escala de magnitud de Richter* | float |
  | time | Fecha del evento sísmico. <sub>Incluye horas, minutos y segundos.</sub> | N/A | datetime |
  | url | Url del sitio web donde se encuentra información detallada del sismo. | N/A | str |
  | tsunami | Booleano que indica si ocurrió o no un tsunami asociado al sismo: <sub>1 = Si, 0 = No.</sub> | N/A | int |
  | title | Descripción detallada del evento sísmico. | N/A | str |
  | lng | Coordenada geográfica Este del evento sísmico. <sub>(Longitud)</sub> | Grados decimales | float |
  | lat | Coordenada geográfica Norte del evento sísmico. <sub>(Latitud)</sub> | Grados decimales | float |
  | deepth | Profundidad a la cual se originó el sismo <sub>(Hipocentro).</sub> | Kilómetros | int |
 
 #### Tabla Volcanes:
  | **Característica** | **Descripción** | **Medida** | **Formato** |
  | --- | --- | --- | --- |
  | idpais | Código único que identifica el país en el cual se localiza el volcán. | N/A | int |
  | nombre | Nombre del volcán. | N/A | str |
  | tipo | Tipo de volcán. | N/A | str |
  | elevacion | Elevacion del volcán. | m.s.n.m. | int |
  | place | Descripción detallada del volcán. | N/A | str |
  | lat | Coordenada geográfica Norte del volcán. <sub>(Latitud)</sub> | Grados decimales | float |
  | lng | Coordenada geográfica Este del volcán. <sub>(Longitud)</sub> | Grados decimales | float |
  | url | Url del sitio web donde se encuentra información detallada del volcán. | N/A | str |
