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

class client_view(object):
    '''
    This view show a client info
    '''

    def __init__(self, client=None):
        '''
        TODO
        '''
        if client == None:
            print "Unable to build client info view with a None client"
        else:
            self.filename = "../interfaces/client_view.glade"
            self.main_window_name = "client_info"
            self.builder = gtk.Builder()
            self.builder.add_from_file(self.filename)
        
            self.window = self.builder.get_object(self.main_window_name)
            self.name_entry = self.builder.get_object("name_entry")
            self.surname_entry = self.builder.get_object("surname_entry")
            self.dni_entry = self.builder.get_object("dni_entry")
            self.email_entry = self.builder.get_object("email_entry")
            self.web_entry = self.builder.get_object("web_entry")
            
            dic = {
                   "on_client_info_destroy" : self.quit,
                   }
            self.builder.connect_signals(dic)
            
            self.name_entry.set_text(_None_to_str(client.name))
            self.surname_entry.set_text(_None_to_str(client.surname))
            self.dni_entry.set_text(_None_to_str(client.dni))
            self.email_entry.set_text(_None_to_str(client.email))
            self.web_entry.set_text(_None_to_str(client.web))
    
    def quit(self, widget):
        gtk.quit_add(1,sys.exit(0))
    
    def show(self):
        self.window.show()
        
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
