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
        self.cm = db_client_manager(self.session)
        self.am = db_address_manager(self.session)

    def new_session(self):
        """Method to create a new session"""
        self.session = models.Models.get_session()
        self.cm.self.session = self.session
        self.am.self.session = self.session

class db_client_manager(object):
    def __init__(self, session):
        """db_client_constructor, it needs session to manage be built in"""
        self.session = session

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

class db_address_manager(object):
    def __init__(self, session):
        """db_address_manager constructor, it needs a session to build it in"""
        self.session = session

    def address_exist(self, a):
        """Function to check if an address is already on the system
        if the address is already on the system returns the actual id, otherwise False"""
        if not(a in self.session):
            aid = self.session.query(models.Models.Address.id).\
                    filter(models.Models.Address.street==a.street,
                        models.Models.Address.number      == a.number,
                        models.Models.Address.city        == a.city,
                        models.Models.Address.state       == a.state,
                        models.Models.Address.country     == a.country,
                        models.Models.Address.postal_code == a.postal_code).first()
            if aid == None:
                return False
            return aid.id
        return a.id

    def delete_address(self, a):
        """Method to delete the address a"""
        id = self.address_exist(a) 
        if id != False:
            self.session.query(models.Models.Address).filter(models.Models.Address.id==a.id).delete()
            self.session.commit()

    def get_all_address(self):
        """Method to return all the address in the system"""
        return self.session.query(models.Models.Address).all()

    def get_address_columns(self):
        pass

    def insert_address(self, a):
        """Method to insert a new address a """
        self.session.add(a)
        self.session.commit()

    def modify_address(self, a, b):
        """Method to modify the address _a_ using the _b_ address instead"""
        cc = a.clients
        for cli in cc:
            self.insert_address_to_client(cli,b,False)
        self.session.delete(a)
        self.session.commit()

    def insert_address_to_client(self, client, address, commit=True):
        """Method to add new address to the client client"""
        self.session.add(address)
        address.clients.append(client)
        if commit==True:
            self.session.commit()

def main():
    """main fuction in db_manager"""
    return True

if __name__ == '__main__':
    main()
