# -*- coding: utf-8 -*-
'''
Created on Nov 14, 2012

@author: tuxskar
'''

from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
import shutil

Base = declarative_base()
sqlite_db_name = "leyenorden.db"

class Client(Base):
    __tablename__ = 'clients'
    
    id      = Column(Integer, primary_key = True)
    name    = Column(String(30))
    surname = Column(String(60))
    dni     = Column(String(15), unique=True, nullable=True)
    email   = Column(String(30))
    web     = Column(String(30))
    address = relationship("Address",
                            secondary = lambda: assoc_client_address,
                            backref   = "clients",
                            cascade   = "all, delete")
    
    def __init__(self, name="", surname="", 
                 dni=None, email="", web="", id=None):
        self.id = id
        self.name    = name.decode('utf-8')
        self.surname = surname.decode('utf-8')
        if self.dni != None:
            self.dni     = dni.decode('utf-8')
        self.email   = email.decode('utf-8')
        self.web     = web.decode('utf-8')

    
    def __repr__(self):
        return "<Client('%s','%s','%s')>" % \
                (self.dni, self.name, self.surname)

class Address(Base):
    __tablename__ = 'address'

    id          = Column(Integer, primary_key = True)
    street      = Column(String(60), nullable = False)
    #number      = Column(Integer)
    number      = Column(String(30))
    city        = Column(String(50))
    state       = Column(String(50))
    country     = Column(String(50))
    #postal_code = Column(Integer)
    postal_code = Column(String(30))
        
    def __init__(self, street, number=None, city=None, state=None,
            country=None, postal_code=None, id = None):
        """Class constructor"""
        self.street      = _decode_or_none(street)
        #self.number      = number
        self.number      = _decode_or_none(number)
        self.city        = _decode_or_none(city)
        self.state       = _decode_or_none(state)
        self.country     = _decode_or_none(country)
        #self.postal_code = postal_code
        self.postal_code = _decode_or_none(postal_code)
        self.id = id

    def __repr__(self):
        return "<Address('%s','%s','%s', '%s')>" % \
                (self.street, self.number, self.city, self.state)

def _decode_or_none(str):
    """Function to decode a string or return None"""
    if str is not None:
        return str.decode('utf-8').lower().strip()
    return ""

assoc_client_address = Table('client_address',Base.metadata,
           Column('client_id', Integer, ForeignKey('clients.id')),
           Column('address_id', Integer, ForeignKey('address.id'))
)

def insert_test(session, debug=False):
    """
        Method to insert dummy data in a empty database
    """
    clients = session.query(Client).all()
    if len(clients) == 0 or debug:
        # Delete already DB for debug 
        if debug:
            for c in clients:
                session.delete(c)
        # Inserting clients
        client1 = Client('Maria', 'Ortega', '12345678z', 'maria-ortega@gmail.com', 'www.mariao.org')
        client2 = Client('Josefa', 'Jimenez', '98765454s', 'JJimenez@hotmail.com', 'www.Jjimenez.es')
        client3 = Client('Ana', 'Ramirez', '23456789r', web="www.anaramirez.tk")
        # Address
        address1 = Address("Alhama","84","Lucena", "Cordoba","España","14900")
        address2 = Address("Arroyo","56","Rute", "Cordoba","España","14978")
        address3 = Address("Almendros","1290" ,"Málaga", "Málaga","España","30264")
        address4 = Address("Naranjos","12" ,"Madrid", "Madrid","España","76602")
        address5 = Address("Pinos","90" ,"Granada", "Madrid","España","62764")

        # Joining both classes
        client1.address.append(address1)
        client1.address.append(address2)
        client2.address.append(address1)
        client2.address.append(address4)
        client2.address.append(address5)
        client3.address.append(address3)
        client3.address.append(address5)
        a = [client1,client2,client3]
        session.add_all(a)
        session.commit()
        return True
                
def get_session(user = None, password = None, echo=False, sqlite=True):
    """
        Method to get a new session
    """
    if sqlite:
        ordenpath = os.path.expanduser('~/.ordenley')
        if not os.path.exists(ordenpath):
            os.makedirs(ordenpath)
        engine = create_engine("sqlite:///%s/%s" % (ordenpath, sqlite_db_name), echo=echo)
    else:
        engine = create_engine("mysql://"+user+":"+password+"@localhost/leyenorden" , echo=echo)
    Base.metadata.create_all(engine)
    return sessionmaker(engine)()


def delete_first_test(session):
    client = session.query(Client).first()
    session.delete(client)
    session.commit()
    return True

def delete_sqlite_db(session):
    """Delete db from software"""
    db_path = os.path.expanduser('~/.ordenley/')
    shutil.rmtree(db_path)

def main():
    """main function to test this module"""
    session = get_session()
    #insert_test(session)
    insert_test(session, True)
    

if __name__ == '__main__':
     main()
