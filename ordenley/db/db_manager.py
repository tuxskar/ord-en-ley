# -*- coding: utf-8 -*-
"""
Created on Nov 17, 2012

@author: tuxskar
"""
import models.Models

class db_manager(object):
    """
    This module is the layer between physical DB to controller
    """

    def __init__(self, user_name = None, user_password=None, session = None):
        """
        This constructor has at least a session object to start petitions agains 
        """
        if session != None:
            self.session = session
        elif user_name != None and user_password != None:
            self.session = models.Models.get_session(user_name, user_password, sqlite=False)
        else:
            self.session = models.Models.get_session()
        self.clients = db_client_manager(self.session)
        self.address = db_address_manager(self.session)

    def new_session(self):
        """Method to create a new session"""
        self.session = models.Models.get_session()
        self.clients.self.session = self.session
        self.address.self.session = self.session

class db_client_manager(object):
    def __init__(self, session):
        """db_client_constructor, it needs session to manage be built in"""
        self.session = session

    def get_all_clients(self):
        return self.session.query(models.Models.Client).all()
    
    def get_client_columns(self):
        return self.session.query(
                           models.Models.Client.id, 
                           models.Models.Client.name, 
                           models.Models.Client.surname,
                           models.Models.Client.dni).all()
                                             
    def get_client(self, client_id):
        return self.session.query(models.Models.Client).filter(models.Models.Client.id==client_id).first()

    def delete(self, client_id):
        self.session.query(models.Models.Client).filter(models.Models.Client.id==client_id).delete()
        self.session.commit()
    
    def insert(self, client):
        print client.id
        if client.id != None:
            client.id = None
        self.session.add(client)
        self.session.commit()
        #self.session.flush()

    def modify(self, client, old_client_id):
        a = self.get_client(old_client_id)
        a.name = client.name
        a.surname = client.surname
        a.dni = client.dni
        a.email = client.email
        a.web = client.web
        self.session.add(a)
        self.session.commit()

    def insert_test_clients(self):
        models.Models.insert_test(self.session)

    def exist(self, client_id):
        """Check if client exist in the db"""
        if self.get_client(client_id):
            return True
        else:
            return False

class db_address_manager(object):
    def __init__(self, session):
        """db_address_manager constructor, it needs a session to build it in"""
        self.session = session

    def exist(self, a_id):
        """Function to check if an address with id==a_id is already on the system
        if the address is already on the system returns the actual id, otherwise False"""
        aid = self.session.query(models.Models.Address.id).\
                filter(models.Models.Address.id==a_id).first()
        if aid == None:
            return False
        return aid

    def exist_by_object(self, a):
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

    def delete(self, a):
        """Method to delete the address a"""
        (ret_id,) = self.exist(a) 
        if ret_id != False:
            self.session.query(models.Models.Address).filter(models.Models.Address.id==ret_id).delete()
            self.session.commit()

    def get_all(self):
        """Method to return all the address in the system"""
        return self.session.query(models.Models.Address).all()

    def get_address(self, add_id):
        """Method to return all the address in the system"""
        return self.session.query(models.Models.Address).filter(models.Models.Address.id==add_id).first()

    def get_address_columns(self):
        pass

    def insert(self, a):
        """Method to insert a new address a """
        if a.id != None:
            a.id = None
        print "clientes de a "
        print a.clients
        for c in a.clients:
            self.insert_address_to_client(c,a)
        self.session.add(a)
        self.session.commit()
        print "hecho"

    def modify(self, a, b_id):
        """Method to modify the address _a_ using the _b_ address instead"""
        b_address = self.get_address(b_id)
        b_address.street      = a.street
        b_address.number      = a.number
        b_address.city        = a.city
        b_address.state       = a.state
        b_address.country     = a.country
        b_address.postal_code = a.postal_code
        self.session.add(b_address)
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
