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
    def __init__(self, user_name=None, user_password=None, main_view=None):
        """
        Initialize the controller with db_manager and views needs
        """
        self.db_manager = db.db_manager.db_manager(user_name, user_password)
        self.main_view = main_view
        self.__client_views = {}
        self.__new_clients_views_count = 0

    ######### Manage client_view ########
    def show_client(self, kind, client_id=None):
        """
            Method to show new client_view window
            kind , data
            new  , None   : Shows a new client_view window to insert a new client
            info , client_id : Shows a client_view window with client information
        """
        if kind == "new":
            self.__new_clients_views_count += 1
            title_view = "New client"
            client_view = views.client.client_view(ctrl=self,title=title_view)
        elif kind == "info":
            client = self.db_manager.clients.get_client(client_id)
            client.name.capitalize()
            title_view = client.name.capitalize() + " " + client.surname.capitalize()
            client_view = views.client.client_view(self, client, title_view)
            self.__client_views[client.id] = client_view
        client_view.show()

    def client_returned_values(self, modification=None, mod_obj=None, 
                                new_object=None, old_id=None):
        """
            Method to get the returned values from client_view
            This method is called when you finish modify a client in client_view and 
            you want to return all the modifications
            Args     : modification , mod_obj  , new_object    , old_id
            values   : client       , delete   , client      , client.id
                     :              , modified ,             ,            -- modify or delete client with old id old_id
                     :              , new      ,             , None
                     : address      , delete   , address     , address.id
                     :              , modified ,             ,            -- modify or delete address with old id old_id
                     :              , new      ,             , None 
                     : view         , delete   , view_object , None       -- Delete the client view_object
        """
        manager = None
        #Note: the unique variation for address, client, etc, is the db_manager controller am, cm, etc
        if modification=="client":
            manager = self.db_manager.clients
        elif modification == "address":
            manager = self.db_manager.address
        if mod_obj == "delete":
            manager.delete(old_id)
        elif mod_obj == "modified":
            manager.modify(new_object, old_id)
        elif mod_obj == "new":
            manager.insert(new_object)
        if modification == "view":
            del new_object

    def hide_view(self, view):
        """
            Method to hide the view with id view=client_id or main_view
            arg: view
            values: "main"    -- hide the main_view
                    client_id -- hide the client_view with id=client_id
        """
        if view=="main":
            self.main_view.hide()
        else:
            self.__client_views.get(view).hide()

    ######## Manage main_view ########
    def init_main(self):
        """
            Method to populate the main_view at the begining of the 
            program execution
        """
        for client in self.db_manager.clients.get_client_columns():
            row_client = [client[0],client[1], client[2], client[3]]
            self.main_view.add_row_client(row_client)
        self.main_view.show()

    def connect_main_view(self, view):
        """
            Method to connect controller with unique main_view
        """
        self.main_view = view

    def fill_up_main_view(self):
        """
            Method to fill up main_view client_tree
        """
        for client in self.db_manager.clients.get_client_columns():
            row_client = [client[0], client[1], client[2]]
            self.main_view.add_row_client(row_client)
        self.main_view.show()
        
    def add_client_row(self, client):
        """
            Method to add the client to the main_view client_tree
        """
        self.main_view.new_client_row(client)

    def insert_test_clients(self):
        """
            Method to insert a dummy data if the database is empty
        """
        self.db_manager.clients.insert_test_clients()

if __name__ == '__main__':
    cont = Controller()
    main_view = views.main.main_view(cont)
    cont.connect_main_view(main_view)
    cont.init_main()
    gtk.main()
