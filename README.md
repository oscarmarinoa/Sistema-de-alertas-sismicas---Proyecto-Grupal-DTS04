# Estandarización de información de redes sismológicas y comunicación efectiva a la comunidad.

## Proyecto-Grupal-DTS04
### Integrantes: 
* Federico Goyechea [Github](https://github.com/Workitaws) [LinkedIn](https://www.linkedin.com/in/federico-goyechea-65361b24a/)
* Gisela Sánchez [Github](https://github.com/sgisela945) [LinkedIn](https://www.linkedin.com/in/gisela-s%C3%A1nchez-272b9017a)
* Lala Weber [Github](https://github.com/LalaYupii)
* Oscar Mariño [Github](https://github.com/oscarmarinoa) [LinkedIn](https://www.linkedin.com/in/oscar-mariño-arias-774098112/)



![Intro](https://user-images.githubusercontent.com/104787036/202545063-d46a6706-e880-448d-a1be-906b4e7c3996.jpg)


## **Contexto**

Los desastres naturales pueden resultar en un gran número de muertes, pérdida de propiedades, y daños irreparables. Es por esto que la predicción temprana y medidas de protección y atención apropiadas resultan urgentes.

Particularmente, los sismos, son el fenómeno natural del cual tenemos menor capacidad predictiva. Sin embargo, son el desastre natural que genera mayor cantidad de victimas mortales y perdidas monetarias.

## **Objetivos**

* Crear una base de datos que contemple la información de sismos para los países de interés.
* Informar a la comunidad de que acciones tomar a la hora de la ocurrencia de un sismo.
* Permitir la obtención información de calidad y actualizada con relación a sismos, tsunamis y volcanes.


## **Procedimiento**

## **Sobre el repositorio**

* En este encontraras la estructura de carpetas y archivos para la ejecución del proyecto, además de documentación adicional complementaria para cada una de las dependencias:

* API/: Estructura de carpetas y documentos para la creación de una API utilizando el framework FASTAPI.
* Airflow/: Archivos para la automatización de procesos de ETL.
* Diccionario de datos: Explicación detallada de la información que se encuentran en la base de datos y que es retornada mediate peticiones a la API de EARTH DATA.
* Scritps/: Scritps con el código para el proceso de ETL de los datos obtenidos. Adicionalmente contiene información relevante de las fuentes de información utilizadas.
* Streamlit/: Estructura de carpetas y documentos para la ejecución de una pagina web usando el framework Streamlit.

## Fuentes de información
 
* USGS: United States Geological Service
* NOAA: National Oceanic and Atmospheric Administration
* CSN: Centro Sismológico Nacional - Universidad de Chile
* JMA: Japan Meteorological Agency https://www.jma.go.jp/jma/index.html
* NIED: National Research Institute for Earth Science and Disaster Resilience https://www.hinet.bosai.go.jp
* P2PQuake

## ¿Como lo hacemos?  

### Enfoque 1 [Data Analysis focus]

Analizando profundamente la relacion de los sismos con otra u otras particularidades de su pais latinoamericano escogido.

Ejemplos de lineas de investigacion (Solo para que se inspiren. Pueden divagar y escoger lo que se les ocurra, su mente es el limite!):

- Sismicidad secundaria (después de un gran sismo) ¿cómo afecta? ¿Qué ha pasado? Se pueden anticipar medidas si es que hay algo sistemáticamente mal?
- Es aconsejable que haya una reubicación de habitantes en zonas como CDMX que es sabido esta construida en una zona geológicamente inestable y con alta actividad sísmica?
- Derribando (o acentuando) mitos: Tiene que ver el clima con la propensión a sismos de mayor “magnitud” y los cambios estacionales?
- Efectos secundarios no deseables: Sismos y Tsunamis, Problemas en redes eléctricas, incendios…


Entregables tangibles minimos:
Mapa de geolocalizacion de los sismos escogidos que contemple la actualizacion cada hora. 
La informacion que debe tener DEBE ser la escogida en su analisis. NO debe ir informacion cientifica como: Magnitud, Profundidad si esta no esta explicada o se indica por que es relevante.


### Enfoque 2 [Machine Learning Focus]

Aplicar un modelo de clasificacion no supervisada. 
La idea aqui NO sera predecir un sismo, sino, dadas las caracteristicas que tienen los sismos, clasificarlos segun patrones como Peligrosidad Media/Alta/Baja
o cualquier enfoque que quieran aplicar. 

Entregables tangibles minimos:
Presentacion de las etiquetas de clasificacion y performancia del modelo.  
Deploy del modelo de ML - puesta en produccion (plataforma a elección)

## **Datasets y fuentes complementarias**

Fuentes de datos obligatorias:
+ Estados Unidos https://earthquake.usgs.gov/fdsnws/event/1/
+ Japon https://www.fdsn.org/networks/detail/JP/
+ Observatorio Latinoamericano de su preferencia ***********

Nota: El producto final debe tener en su etapa de *extraccion* los datos en formato JSON o GeoJSON. Formatos de texto como CSV podrian usarse en los pasos intermedios para hacer sus test respectivos de ser necesario, pero no seran admitidos en la entrega final.

## **Planificación, seguimiento de actividades y tareas de cada integrante:**
### Tareas Sprint 01:
[Grupo 01 Datascience 01 JIRA](https://grupo01datascience.atlassian.net/jira/software/projects/PGS/boards/1)
### Tareas Sprint 02:
Presentación: 
https://www.canva.com/design/DAFS6iNq4-A/e2zEpPwc_PynegS6OCsBQA/view?utm_content=DAFS6iNq4-A&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink
[Grupo 01 Datascience 01 JIRA](https://grupo01datascience.atlassian.net/jira/software/projects/PGS/boards/2)
### Tareas Sprint 03:
[Grupo 01 Datascience 01 JIRA](https://grupo01datascience.atlassian.net/jira/software/projects/PGS/boards/3)

![Henry DTS-04](https://github.com/oscarmarinoa/Sistema-de-alertas-sismicas---Proyecto-Grupal-DTS04/blob/main/Henry%20Logo.png)
