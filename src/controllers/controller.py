'''
Created on Nov 17, 2012

@author: skar
'''
try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  
from db import db_manager
import views.main
import views.client
import gtk

class Controller(object):
    '''
    The controller part of the Model-View-Controller design pattern
    '''


    def __init__(self, user_name=None, user_password=None):
        '''
        Initialize the controller with db_manager and views needs
        '''
        self.db_manager = db_manager.db_manager(user_name, user_password)
    
    def init_main(self):
        self.main_view = views.main.main_view()
        for client in self.db_manager.get_all_clients():
            row_client = [client.name, client.surname, client.dni]
            self.main_view.add_row_client(row_client)
        self.main_view.show()
        
    def show_client_info(self, dni):
##        self.client_info = client_view(client)
        client = self.db_manager.get_client(dni)
        self.client_info = views.client.client_view(client)
        self.client_info.show()

if __name__ == '__main__':
    cont = Controller()
    cont.init_main()
    gtk.main()