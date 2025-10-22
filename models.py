from sqlalchemy import Column, Integer, String, Date
from database import Base

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Edital(Base):
    __tablename__ = "editais"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    orgao = Column(String)
    uf = Column(String)
    modalidade = Column(String)
    data_publicacao = Column(Date)
    link = Column(String)

