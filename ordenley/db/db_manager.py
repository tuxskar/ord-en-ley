# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2012

@author: tuxskar
'''
from models import Models

class db_manager(object):
    '''
    This module is the layer between physical DB to controller
    '''

    def __init__(self, user_name = None, user_password=None, session = None):
        '''
        This constructor has at least a session object to start petitions agains 
        '''
        if session != None:
            self.session = session
        elif user_name != None and user_password != None:
            self.session = Models.get_session(user_name, user_password, sqlite=False)
        else:
            self.session = Models.get_session()
        
    def get_all_clients(self):
        return self.session.query(Models.Client).all()
    
    def get_client_columns(self):
        return self.session.query(Models.Client.name, 
                           Models.Client.surname,
                           Models.Client.dni).all()
                                             
    def get_client(self, dni):
        return self.session.query(Models.Client).filter(Models.Client.dni==dni).first()

    def delete_client(self, dni):
        self.session.query(Models.Client).filter(Models.Client.dni==dni).delete()
        self.session.commit()
    
    def insert_client(self, client):
        self.session.add(client)
        self.session.commit()

    def modify_client(self, dni, client):
        dic = {
                Models.Client.name : client.name,
                Models.Client.surname : client.surname,
                Models.Client.dni : client.dni,
                Models.Client.email : client.email,
                Models.Client.web : client.web,
                }
        self.session.query(Models.Client).filter(Models.Client.dni==dni).update(dic)
        self.session.commit()

    def insert_test_clients(self):
        Models.insert_test(self.session)

    def client_exist(self, dni):
        """Check if client exist in the db"""
        if self.get_client(dni)==None:
            return False
        else:
            return True

if __name__ == '__main__':
    dbman = db_manager()
    print dbman.get_client_columns()
