'''
Created on Nov 14, 2012

@author: tuxskar
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
def insert_test(session):
        clients = session.query(Client).all()
        if len(clients) == 0:
            client1 = Client('Maria', 'Ortega', '12345678z', 'maria-ortega@gmail.com', 'www.mariao.org')
            client2 = Client('Josefa', 'Jimenez', '98765454s', 'JJimenez@hotmail.com', 'www.Jjimenez.es')
            client3 = Client('Ana', 'Ramirez', '23456789r', web="www.anaramirez.tk")
            a = [client1,client2,client3]
            session.add_all(a)
            session.commit()
            print 'Inserted 3 test clients'
                
def get_session(user = None, password = None, echo=False, sqlite=True):
    if sqlite:
        engine = create_engine("sqlite:///leyenorden.db" , echo=echo)
    else:
        engine = create_engine("mysql://"+user+":"+password+"@localhost/leyenorden" , echo=echo)
    Base.metadata.create_all(engine)
    return sessionmaker(engine)()


def delete_first_test(session):
    client = session.query(Client).one()
    session.delete(client)
    session.commit()
    print 'deleted' + str(client)

if __name__ == '__main__':
#    Before use this module you should create a user and password plus create a database
#    called leyenorden
#    in mysql database you should loggin into root profile and execute:
#    > mysql -u root -p
#    mysql> create database leyenorden;
#    mysql> grant all on ordenley.* to leyuser@localhost identified by 'pass';
#    engine = create_engine("mysql://leyuser:pass@localhost/ordenley", echo=True)
    session = get_session()
    insert_test(session)
