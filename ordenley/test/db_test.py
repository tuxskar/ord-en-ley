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
        self.clients_inserted.append(client)
        g_client = self.db_manager.get_client(client.dni)
        self.assertEqual(client, g_client)
        
        pass

    def random_string(self, length=10):
        s = ""
        for n in range(length):
            s += random.choice(string.ascii_letters + string.digits)
        return s

    def random_client(self):
        name = self.random_string()
        surname = self.random_string()
        dni = self.random_string(4)
        web = self.random_string()
        email = self.random_string()
        client = models.Models.Client(
                name = name,
                surname = surname,
                web = web,
                email = email,
                dni = dni)
        return client

if __name__ == '__main__':
    unittest.main()
