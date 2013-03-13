# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2012

@author: tuxskar
'''
import sys
import views

try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  

try:  
    import gtk   
except:  
    print("GTK Not Available")
    sys.exit(1)
import glib

class main_view(object):
    '''
    This is the main view that represent the whole application dashboard
    '''

    def __init__(self, ctrl):
        '''
        Build the main dashboard view using the main_view.glade file 
        located in interfaces
        '''
        self.controller = ctrl
        self.builder = gtk.Builder()
        self.main_window_name = "Ord-en Ley"
        glade_name = "main_view.glade"
        try:
            self.filename = views.get_data_dev(glade_name)
            self.builder.add_from_file(self.filename)
        except glib.GError:
            self.filename = views.get_data(glade_name)
            self.builder.add_from_file(self.filename)

        self.treeview = self.builder.get_object("client_tree")
        self.liststore = self.builder.get_object("client_store")
        self.notifier_label = self.builder.get_object("notifier_label")
        #dni_column = self.builder.get_object("id_column")
        #dni_column.set_visible(False)
        
        self.window = self.builder.get_object(self.main_window_name)

        print "self.window=" + str(self.window)
        print "self.filename=" + str(self.filename)
        print "self.builder=" + str(self.builder)
        
        dic = {
        "gtk_main_quit" : self.quit,
        "on_main_view_destroy" : self.quit,
        "on_client_tree_row_activated" : self.row_activated,
        "on_new_client_clicked" : self.new_client,
        "on_delete_client_clicked" : self.delete_client,
               }
        self.builder.connect_signals(dic)
        self.activated_clients = []
        self.window.set_title("Ord-en Ley")
        # iter_id is a variable to get all pairs id iter in the liststore
        self.__iter_id = {}
        
    
    def add_row_client(self, client_column, old_id=None):
        """
            This method add new row client if doesn't exist it append a new one, otherwise 
            it modify the actual client Treerow
            the rows have the next structure
            c_id | name | surname | DNI | street | number | city | state | postal_code
            where c_id column is hidden
        """
        if old_id != None:
            treeiter = self.__iter_id.get(old_id)
            self.liststore.insert_before(treeiter, client_column)
            self.liststore.remove(treeiter)
            self.__iter_id[client_column[0]] = treeiter
            self.info("Modified client: %s %s" % (client_column[1],client_column[2]))
        else:
            treeiter = self.liststore.append(client_column)
            #client_column[0] is client_id
            self.__iter_id[client_column[0]] = treeiter
            self.info("Added client %s %s" % (client_column[1], client_column[2]))
    
    def row_activated(self, tree_view, path, column):
        treeiter = self.liststore.get_iter(path)
        #it get the id of the client selected stored in liststore
        c_id = self.liststore.get_value(treeiter, 0).decode('utf-8')
        self.activated_clients.append(c_id)
        self.controller.show_client("info", c_id)
    
    def deactivate_client(self, c_id):
        """Remove client from activated_clients by c_id"""
        if self.activated_clients.count(c_id) != 0:
            self.activated_clients.remove(c_id)
            return True
        else:
            return False

    def new_client(self, new_button):
        self.controller.show_client_info(kind="new")
        self.info("Inserting new client")

    def info(self, msg):
        """
            Method to show the msg using view notifier
        """
        self.notifier_label.set_text(msg)
        
    def delete_client(self, delete_button):
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter != None:
            c_id = model.get_value(treeiter, 0)
            name = model.get_value(treeiter, 1).decode('utf8')
            surname = model.get_value(treeiter, 2).decode('utf8')
            dni = model.get_value(treeiter, 3).decode('utf8')
            keep = self.delete_client_dialog(name, surname, dni)
            print "id "      + str(c_id)
            print "name "    + str(name)
            print "surname " + str(surname)
            print "dni "     + str(dni)

            if not keep:
                #hide view_client if exist and delete
                if self.deactivate_client(c_id):
                    self.controller.hide_view(c_id)
                self.controller.client_returned_values("client","delete",None, c_id)
                model.remove(treeiter)
                self.info("Client %s %s with dni: %s, has been deleted" % \
                    (name, surname, dni))
            else:
                self.info("No client deleted")
        else:
            self.info("A Row must be selected to be deleted") 

    def delete_client_dialog(self, name, surname, dni):
        delete_dialog = gtk.Dialog("Delete client", self.window,
                                  gtk.DIALOG_MODAL,
                                  ( gtk.STOCK_NO, True ,
                                    gtk.STOCK_YES, False))
        label = gtk.Label("Are you sure you want to delete the client: \n\
                Name: %s \n\
                Surname: %s \n\
                DNI: %s?\n" % (name, surname, dni))
        delete_dialog.get_content_area().pack_start(label)
        delete_dialog.show_all()
        res =  delete_dialog.run()
        delete_dialog.hide()
        return res

    def show(self):
        self.window.show()
    
    def hide(self):
        self.window.hide()
        
    def quit(self, widget):
        gtk.main_quit()

if __name__ == '__main__':
    gui = main_view()
    gui.window.show()
    gtk.main()
