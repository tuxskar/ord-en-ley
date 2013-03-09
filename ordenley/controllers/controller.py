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
    """
    The controller part of the Model-View-Controller design pattern
    """
    def __init__(self, user_name=None, user_password=None, ctlr=None):
        """
        Initialize the controller with db_manager and views needs
        """
        self.db_manager = db.db_manager.db_manager(user_name, user_password)
        self.main_view = ctlr
        self.client_views = {}
        self.new_clients_views = []

    ######### Manage client_view ########
    def show_client(self, kind, data=None):
        """
        Method to show new client_view window
        kind , data
        new  , None   : Shows a new client_view window to insert a new client
        info , client : Shows a client_view window with client information
        """
        pass

    def client_returned_values(self, modification=None, mod_obj=None, 
                                new_data=None, old_id=None):
        """
        Method to get the returned values from client_view
        This method is called when you finish modify a client in client_view and 
        you want to return all the modifications
        Args   : modification , mod_obj  , new_data , old_id
        values : None         , None     , None     , None       __ No modification at all
               : client       , delete   , client   , client.id
               :              , modified ,          ,            __ modify or delete client with old id old_id
               : address      , delete   , address  , address.id
               :              , modified ,          ,            __ modify or delete address with old id old_id
        """
        pass

    def hide_client_view(self, view):
        """
        Method to hide the view with id equal to client_id
        arg: view
        values: "main"    -- hide the main_view
                client_id -- hide the client_view with id=client_id
        """
        pass

    ######## Manage main_view ########
    def connect_main_view(self, view):
        """
        Method to connect controller with unique main_view
        """
        self.main_view = view

    def fill_up_main_view(self):
        """
        Method to fill up main_view client_tree
        """
        for client in self.db_manager.cm.get_client_columns():
            row_client = [client[0], client[1], client[2]]
            self.main_view.add_row_client(row_client)
        self.main_view.show()
        
    def add_client_row(self, client):
        """
        Method to add the client to the main_view client_tree
        """
        pass



######## this is end of methods with the new method structure #########
    def show_client_info(self, dni=None, kind=None):
        if dni!=None:
            client = self.db_manager.cm.get_client(dni)
            client_info = views.client.client_view(self,client, c_id=client.dni)
            self.client_views[client.dni] = client_info
        else:
            c_id = self.__new_client_view_id()
            client_info = views.client.client_view(self,kind=kind, c_id=c_id)
            self.client_views[c_id] = client_info
        client_info.show()

    def __new_client_view_id(self):
        """generate a new id for new client view"""
        return "#:" + str(len(self.new_clients_views)+1)
    
    def insert_new_client(self, client):
        self.db_manager.cm.insert_client(client)
        
    def refresh_clients_main_view(self, client, old_dni=None):
        row_client = [client.name, client.surname, client.dni]
        self.main_view.add_row_client(row_client, old_dni)
    
    def delete_client(self, dni):
        self.db_manager.cm.delete_client(dni) 

    def to_modify(self, dni, client):
        self.db_manager.cm.modify_client(dni, client)
        
    def hide_view(self, dni):
        """Hide client_view by dni"""
        self.client_views.get(dni).hide()

    def insert_test_clients(self):
        self.db_manager.cm.insert_test_clients()

    def client_exist(self, dni):
        """Check if client with dni==dni is already in the system"""
        # TODO focus row with dni==dni in main_view
        return self.db_manager.cm.client_exist(dni)

if __name__ == '__main__':
    cont = Controller()
    main_view = views.main.main_view(cont)
    cont.connect_main_view(main_view)
    cont.init_main()
    gtk.main()
