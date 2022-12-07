from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, select, literal, or_, and_, desc
from . import models
from . import schemas

'''
Funciones:

- Sismos:

--> #1 Obtener todos los registros de sismos.
--> #2 Obtener los registros de sismos filtrando por características.
--> #3 Obtener el sismos más fuerte para el pais de interesl
--> #4 Definir el pais.''' 

#1
def obtener_sismos(db: Session):
    sismos = db.query(models.Sismos).limit(100).all()
    return sismos

# # Obtener los registros de sismos filtrando por características.
# @app.get('/sismos/',tags=['Sismos'], description='Petición para obtener los registros  de sismos filtrados según sus características.')
# def sismos_filtrados(max_depth: float | None = 800, min_depth: float | None = 0, min_mag: float | None = 0, max_mag: float | None = 9.9,
#          min_lat: float | None = -90, max_lat: float | None = 90, min_long: float | None = -180, max_long:float | None = 180,
#          min_anio: float | None = 2000, max_anio:float | None = 2022,
#          db: Session = Depends(get_db)):
    
#     sismos = db.query(models.Sismos).filter(models.Sismos.deepth >= min_depth).filter(models.Sismos.deepth <= max_depth).\
#             filter(models.Sismos.mag <= max_mag).filter(models.Sismos.mag >= min_mag).\
#                 filter(models.Sismos.lat <= max_lat).filter(models.Sismos.lat >= min_lat).\
#                     filter(models.Sismos.lng <= max_long).filter(models.Sismos.lng >= min_long).\
#                         filter(models.Sismos.year <= max_anio).filter(models.Sismos.year >= min_anio).\
#                             limit(100).all()
#     return sismos


# # sismo mas fuerte para el año deseado en el pais de interes
# @app.get('/sismos/evento_maximo', tags=['Sismos'], description='Petición que retorna el sismo mas fuerte para el año deseado en el pais de interes.')
# def sismo_maximo(pais_i : str,anio: int, db: Session = Depends(get_db)):
#     max_sismo = db.query((models.Sismos),).select_from(models.Sismos).join(models.Pais, models.Sismos.idpais == models.Pais.idpais,).\
#         filter(models.Pais.pais == pais_i).filter(models.Sismos.year == anio).order_by(models.Sismos.mag.desc()).limit(1).all()
#     return max_sismo

#4
def pais(pais):
    if pais.lower() == 'japon'or pais.lower() == 'japan':
        valor = 1
    elif pais.lower() == 'usa':
        valor = 2
    elif pais.lower() == 'chile':
        valor = 3
    return valor