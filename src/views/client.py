'''
Created on Nov 17, 2012

@author: skar
'''
import sys
try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  

try:  
    import gtk   
except:  
    print("GTK Not Availible")
    sys.exit(1)
from db import db_manager
import models.Models
import controllers.controller

class client_view(object):
    '''
    This view show a client info
    '''

    def __init__(self, client=None, kind=None):
        '''
        
        '''
        self.filename = "../interfaces/client_view.glade"
        self.main_window_name = "client_info"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.filename)
        self.controller = controllers.controller.Controller()
        
        self.window = self.builder.get_object(self.main_window_name)
        self.name_entry = self.builder.get_object("name_entry")
        self.surname_entry = self.builder.get_object("surname_entry")
        self.dni_entry = self.builder.get_object("dni_entry")
        self.email_entry = self.builder.get_object("email_entry")
        self.web_entry = self.builder.get_object("web_entry")
            
        dic = {
            "on_client_info_destroy" : self.quit,
            "on_cancel_clicked" : self.quit,
              }
        
        if kind == "new":    
            dic['on_apply_clicked'] = self.new_apply    
        if client!=None:
            dic['on_apply_clicked'] = self.to_modify 
            self.name_entry.set_text(_None_to_str(client.name))
            self.surname_entry.set_text(_None_to_str(client.surname))
            self.dni_entry.set_text(_None_to_str(client.dni))
            self.email_entry.set_text(_None_to_str(client.email))
            self.web_entry.set_text(_None_to_str(client.web))
        
        self.builder.connect_signals(dic)
    
    def to_modify(self):
        pass
    
    def new_apply(self, apply_button):
        # TODO check dni is not none
        client = models.Models.Client(self.name_entry.get_text(),
                                      self.surname_entry.get_text(),
                                      self.dni_entry.get_text(),
                                      self.email_entry.get_text(),
                                      self.web_entry.get_text(),
                                      )
        print "New apply clicked client: "
        print client
    #self.controller.insert_new_client(client)
        
    
    def quit(self, widget):
#        gtk.main_quit()
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
    db_man = db_manager.db_manager()
    client = db_man.get_all_clients()[0]
    cl_view = client_view(client)
    cl_view.window.show()    
    gtk.main()
