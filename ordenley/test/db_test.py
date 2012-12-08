# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2012

@author: skar
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
        pass
        #for c in self.clients_inserted:
            #self.db_manager.delete_client(c.dni)

    def test_insert_client(self):
        old_clients = self.db_manager.get_all_clients()
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
        self.clients_inserted.append(client)

        old_clients.append(client)
        self.db_manager.insert_client(client)
        new_clients = self.db_manager.get_all_clients()
        self.assertEqual(old_clients, 
                        new_clients)
        #print self.clients_inserted

    def random_string(self, length=10):
        s = ""
        for n in range(length):
            s += random.choice(string.ascii_letters + string.digits)
        return s

if __name__ == '__main__':
    unittest.main()

