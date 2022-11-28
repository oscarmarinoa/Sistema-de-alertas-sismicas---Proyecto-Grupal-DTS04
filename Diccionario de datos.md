# Diccionario de datos:
Explicación detallada del contenido de los datos y su formato. INtento OSCAR

#### Tabla Sismos: 
  | **Característica** | **Descripción** | **Medida** | **Formato** |
  | --- | --- | --- | --- |
  | idpais | Código único que identifica el país en el cual se originó el sismo. | N/A | int |
  | mag | Magnitud del sismo sucedido. | Medida en escala de magnitud de Richter* | float |
  | time | Fecha del evento sísmico. <sub>Incluye horas, minutos y segundos.</sub> | N/A | datetime |
  | url | Url del sitio web donde se encuentra información detallada del sismo. | N/A | str |
  | tsunami | Valor que indica si ocurrió un tsunami: <sub>-1 = Sin Datos 0 = No</sub> <sub>1 = Si | N/A | smallint |
  | title | Descripción detallada del evento sísmico. | N/A | str |
  | lng | Coordenada geográfica Este del evento sísmico. <sub>(Longitud)</sub> | Grados decimales | float |
  | lat | Coordenada geográfica Norte del evento sísmico. <sub>(Latitud)</sub> | Grados decimales | float |
  | deepth | Profundidad a la cual se originó el sismo <sub>(Hipocentro).</sub> | Kilómetros | int |
  | peligro | Resultado de la preddicción del modelo. |  N/A  | smallint |
 
 * <sub>N/A: No aplica</sub>
 * <sub>[Escala de Richter USGS](https://www.usgs.gov/faqs/moment-magnitude-richter-scale-what-are-different-magnitude-scales-and-why-are-there-so-many)
 
 #### Tabla Tsunamis:
  | **Característica** | **Descripción** | **Medida** | **Formato** |
  | --- | --- | --- | --- |
  | idpais | Código único que identifica el país en el cual se localiza el volcán. | N/A | int |
  | altura_oleaje | Altura de las olas producidas por el evento natural. | m.s.n.m | float |
  | place | Descripción detallada del volcán. | N/A | str |
  | time | Fecha del fenomeno natural. <sub>Incluye horas, minutos y segundos.</sub> | N/A | datetime |
  | url | Url del sitio web donde se encuentra información detallada del sismo. | N/A | str |
  | mag | Magnitud del evento sísmico que ocasiono el tsunami. | Medida en escala de magnitud de Richter | float |
  | lng | Coordenada geográfica Este del evento sísmico. <sub>(Longitud)</sub> | Grados decimales | float |
  | lat | Coordenada geográfica Norte del evento sísmico. <sub>(Latitud)</sub> | Grados decimales | float |
  | deepth | Profundidad a la cual se originó el sismo que ocasionó el tsunami <sub>(Hipocentro).</sub> | Kilómetros | int |
  
 * <sub>m.s.n.m: Metros sobre el nivel del mar</sub>
 
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
