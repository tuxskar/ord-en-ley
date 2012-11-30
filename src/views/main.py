# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2012

@author: skar
'''
import sys,os.path

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
        dir = os.path.dirname(__file__)
        self.filename = os.path.join(dir, "../interfaces/main_view.glade")
        self.main_window_name = "main_view"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.filename)

        self.treeview = self.builder.get_object("client_tree")
        self.liststore = self.builder.get_object("client_store")
        self.notifier_label = self.builder.get_object("notifier_label")
        
        self.window = self.builder.get_object(self.main_window_name)
        
        dic = {
        "on_main_view_destroy" : self.quit,
        "on_client_tree_row_activated" : self.row_activated,
        "on_new_client_clicked" : self.new_client,
        "on_delete_client_clicked" : self.delete_client,
               }
        self.builder.connect_signals(dic)
        
        
    
    def add_row_client(self, client_column, pos = None):
        if pos == None:
            self.liststore.append(client_column)
        else:
            self.liststore.insert(pos, client_column)
    
    def row_activated(self, tree_view, path, column):
        treeiter = self.liststore.get_iter(path)
        dni = self.liststore.get_value(treeiter, 2)
        self.controller.show_client_info(dni)
    
    def new_client(self, new_button):
        self.controller.show_client_info(None, kind="new")
        
    def delete_client(self, new_button):
        model, path = self.treeview.get_selection().get_selected()
        if path != None:
            dni = model.get_value(path, 2)
#TODO add a pop-up view to ask if user is sure want to delete client with dni=dni
            self.controller.delete_client(dni)
            model.remove(path)
            self.notifier_label.set_text("Client with dni: %s, has been deleted" % dni)
        else:
            self.notifier_label.set_text("Row to delete must be selected") 


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
