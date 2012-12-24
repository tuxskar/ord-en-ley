'''
Created on Nov 17, 2012

@author: tuxskar
'''
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  
import db.db_manager
import views.main
import views.client
import gtk

class Controller(object):
    '''
    The controller part of the Model-View-Controller design pattern
    '''
    #_main_view = None

    def __init__(self, user_name=None, user_password=None):
        '''
        Initialize the controller with db_manager and views needs
        '''
        self.db_manager = db.db_manager.db_manager(user_name, user_password)
        self.main_view = None
        self.client_views = {}
        self.new_clients_views = []
        self._nclientviews = 0
        
    def init_main(self):
        for client in self.db_manager.get_client_columns():
            row_client = [client[0], client[1], client[2]]
            self.main_view.add_row_client(row_client)
        self.main_view.show()
        
    def connect_main_view(self, view):
        self.main_view = view

    def show_client_info(self, dni=None, kind=None):
        if dni!=None:
            client = self.db_manager.get_client(dni)
            client_info = views.client.client_view(self,client, c_id=client.dni)
            self.client_views[client.dni] = client_info
        else:
            c_id = self._new_client_view_id()
            client_info = views.client.client_view(self,kind=kind, c_id=c_id)
            self.client_views[c_id] = client_info
        client_info.show()

    def _new_client_view_id(self):
        """generate a new id for new client view"""
        self._nclientviews += 1
        return "#:" + str(self._nclientviews)
    
    def insert_new_client(self, client):
        self.db_manager.insert_client(client)
        
    def refresh_clients_main_view(self, client, old_dni=None):
        row_client = [client.name, client.surname, client.dni]
        self.main_view.add_row_client(row_client, old_dni)
    
    def delete_client(self, dni):
        self.db_manager.delete_client(dni) 

    def to_modify(self, dni, client):
        self.db_manager.modify_client(dni, client)
        
    def hide_view(self, dni):
        """Hide client_view by dni"""
        self.client_views.get(dni).hide()

    def insert_test_clients(self):
        self.db_manager.insert_test_clients()

    def client_exist(self, dni):
        """Check if client with dni==dni is already in the system"""
        # TODO focus row with dni==dni in main_view
        return self.db_manager.client_exist(dni)

if __name__ == '__main__':
    cont = Controller()
    main_view = views.main.main_view(cont)
    cont.connect_main_view(main_view)
    cont.init_main()
    gtk.main()
