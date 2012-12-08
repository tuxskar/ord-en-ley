'''
Created on Nov 17, 2012

@author: tuxskar
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

import db.db_manager
import models.Models
import views

class client_view(object):
    '''
    This view show a client info
    '''

    def __init__(self, ctrl, client=None, kind=None):
        '''
        
        '''
        self.controller = ctrl
        self.filename = views.get_data("client_view.glade")
        self.main_window_name = "client_info"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.filename)
        
        self.window = self.builder.get_object(self.main_window_name)
        self.name_entry = self.builder.get_object("name_entry")
        self.surname_entry = self.builder.get_object("surname_entry")
        self.dni_entry = self.builder.get_object("dni_entry")
        self.email_entry = self.builder.get_object("email_entry")
        self.web_entry = self.builder.get_object("web_entry")
        self.warning_label = self.builder.get_object("warning_label")    
        self.apply_button = self.builder.get_object("apply")
        
        dic = {
            "on_client_info_destroy" : self.quit,
            "on_cancel_clicked" : self.quit,
            "client_entry_changed" : self.entry_changed,
              }
        self.old_dni = ""
        self.modified = None
        if kind == "new":    
            dic['on_apply_clicked'] = self.save_apply    
        if client!=None:
            dic['on_apply_clicked'] = self.to_modify 
            self.name_entry.set_text(_None_to_str(client.name))
            self.surname_entry.set_text(_None_to_str(client.surname))
            self.old_dni = _None_to_str(client.dni)
            self.dni_entry.set_text(self.old_dni)
            self.email_entry.set_text(_None_to_str(client.email))
            self.web_entry.set_text(_None_to_str(client.web))
            self.modified = False
        
        self.builder.connect_signals(dic)
    
    def to_modify(self, button):
        if self.modified == True:
            self.modified = False
            self.save_apply(button, self.old_dni)
        else:
            self.window.hide()
    
    def save_apply(self, apply_button, to_update=None):
        dni = self.dni_entry.get_text()
        if dni=="":
            self.warning_label.set_text("Warning, dni field must be filled  ")
            self.warning_label.show()
        else:
            self.warning_label.hide()
            client = models.Models.Client(self.name_entry.get_text(),
                                      self.surname_entry.get_text(),
                                      self.dni_entry.get_text(),
                                      self.email_entry.get_text(),
                                      self.web_entry.get_text(),
                                      )
            if to_update != None:
                self.controller.to_modify(self.old_dni, client)
            else:
                self.controller.insert_new_client(client)
            self.controller.refresh_clients_main_view(client, old_dni=self.old_dni)
            self.window.hide()
        
    def entry_changed(self, widget):
        if self.modified == False:
            self.modified = True
            self.apply_button.set_label("Save")

    def quit(self, widget):
        self.hide()
    
    def show(self):
        self.window.show()
    
    def hide(self):
        self.window.hide()
        
def _None_to_str(txt):
    if txt == None:
        return ""
    return txt
        
if __name__ == '__main__':
    db_man = db.db_manager.db_manager()
    client = db_man.get_all_clients()[0]
    cl_view = client_view(client)
    cl_view.window.show()    
    gtk.main()
