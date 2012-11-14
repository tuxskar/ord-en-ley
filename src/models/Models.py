'''
Created on Nov 14, 2012

@author: skar
'''

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    def __init__(self):    
        pass
    
    def __repr__(self):
        pass

if __name__ == '__main__':
    pass