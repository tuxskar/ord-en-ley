'''
Created on Nov 14, 2012

@author: skar
'''

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    surname = Column(String(60))
    dni = Column(String(15), unique=True)
    email = Column(String(30))
    web = Column(String(30))
    
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
                
def get_session(echo=False, user = 'skar', password = 'mypass'):
        engine = create_engine("mysql://"+user+":"+password+"@localhost/leyenorden" , echo=echo)
        Base.metadata.create_all(engine)
        return sessionmaker(engine)()

def _insert_delete_test(session):
    clients = session.query(Client).all()
    print clients
    for c in clients:
        print c
    if len(clients) == 0:
            client1 = Client('maria', 'Ortega', '12345678z', 'maria-ortega@gmail.com', 'www.mariao.org')
            client2 = Client('Josefa', 'Jimenez', '98765454s', 'JJimenez@hotmail.com', 'www.Jjimenez.es')
            client3 = Client('Ana', 'Ramirez', '23456789r', web="www.anaramirez.tk")
            print 'Created client1-3'
            session.add_all([client1,client2,client3])
            session.commit()
            print 'Added all clients'
#    else:
#        session.delete(clients[0])
#        session.commit()
#        print 'deleted clients[0]'

if __name__ == '__main__':
#    Before use this module you should create a user and password plus create a database
#    called leyenorden
#    in mysql database you should loggin into root profile and execute:
#    > mysql -u root -p
#    mysql> create database leyenorden;
#    mysql> grant all on ordenley.* to leyuser@localhost identified by 'pass';
#    engine = create_engine("mysql://leyuser:pass@localhost/ordenley", echo=True)

    session = get_session()
    _insert_delete_test(session)