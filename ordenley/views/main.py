# -*- coding: utf-8 -*-
'''
Created on Nov 17, 2012

@author: skar
'''
import sys,os.path
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
        self.filename = views.get_data("main_view.glade")
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
        self.values = {}
        
    
    def add_row_client(self, client_column, old_dni=None):
        #TODO optimitation using the old position of the client that you have update
        if self.values.has_key(old_dni):
            titer = self.liststore.insert_after(self.values.get(old_dni),client_column)
            self.liststore.remove(self.values.pop(old_dni))
            self.notifier_label.set_text("Modified client with old DNI: %s" % old_dni) 
        else:
            titer = self.liststore.append(client_column)
            self.notifier_label.set_text(("Added client %s %s" % (client_column[0], client_column[1])))
        self.values[client_column[2]] = titer
    
    def row_activated(self, tree_view, path, column):
        treeiter = self.liststore.get_iter(path)
        dni = self.liststore.get_value(treeiter, 2).decode('utf-8')
        self.controller.show_client_info(dni)
    
    def new_client(self, new_button):
        self.controller.show_client_info(None, kind="new")
        self.notifier_label.set_text("Inserting new client")
        
    def delete_client(self, new_button):
        model, path = self.treeview.get_selection().get_selected()
        if path != None:
            dni = model.get_value(path, 2).decode('utf8')
            name = model.get_value(path, 0).decode('utf8')
            surname = model.get_value(path, 1).decode('utf8')
            keep = self.delete_client_dialog(name, surname, dni)
            if not keep:
                self.controller.delete_client(dni)
                model.remove(path)
                self.notifier_label.set_text("Client %s %s with dni: %s, has been deleted" % \
                    (name, surname, dni))
            else:
                self.notifier_label.set_text("No client deleted")
        else:
            self.notifier_label.set_text("A Row must be selected to be deleted") 

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
