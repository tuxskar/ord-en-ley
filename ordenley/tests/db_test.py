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
import ordenley.tests

class db_test(unittest.TestCase):
    def setUp(self):
        user = None
        u_pass = None
        self.db_manager = db.db_manager.db_manager(user,u_pass)
        self.clients_inserted = []

    def tearDown(self):
        for c in self.clients_inserted:
            self.db_manager.delete_client(c.dni)

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

    def random_string(self, length=10):
        s = ""
        for n in range(length):
            s += random.choice(string.ascii_letters + string.digits)
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
