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

class db_client_test(unittest.TestCase):
    def setUp(self):
        user = None
        u_pass = None
        self.db_manager = db.db_manager.db_manager(user,u_pass)
        self.db_cm = self.db_manager.clients
        self.clients_inserted = []

    def tearDown(self):
        for c in self.clients_inserted:
            self.db_cm.delete(c)
        #TODO

    def test_client_insert(self):
        old_clients = self.db_cm.get_all_clients()
        client = random_client()
        self.clients_inserted.append(client)
        old_clients.append(client)
        self.db_cm.insert(client)
        new_clients = self.db_cm.get_all_clients()
        self.assertEqual(old_clients, new_clients)

    def test_client_update(self):
        client = random_client()
        self.clients_inserted.append(client)
        self.db_cm.insert(client)
        old_id = client.id
        client.name += client.name
        client.surname += client.surname
        client.dni += client.dni
        client.web+= client.web
        client.email+= client.email
        self.db_cm.modify(client, old_id) 
        client_modified = self.db_cm.get_client(client.id)
        self.assertEqual(client,client_modified)

    def test_client_delete(self):
        old_clients = self.db_cm.get_all_clients()
        client = random_client()
        self.db_cm.insert(client)
        self.db_cm.delete(client)
        new_clients = self.db_cm.get_all_clients()
        self.assertEqual(old_clients, new_clients)

    def test_client_search(self):
        client = random_client()
        self.db_cm.insert(client)
        self.db_cm.exist(client)
        self.clients_inserted.append(client)
        g_client = self.db_cm.get_client(client.id)
        self.assertEqual(client, g_client)

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
        columns = self.db_cm.get_client_columns()
        clients = self.db_cm.get_all_clients()
        clients_columns = []
        for c in clients:
            clients_columns.append((c.name,c.surname,c.dni))
        self.assertEqual(columns, clients_columns)

    def test_clients(self):
        """test_clients from db_manager"""
        self.db_cm.insert_test_clients()

    def test_main(self):
        """test for main_test"""
        self.assertTrue(db.db_manager.main())

class db_address_test(unittest.TestCase):
    def setUp(self):
        """Setup method for address tests"""
        user = None
        u_pass = None
        self.db_manager = db.db_manager.db_manager(user,u_pass)
        self.db_am = self.db_manager.address
        self.db_cm = self.db_manager.clients
        self.address_inserted = []

    def tearDown(self):
        """tearDown method to destroy all address generated"""
        for a in self.address_inserted:
            self.db_ca.delete(a)

    def test_insert(self):
        """This test verify exist, insert and delete address from db"""
        add = random_address()
        while(self.db_am.exist(add) != False):
            add = self.random_address()
        self.db_am.insert(add)
        self.assertTrue(self.db_am.exist(add), int)
        self.db_am.delete(add)
        self.assertFalse(self.db_am.exist(add))

    def test_insert_and_client(self):
        """Test to verify we can insert address joined to clients
       methods tested:
       <Client>.address.append
       <db_client_manager>.insert(<Address>)
        """
        add1 = random_address() 
        add2 = random_address() 
        cc = random_client()
        self.db_cm.insert(cc)

        self.assertFalse(self.db_am.exist(add1))
        self.assertFalse(self.db_am.exist(add2))

        self.db_am.insert_address_to_client(cc, add1)
        self.db_am.insert_address_to_client(cc, add2)

        self.assertTrue(add2.clients[0].dni == cc.dni)
        self.assertTrue(add1.clients[0].dni == cc.dni)
        self.assertTrue(isinstance(cc.address.index(add2), int))
        self.assertTrue(self.db_am.exist(add1))
        self.assertTrue(self.db_am.exist(add2))

    def test_address_update(self):
        dc = self.db_cm
        da = self.db_am
        cc = random_client()
        cc2 = random_client()
        cc3 = random_client()
        add = random_address()
        add2 = random_address()
        add4 = random_address()
        add5 = random_address()

        cc.address.append(add)
        cc.address.append(add2)
        cc2.address.append(add)
        cc3.address.append(add2)

        dc.insert(cc)
        dc.insert(cc2)
        dc.insert(cc3)
        
        da.modify(add4, add.id)
        da.modify(add5, add2.id)

        self.assertTrue(add4.street == add.street)
        self.assertTrue(add4.city == add.city)
        self.assertTrue(add4.state == add.state)

def random_client():
    name = random_string()
    surname = random_string()
    dni = random_string(9)
    web = random_string()
    email = random_string()
    client = models.Models.Client(
            name = name,
            surname = surname,
            web = web,
            email = email,
            dni = dni)
    return client

def random_address():
    street = random_string()
    number = random_integer()
    city = random_string(9)
    state = random_string()
    postal_code = random_integer()
    address = models.Models.Address(
            street = street,
            number = number,
            city = city,
            state = state,
            postal_code = postal_code)
    return address
        
def random_string(length=10):
    s = ""
    for n in range(length):
        s += random.choice(string.ascii_letters + string.digits)
    return s

def random_integer(length=10):
    s = ""
    for n in range(length):
        s += random.choice(string.digits)
    return s

if __name__ == '__main__':
    unittest.main()
