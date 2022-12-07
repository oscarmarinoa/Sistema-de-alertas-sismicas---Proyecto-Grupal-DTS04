from pydantic import BaseModel 
from datetime import date

# Definen la forma de los datos. Es usado para validar los datos de entrado y de salida de la API

# Con este creamos los modelos bases de pydantyc "como van a lucir nuestros datos". 

class SismosBase(BaseModel):
    
    idpais : int
    mag : float
    place : str
    time : str
    url : str
    tsunami : str
    title :  str
    lng : float
    lat : float
    deepth : float
    peligro : int
    
class Sismos(SismosBase):
    idsismo : int
    
    class Config:
        orm_mode = True

class Intento(BaseModel):
    
    idintento : int
    mag : float
    deepth : float
    peligro : str
    
class TsunamisBase(BaseModel):
    
    idpais : int
    altura_oleaje : float
    place : str
    time : str
    url : str
    mag : float
    lng : float
    lat : float
    deepth : float

class Tsunami(TsunamisBase):
    
    idtsunami : int
    
    class Config:
        orm_model = True

class VolcanesBase(BaseModel):
    
    idpais : int
    nombre : str
    tipo : str
    elevacion : float
    place : str
    ultima_erupcion : str
    lat : float
    lng : float
    url : float
    
class Volcanes(VolcanesBase):
    
    idvolcanes : int
    
    class Config:
        orm_model = True

class PaisBase(BaseModel):
    
    pais : str

class Pais(PaisBase):
    
    idpais : int
    
    class Config:
        orm_model = True