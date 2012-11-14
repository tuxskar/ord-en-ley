'''
Created on Nov 14, 2012

@author: skar
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    dni = Column(String, unique=True)
    email = Column(String)
    web = Column(String)
    
    def __init__(self, name=None, surname=None, 
                 dni=None, email=None, web=None):
        self.name = name
        self.surname = surname
        self.dni = dni
        self.email = email
        self.web = web

    
    def __repr__(self):
        return "<Client('%s','%s','%s')>" % \
                (self.dni, self.name, self.surname)

if __name__ == '__main__':
    pass