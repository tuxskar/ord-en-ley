'''
Created on Nov 14, 2012

@author: tuxskar
'''

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import shutil

Base = declarative_base()
sqlite_db_name = "leyenorden.db"

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    surname = Column(String(60))
    dni = Column(String(15), unique=True)
    email = Column(String(30))
    web = Column(String(30))
    
    def __init__(self, name="", surname="", 
                 dni="", email="", web=""):
        self.name = name.decode('utf-8')
        self.surname = surname.decode('utf-8')
        self.dni = dni.decode('utf-8')
        self.email = email.decode('utf-8')
        self.web = web.decode('utf-8')

    
    def __repr__(self):
        return "<Client('%s','%s','%s')>" % \
                (self.dni, self.name, self.surname)

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    street = Column(String(60))
    number = Column(Integer)
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    postal_code = Column(Integer)
    

def insert_test(session):
        clients = session.query(Client).all()
        if len(clients) == 0:
            client1 = Client('Maria', 'Ortega', '12345678z', 'maria-ortega@gmail.com', 'www.mariao.org')
            client2 = Client('Josefa', 'Jimenez', '98765454s', 'JJimenez@hotmail.com', 'www.Jjimenez.es')
            client3 = Client('Ana', 'Ramirez', '23456789r', web="www.anaramirez.tk")
            a = [client1,client2,client3]
            session.add_all(a)
            session.commit()
            return True
                
def get_session(user = None, password = None, echo=False, sqlite=True):
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
    insert_test(session)
    

if __name__ == '__main__':
#    Before use this module you should create a user and password plus create a database
#    called leyenorden
#    in mysql database you should loggin into root profile and execute:
#    > mysql -u root -p
#    mysql> create database leyenorden;
#    mysql> grant all on ordenley.* to leyuser@localhost identified by 'pass';
#    engine = create_engine("mysql://leyuser:pass@localhost/ordenley", echo=True)
    self.main()
