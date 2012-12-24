# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2012

@author: tuxskar
'''
import models.Models

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
            self.session = models.Models.get_session(user_name, user_password, sqlite=False)
        else:
            self.session = models.Models.get_session()
        
    def get_all_clients(self):
        return self.session.query(models.Models.Client).all()
    
    def get_client_columns(self):
        return self.session.query(models.Models.Client.name, 
                           models.Models.Client.surname,
                           models.Models.Client.dni).all()
                                             
    def get_client(self, dni):
        ret = self.session.query(models.Models.Client).filter(models.Models.Client.dni==dni).first()
        if ret!=None:
            return ret
        else:
            return None

    def delete_client(self, dni):
        self.session.query(models.Models.Client).filter(models.Models.Client.dni==dni).delete()
        self.session.commit()
    
    def insert_client(self, client):
        self.session.add(client)
        self.session.commit()

    def modify_client(self, dni, client):
        dic = {
                models.Models.Client.name : client.name,
                models.Models.Client.surname : client.surname,
                models.Models.Client.dni : client.dni,
                models.Models.Client.email : client.email,
                models.Models.Client.web : client.web,
                }
        self.session.query(models.Models.Client).filter(models.Models.Client.dni==dni).update(dic)
        self.session.commit()

    def insert_test_clients(self):
        models.Models.insert_test(self.session)

    def client_exist(self, dni):
        """Check if client exist in the db"""
        if self.get_client(dni):
            return True
        else:
            return False

def main():
    """main fuction in db_manager"""
    dbman = db_manager()
    dbman.get_client("hola")
    return True

if __name__ == '__main__':
    self.main()
