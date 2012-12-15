# -*- coding: utf-8 -*-
'''
Created on Dec 8, 2012

@author: tuxskar
'''
import models.Models
import unittest

class models_test(unittest.TestCase):
    def representation_test(self):
        """representation test"""
        name = "Ana María"
        surname ="mögg"
        dni = "12341234R"
        email = "anamm@noth.ing"
        web = "anamögg.com"
        c = models.Models.Client(name, surname, dni, email, web)
        self.assertEqual(str(c), "<Client('%s','%s','%s')>" % (dni, name, surname))

if __name__ == '__main__':
    unittest.main()
