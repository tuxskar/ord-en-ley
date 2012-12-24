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
import ordenley.tests
import ldtp
import models.Models

class main_test(unittest.TestCase):
    def setUp(self):
        """Setup for main_view window test"""
        self.controller = controllers.controller.Controller()
        self.main_view = views.main.main_view(self.controller)
        self.controller.connect_main_view(self.main_view)
        self.m_window = self.main_view.get_window()
        buttons = self.main_view.get_buttons()
        self.b_new_client = buttons[0]
        self.b_del_client = buttons[1]

        print "main Window title: " + str(self.m_window.get_title())

    #def destroy_test(self):
        #self.assertRaises(RuntimeError,self.m_window.destroy())

    def test_new_client(self):
        """new_client add from GUI"""
        self.main_view.new_client(self.b_new_client)


class client_test(unittest.TestCase):
    def setUp(self):
        """Setup for client_tests"""
        self.controller = controllers.controller.Controller()
        self.main_view = views.main.main_view(self.controller)
        self.controller.connect_main_view(self.main_view)

    def tearDown(self):
        """Teardown for client_test"""
        pass

    def test_new_client_view(self):
        """client view tests for every new client view case"""
        #view to add new client just with random dni
        dni = ordenley.tests.random_string(9)
        self.assertFalse(self.controller.client_exist(dni))

        client_view = views.client.client_view(self.controller, kind="new",c_id="#:1")
        client_view.dni_entry.set_text(dni)
        client_view.entry_changed = True
        client_view.apply_button.clicked()
        #inserted new client with dni=dni
        self.assertTrue(self.controller.client_exist(dni))

        #view to show already storaged client
            #modify client
            #don't do anything with client
        #no c_id to raise exception 

class app_test(unittest.TestCase):
    def setUp(self):
        """docstring for setUp"""
        self.mv_name = "frmOrd-enLey"
        self.new_c_button_name = "btnnew"
        self.delete_c_button_name = "btndelete"
        self.tree_name_mv = "tbl0"
        ldtp.launchapp('python', args=['/home/skar/projects/python/orden-ley/ordenley/tests/run.py'])
        ldtp.guiexist(self.mv_name)
        #ldtp.waittillguiexist(self.mv_name)

    def tearDown(self):
        """docstring for tearDown"""
        ldtp.closewindow(self.mv_name)

    def test_insert_clientfromUI(self):
        """docstring for test_insert_clientfromUI"""
        ldtp.click(self.mv_name, self.new_c_button_name)
        ldtp.guiexist("frmNewclient1")
        ldtp.click("frmNewclient1", "btnCancel")
        ldtp.click(self.mv_name, self.new_c_button_name)
        ldtp.guiexist("frmNewclient2")
        new_c_name = "frmNewclient2"
        dni = "12345678R"
        ldtp.settextvalue("frmNewclient2", "txt4", "Alice")
        ldtp.settextvalue("frmNewclient2", "txt3", "Pound")
        ldtp.click("frmNewclient2", "btnOK")
        ldtp.settextvalue("frmNewclient2", "txt2", dni)
        ldtp.click("frmNewclient2", "btnOK")
        ldtp.singleclickrow(self.mv_name, self.tree_name_mv, "Alice")

        #Alice client changing
        ldtp.doubleclickrow(self.mv_name, self.tree_name_mv, "Alice")
        alice_title = "*DNI:12345678R"
        ldtp.guiexist(alice_title)
        ldtp.click(alice_title, "btnCancel")
        ldtp.doubleclickrow(self.mv_name, self.tree_name_mv, "Alice")
        #alice_title += "1"
        ldtp.guiexist(alice_title)
        ldtp.click(alice_title, "btnOK")

        ldtp.doubleclickrow(self.mv_name, self.tree_name_mv, "Alice")
        ldtp.guiexist(alice_title)
        ldtp.settextvalue(alice_title, "txt3", "Poundssss")
        ldtp.click(alice_title, "btnCancel")
        ldtp.doubleclickrow(self.mv_name, self.tree_name_mv, "Alice")
        ldtp.guiexist(alice_title)
        ldtp.settextvalue(alice_title, "txt3", "Poundssss")
        ldtp.settextvalue(alice_title, "txt2", "678R")
        ldtp.click(alice_title, "btnOK")



        #delete Alice from UI
        ldtp.selectrow(self.mv_name, self.tree_name_mv, "Alice")
        delete_dlg = "dlgDeleteclient"
        ldtp.click(self.mv_name, self.delete_c_button_name)
        ldtp.guiexist(delete_dlg)
        ldtp.click(delete_dlg, "btnNo")

        ldtp.click(self.mv_name, self.delete_c_button_name)
        ldtp.singleclickrow(self.mv_name, self.tree_name_mv, "Alice")
        ldtp.guiexist(delete_dlg)
        ldtp.click(delete_dlg, "btnYes")
        
        #Using dltp and GTK
        #alice = models.Models.Client("Alice","Pound", dni="12345678R")
        #alice_title = "frmClientwithDNI:12345678R"
        #client_v = views.client.client_view(alice,c_id=dni)
        #client_v.show()
        #ldtp.waittillguiexist(alice_title)
        #ldtp.click(client_v, "btnCancel")
        #client_v = views.client.client_view(alice,c_id=dni)
        #client_v.show()
        #ldtp.click(client_v, "btnOK")
        #client_v = views.client.client_view(alice,c_id=dni)
        #client_v.show()
        #ldtp.settextvalue(client_v, "txt3", "Poundssss")
        #ldtp.click(client_v, "btnCancel")
        #client_v = views.client.client_view(alice,c_id=dni)
        #client_v.show()
        #ldtp.settextvalue(client_v, "txt3", "Poundssss")
        #ldtp.settextvalue(client_v, "txt2", "678R")
        #ldtp.click(client_v, "btnOK")
        


if __name__ == '__main__':
    unittest.main()
