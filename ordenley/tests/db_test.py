# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2012

@author: tuxskar
'''
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
import db.db_manager
import models.Models
import random
import string

class db_test(unittest.TestCase):
    def setUp(self):
        user = None
        u_pass = None
        self.db_manager = db.db_manager.db_manager(user,u_pass)
        self.clients_inserted = []
        self.addresss_inserted = []

    def tearDown(self):
        for c in self.clients_inserted:
            self.db_manager.delete_client(c.dni)
        #TODO
        #for a in self.addresss_inserted:
            #self.db_manager.delete_address(a.street)

    def test_client_insert(self):
        old_clients = self.db_manager.get_all_clients()
        client = self.random_client()
        self.clients_inserted.append(client)
        old_clients.append(client)
        self.db_manager.insert_client(client)
        new_clients = self.db_manager.get_all_clients()
        self.assertEqual(old_clients, new_clients)

    def test_client_update(self):
        client = self.random_client()
        self.clients_inserted.append(client)
        self.db_manager.insert_client(client)
        old_dni = client.dni
        client.name += client.name
        client.surname += client.surname
        client.dni += client.dni
        client.web+= client.web
        client.email+= client.email
        self.db_manager.modify_client(old_dni, client) 
        client_modified = self.db_manager.get_client(client.dni)
        self.assertEqual(client,client_modified)

    def test_client_delete(self):
        old_clients = self.db_manager.get_all_clients()
        client = self.random_client()
        self.db_manager.insert_client(client)
        self.db_manager.delete_client(client.dni)
        new_clients = self.db_manager.get_all_clients()
        self.assertEqual(old_clients, new_clients)

    def test_client_search(self):
        client = self.random_client()
        self.db_manager.insert_client(client)
        self.db_manager.client_exist(client.dni)
        self.clients_inserted.append(client)
        g_client = self.db_manager.get_client(client.dni)
        self.assertEqual(client, g_client)
        #This DNI is a imposible one because a dni is a consecution of numbers and a simple letter
        self.assertFalse(self.db_manager.client_exist("XXXXxxkjd9999999999"))

    def test_address_insert(self):
        #TODO
        #get_all_address
        #insert_address

        #actual address in the db
        old_addresss = self.db_manager.get_all_addresss()
        address = self.random_address()
        old_addresss.append(address)
        #all address plus random address

        self.db_manager.insert_address(address)
        new_addresss = self.db_manager.get_all_addresss()
        self.assertEqual(old_addresss, new_addresss)

        self.addresss_inserted.append(address)

    def test_address_update(self):
        #TODO
        #insert_address
        #modify_address
        #get_address
        address = self.random_address()
        old_address = address
        self.addresss_inserted.append(address)
        self.db_manager.insert_address(address)
        address.street      += address.street      
        address.number      += address.number      
        address.city        += address.city        
        address.state       += address.state       
        address.country     += address.country     
        address.postal_code += address.postal_code
        self.db_manager.modify_address(old_address, address) 
        address_modified = self.db_manager.get_address(address.street)
        self.assertequal(address,address_modified)

    def test_address_delete(self):
        #TODO
        #insert_address
        #delete_address
        #get_all__address
        old_addresss = self.db_manager.get_all_addresss()
        address = self.random_address()
        self.db_manager.insert_address(address)
        self.db_manager.delete_address(address.dni)
        new_addresss = self.db_manager.get_all_addresss()
        self.assertEqual(old_addresss, new_addresss)

    def test_address_search(self):
        #TODO
        #insert_address
        #exist_address
        #get__address
        address = self.random_address()
        self.db_manager.insert_address(address)
        self.db_manager.exist_address(address.dni)
        self.addresss_inserted.append(address)
        g_address = self.db_manager.get_address(address.dni)
        self.assertEqual(address, g_address)

    def random_string(self, length=10):
        s = ""
        for n in range(length):
            s += random.choice(string.ascii_letters + string.digits)
        return s

    def random_integer(self, length=10):
        s = ""
        for n in range(length):
            s += random.choice(string.digits)
        return s

    def random_client(self):
        name = self.random_string()
        surname = self.random_string()
        dni = self.random_string(9)
        web = self.random_string()
        email = self.random_string()
        client = models.Models.Client(
                name = name,
                surname = surname,
                web = web,
                email = email,
                dni = dni)
        return client

    def random_address(self):
        street = self.random_string()
        number = self.random_integer()
        city = self.random_string(9)
        state = self.random_string()
        posta_code = self.random_integer()
        address = models.Models.Address(
                street = street,
                number = number,
                city = city,
                state = state,
                posta_code = posta_code)
        return address

    def test_differents_session(self):
        """Test all kind of session you can have"""
        session1 = models.Models.get_session()
        session2 = models.Models.get_session("skar", "mypass")
        db_manager1 = db.db_manager.db_manager()
        db_manager2 = db.db_manager.db_manager(session = session1)
        db_manager3 = db.db_manager.db_manager("skar", "mypass")
        self.assertEqual(db_manager2.session,session1)
        self.assertNotEqual(db_manager1.session,session1)
        self.assertNotEqual(db_manager3.session,session2)

    def test_get_client_colums(self):
        """get client columns test"""
        columns = self.db_manager.get_client_columns()
        clients = self.db_manager.get_all_clients()
        clients_columns = []
        for c in clients:
            clients_columns.append((c.name,c.surname,c.dni))
        self.assertEqual(columns, clients_columns)

    def test_clients(self):
        """test_clients from db_manager"""
        self.db_manager.insert_test_clients()

    def test_main(self):
        """test for main_test"""
        self.assertTrue(db.db_manager.main())

if __name__ == '__main__':
    unittest.main()
