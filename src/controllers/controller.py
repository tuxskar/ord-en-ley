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
from views import main
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
        self.main_view = main.main_view()
        for client in self.db_manager.get_all_clients():
            row_client = [client.name, client.surname, client.dni]
            self.main_view.add_row_client(row_client)
        self.main_view.show()

if __name__ == '__main__':
    cont = Controller()
    cont.init_main()
    gtk.main()