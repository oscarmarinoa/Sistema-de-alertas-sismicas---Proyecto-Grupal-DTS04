from sqlalchemy import Column, Integer, String, Float,Date, DateTime, Text, ForeignKey
from .database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
 
# Un modelo en SQLAlchemy se refiere a las clases e instancias que interactuan con la database. Representan las tablas en nuestra base de datos.
 
# Creamos los atributos de los modelos. Estos atributos representan las columnas en las tablas de la database.

# Atributos de un modelo --> Columnas de una tabla
    
# Clase sismos Database NUBE
class Sismos(Base):
    
    __tablename__ = 'sismos'
    
    idsismo = Column(Integer, primary_key=True, index = True)
    idpais = Column(Integer, ForeignKey('pais.idpais'))
    mag = Column(Float)
    place = Column(Text)
    time = Column(Text)
    url = Column(Text)
    tsunami = Column(Integer)
    title =  Column(Text)
    lng = Column(Float)
    lat = Column(Float)
    depth = Column(Float)
    peligro = Column(Integer)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    
    pais_r = relationship('Pais', back_populates = 'sismos_r')
    
class Tsunamis(Base):
    
    __tablename__ = 'tsunamis'
    
    id = Column(Integer, primary_key=True, index = True) # No se le pone idvolcanes
    idpais = Column(Integer, ForeignKey('pais.idpais'))
    altura_oleaje = Column(Float)
    place = Column(Text)
    time = Column(Text)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    url = Column(Text)
    mag = Column(Float)
    lng = Column(Float)
    lat = Column(Float)
    depth = Column(Float)

    pais_r2 = relationship('Pais', back_populates = 'tsunamis_r')
    
class Volcanes(Base):
    
    __tablename__ = 'volcanes'
    
    id = Column(Integer, primary_key=True, index = True) # No se le pone idvolcanes
    idpais = Column(Integer, ForeignKey('pais.idpais'))
    nombre = Column(String)
    tipo = Column(String)
    elevacion = Column(Float)
    place = Column(Text)
    ultima_erupcion = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    url = Column(Text)
    
    pais_r3 = relationship('Pais', back_populates = 'volcanes_r')
    

class Pais(Base):
    
    __tablename__ = 'pais'
    
    idpais = Column(Integer, primary_key=True, index = True)
    pais = Column(Text)
    
    sismos_r = relationship('Sismos', back_populates = 'pais_r')
    tsunamis_r = relationship('Tsunamis', back_populates = 'pais_r2')
    volcanes_r = relationship('Volcanes', back_populates = 'pais_r3')
