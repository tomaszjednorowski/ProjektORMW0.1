from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, ForeignKey, DefaultClause
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Zwierze(Base):
    __tablename__ = 'Zwierze'
    
    id = Column(Integer, primary_key= True)
    imie  = Column(String(25))
    masa = Column(Numeric(precision=5,scale=2))
    plec = Column(String(25)) #Zmienić też w DB
    typRasy = Column(String(25))
    opis = Column(String(250))
    statusZwierzecia = Column(String(25))
    dataPrzyjecia = Column(DateTime)
    dataWydania = Column(DateTime)
    numerChip = Column(Integer)
    wiek = Column(Integer)
    boks = Column(String(20))

    
    
class Kandydat(Base):
    __tablename__ = 'Kandydat'
    
    id = Column(Integer, primary_key= True)
    imiona = Column(String(25))
    nazwisko = Column(String(25))
    numerPESEL = Column(String(25))
    telefon1 = Column(String(25))
    telefon2 = Column(String(25))
    mail = Column(String(25))
     
    
class Ocena(Base):
    __tablename__ = 'Ocena'
    
    id = Column(Integer, primary_key= True)
    wolontariuszProwadzacy = Column(String(25))
    ocenaRozmowy = Column(String(25))
    ocenaAnkiety = Column(String)
    ocenaSpotkan = Column(String)
    ocenaKoncowa = Column(String)

class ProcesAdopcj(Base):
    __tablename__ = 'ProcesAdopcji'
    
    id = Column(Integer, primary_key= True)
    statusAdopcji = Column(Integer)
    idKandydat = Column(Integer)
    idZwierze = Column(Integer)
    idOcena = Column(Integer)
  
