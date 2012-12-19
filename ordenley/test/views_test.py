# -*- coding: utf-8 -*-
'''
Created on Dec 8, 2012

@author: tuxskar
'''

import unittest
import gtk
import views.main
import views.client
import controllers.controller

class main_test(unittest.TestCase):
    def setUp(self):
        """Setup for main_view window test"""
        self.controller = controllers.controller.Controller()
        self.main_view = views.main.main_view(self.controller)
        self.m_window = self.main_view.get_window()
        buttons = self.main_view.get_buttons()
        self.b_new_client = buttons[0]
        self.b_del_client = buttons[1]

        print "main Window title: " + str(self.m_window.get_title())

    #def destroy_test(self):
        #self.assertRaises(RuntimeError,self.m_window.destroy())

    def new_client_test(self):
        """new_client add from GUI"""
        self.main_view.new_client(self.b_new_client)


class client_test(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
