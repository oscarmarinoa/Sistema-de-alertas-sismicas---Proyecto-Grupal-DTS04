# Fuentes de información:
## USGS 
Corresponde con el Servicio Geológico de Estados Unidos. Se utilizó esta API para recolectar información relacionada con eventos sísmicos y de tsunamis para los paises de interés.
* [Documentación API USGS](https://earthquake.usgs.gov/fdsnws/event/1/)
* [Diccionario API USGS](https://earthquake.usgs.gov/data/comcat/index.php#tsunami)
* [Rango de fechas/formatos disponibles por catálogo](https://earthquake.usgs.gov/data/comcat/catalog/us/)
* [FDSN	Web Service Specifications](http://www.fdsn.org/webservices/FDSN-WS-Specifications-1.0.pdf)

## JMA
Agencia meteoreológica de Japón. Se obtuvó datos de los sismos registrados en Japón mediante la API de esta agencia
* [Página principal](https://www.jma.go.jp/jma/index.html)
* [Visualizador de sismos](https://www.jma.go.jp/bosai/map.html#10/37.318/137.571/&elem=int&contents=earthquake_map&lang=en)

## P2PQuake
Aplicación que dispone de una API para obtener sismos en Japón. 
* [Página principal](https://www.p2pquake.net/)
* [Documentación API P2PQuake](https://earthquake.usgs.gov/fdsnws/event/1/)
![Ejemplo JSON](https://user-images.githubusercontent.com/104787036/203128755-af6ed777-dfcd-4df5-bc67-ba593bfa9443.JPG)

## NOAA
Como fuente de información adicional se utilizaron los datos obtenidos de la API de la Oficina Nacional de Administración Oceánica y Atmosférica (NOAA). De esta se extraen datos referentes a sismos de los 3 paises, tsunamis y localización de volcanes.
* [Documentación API NOAA](https://www.ngdc.noaa.gov/hazel/view/swagger#/)
* [Diccionario API NOAA](https://www.ngdc.noaa.gov/hazel/view/about)
  
## CSN
Centro Sismológico Nacional de la Universidad de Chile. Corresponde a una interfaz web donde se registran los eventos sísmicos mpas recientes de Chile.
* [Página principal](https://www.sismologia.cl)

## NIED
Interfaz web de el Instituto Nacional de Investigacición de Ciencias de la Tierra y Resilencia ante Desastres. Disponibiliza información acerca de eventos sísmicos en Japón.
* [Página principal](https://www.hinet.bosai.go.jp)

La obtención de información para las ultimas dos fuentes fue realizada mediante Web Scrapping. Esto se llevo acabo de la siguiente manera:
1.Inspección de los elementos de la página webor.
2. Conexión con librerias Requests y BeautifulSoup.
3. Generar request y obtención de respuesta.
4. Generación de contenedores para los datos de interes y extracción de los mismos.

## Librerías Python:
 * Ver archivo requirements.txt (url :https://pypi.org/search/?q=pywin32)
