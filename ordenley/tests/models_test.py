# -*- coding: utf-8 -*-
'''
Created on Dec 8, 2012

@author: tuxskar
'''
import models.Models
import unittest
import os

class models_test(unittest.TestCase):
    def test_representation(self):
        """representation test"""
        name = "Ana Mara"
        surname ="mogg"
        dni = "12341234R"
        email = "anamm@noth.ing"
        web = "anamogg.com"
        c = models.Models.Client(name, surname, dni, email, web)
        self.assertEqual(str(c), "<Client('%s','%s','%s')>" % (dni, name, surname))

    def test_session_sqlite(self):
        """test for session_and_insert_test"""
        session = models.Models.get_session(sqlite=True)
        self.assertTrue(os.path.exists(os.path.expanduser("~/.ordenley/%s" % models.Models.sqlite_db_name)))

    def test_session_mysql(self):
        """test for mysql db"""
        session = models.Models.get_session(user = "skar", password = "mypass", sqlite=False)
        models.Models.insert_test(session)
        self.assertTrue(models.Models.delete_first_test(session))

    def test_main(self):
        """test for main fuction"""
        models.Models.main()


    def test_insert_test(self):
        """test for insert_test_test"""
        session = models.Models.get_session(sqlite=True)
        models.Models.delete_sqlite_db(session)
        session = models.Models.get_session(sqlite=True)
        self.assertTrue(models.Models.insert_test(session))

if __name__ == '__main__':
    unittest.main()
