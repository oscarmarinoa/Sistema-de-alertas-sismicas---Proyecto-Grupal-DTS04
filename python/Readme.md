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
  
## Web Scraping 

1. Sitio usado como herramienta de Web Scraping :

  A. https://www.sismologia.cl -- DATOS DE CHILE.
  
  B. https://www.hinet.bosai.go.jp -- DATOS DE JAPÓN.
  
Como Fuente Para estudio(Henry) de Proyecto Grupal (Sismo).

2. Sitio Web: Inspeccione de elemento, mediante opciones de navegación del mismo navegador.

3. Inspeccionar el body de la web y Buscar la etiqueta table. Si se cumple lo Siguiente. Se puede pasar al Siguiente paso.

4. Para conectar se usaron 2 librerías:

 	A. Requests
  
	B. BeautifulSoup

5. Generar la Requests del sitio web (Conexión).

6. Genero con BeautifulSoup(html) para poder ver lo que contiene el sitio web o de la pagina.

7. Filtro la Etiqueta Tabla del la Vista Generada por BeautifulSoup.

8. Genero Contenedores Para Cada columna.

9. Programar tipo de parámetro para extrae la información y albergarla según su columna .
