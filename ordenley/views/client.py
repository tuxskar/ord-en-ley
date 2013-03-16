'''
Created on Nov 17, 2012

@author: tuxskar
'''
import sys
import glib

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
        This view shows a client info or a client view for a new client
        If client is None then it is a new client view,
        otherwise it show a client view info
    '''

    def __init__(self, ctrl, client=None, title=None):
        '''
            ctrl: is the controller necessary to manage MVC pattern
            client: could be None for a new client view or client object 
                of client info view
            tittle: is the tittle of the window
        '''
        self.debbuging = True
        self.controller = ctrl
        self.builder = gtk.Builder()
        main_window_name = "client_info"
        glade_name = "client_view.glade"
        try:
            self.filename = views.get_data_dev(glade_name)
            self.builder.add_from_file(self.filename)
        except glib.GError:
            self.filename = views.get_data(glade_name)
            self.builder.add_from_file(self.filename)
        
        self.window = self.builder.get_object(main_window_name)

        ######## client variables #########
        self.name_entry = self.builder.get_object("name_entry")
        self.surname_entry = self.builder.get_object("surname_entry")
        self.dni_entry = self.builder.get_object("dni_entry")
        self.email_entry = self.builder.get_object("email_entry")
        self.web_entry = self.builder.get_object("web_entry")
        self.notification_label = self.builder.get_object("notification_label")    
        self.apply_button = self.builder.get_object("apply")
        self.client_id_label = self.builder.get_object("client_id_label")
        if self.debbuging:
            #For debug
            self.client_id_label.set_visible(True)

        ######## address 1 variables #########
        #to manage address the view store every street entry in a lists 
        #for instance to access to the stree_entry in the tab number 3, you can access
        #using self.street_entries[3]
        #the tabs starts in in 0
        self.street_entries        = {0 : self.builder.get_object("street_entry")}
        self.street_number_entries = {0 : self.builder.get_object("street_number_entry")}
        self.city_entries          = {0 : self.builder.get_object("city_entry")}
        self.state_entries         = {0 : self.builder.get_object("state_entry")}
        self.country_entries       = {0 : self.builder.get_object("country_entry")}
        self.postal_code_entries   = {0 : self.builder.get_object("postal_code_entry")}
        self.id_address_labels     = {0 : self.builder.get_object("id_label")}
        self.address_notebook = self.builder.get_object("address_notebook")
        
        dic = {
            "on_client_info_destroy" : self.quit,
            "on_cancel_clicked" : self.quit,
            "client_entry_changed" : self.client_changed,
            "address_entry_changed" : self.address_changed,
            "on_apply_clicked" : self.save_apply,
              }

        self.window.set_title(title)
        self.client = client
        self.populate_client_view(client)
        self.builder.connect_signals(dic)
        self.modified = [] # Store what kind of object has been modified
        self.modified_add = [] # Store the tab_number of the modified address
        self.new_address = [] # For address added
        self.deleted_address = [] # For address deleted

    def populate_client_view(self, client):
        """
            This method set all the client content into the client_view
        """
        if self.client!=None:
            self.client_id_label.set_text(_None_to_str(str(client.id)))
            self.name_entry.set_text(_None_to_str(client.name))
            self.surname_entry.set_text(_None_to_str(client.surname))
            self.dni_entry.set_text(_None_to_str(client.dni))
            self.email_entry.set_text(_None_to_str(client.email))
            self.web_entry.set_text(_None_to_str(client.web))
            #For debug
            if self.debbuging:
                self.client_id_label.set_visible(True)
            if len(client.address)>0: 
                self.street_entries[0].set_text(_None_to_str(client.address[0].street))
                self.street_number_entries[0].set_text(_None_to_str(str(client.address[0].number)))
                self.city_entries[0].set_text(_None_to_str(client.address[0].city))
                self.state_entries[0].set_text(_None_to_str(client.address[0].state))
                self.country_entries[0].set_text(_None_to_str(client.address[0].country))
                self.postal_code_entries[0].set_text(_None_to_str(str(client.address[0].postal_code)))
                self.id_address_labels[0].set_text(str(client.address[0].id))
                #For debug
                if self.debbuging:
                    self.id_address_labels[0].set_visible(True)
                #Adding all the others tabs with client.address informatation
                for a in range(1,len(client.address)):
                    self.add_address_tab(client.address[a],a+1)

    def save_apply(self, apply_button):
        if self.entry_changed:
            new_dni = self.dni_entry.get_text().decode('utf-8')
            exist = self.controller.client_exist(new_dni)
            if new_dni=="":
                self.warning_label.set_text("DNI field must be filled")
                self.warning_label.show()
            elif new_dni[0] == "#":
                self.warning_label.set_text("DNI not able to start with #")
                self.warning_label.show()
            elif (self.old_dni != new_dni and exist):
                self.warning_label.set_text("DNI already in the system")
                self.warning_label.show()
            else:
                self.warning_label.hide()
                client = models.Models.Client(self.name_entry.get_text(),
                                          self.surname_entry.get_text(),
                                          new_dni,
                                          self.email_entry.get_text(),
                                          self.web_entry.get_text(),
                                          )
                #if new_dni != self.old_dni or exist:
                if exist:
                    self.controller.to_modify(self.old_dni, client)
                else:
                    self.controller.insert_new_client(client)
                self.controller.refresh_clients_main_view(client, old_dni=self.old_dni)
                self.window.hide()
        else:
            self.window.hide()

    def quit(self, widget):
        self.hide()
    
    def show(self):
        self.window.show()
    
    def hide(self):
        self.window.hide()

    def info(self, message):
        """
            Method to show the _message_ string as user information
        """
        self.notification_label.set_text(message)

    ######## Client management #########
    def client_changed(self, widget_button):
        if self.modified.count("client") == 0:
            self.modified.append("client")
        self.apply_button.set_label("Save")

    ######## Address management #########
    def add_address_tab(self, add, num):
        """
            Method to new address_tab
            num is the tab number
        """
        title = gtk.Label("Address %d" % num)
        new_table = self.address_table(num, add)
        self.address_notebook.insert_page(new_table, title, position=num)

    def address_table(self, tab_num, address=None):
        """
            Method to create an address table customized with tab_number
            if address == None then just create a address_table empty,
            otherwise it creates a new address_table filled up with
            address information
        """
        table = gtk.Table(3,4)
        self.street_entries[tab_num] = gtk.Entry()
        self.street_number_entries[tab_num] = gtk.Entry()
        self.city_entries[tab_num] = gtk.Entry()
        self.state_entries[tab_num] = gtk.Entry()
        self.country_entries[tab_num] = gtk.Entry()
        self.postal_code_entries[tab_num] = gtk.Entry()
        #First column
        table.attach(gtk.Label("Street"),0,1,0,1)
        table.attach(gtk.Label("City"),0,1,1,2)
        table.attach(gtk.Label("Country"),0,1,2,3)
        #Second column
        table.attach(self.street_entries[tab_num],1,2,0,1)
        table.attach(self.city_entries[tab_num],1,2,1,2)
        table.attach(self.country_entries[tab_num],1,2,2,3)
        #third column
        table.attach(gtk.Label("Number"),2,3,0,1)
        table.attach(gtk.Label("State"),2,3,1,2)
        table.attach(gtk.Label("Postal Code"),2,3,2,3)
        #fourth column
        table.attach(self.street_number_entries[tab_num],3,4,0,1)
        table.attach(self.state_entries[tab_num],3,4,1,2)
        table.attach(self.postal_code_entries[tab_num],3,4,2,3)
        #Populate the address table with address information
        if address != None:
            self.street_entries[tab_num].set_text(_None_to_str(address.street))
            self.street_number_entries[tab_num].set_text(_None_to_str(str(address.number)))
            self.city_entries[tab_num].set_text(_None_to_str(address.city))
            self.state_entries[tab_num].set_text(_None_to_str(address.state))
            self.country_entries[tab_num].set_text(_None_to_str(address.country))
            self.postal_code_entries[tab_num].set_text(_None_to_str(str(address.postal_code)))
            self.id_address_labels[tab_num] = gtk.Label(str(address.id))
        #connect the handlers for the address entries
        self.street_entries[tab_num].connect("changed",self.address_changed)
        self.street_number_entries[tab_num].connect("changed",self.address_changed)
        self.city_entries[tab_num].connect("changed",self.address_changed)
        self.state_entries[tab_num].connect("changed",self.address_changed)
        self.country_entries[tab_num].connect("changed",self.address_changed)
        self.postal_code_entries[tab_num].connect("changed",self.address_changed)
        vbox = gtk.VBox()
        vbox.pack_start(table)
        #Just show id if you are debbuging the applicacion
        if self.debbuging:
            vbox.pack_start(self.id_address_labels[tab_num])
        vbox.show_all()
        return vbox

    def address_changed(self, widget_button):
        if self.modified.count("address") == 0:
            self.modified.append("address")
        tab_num = self.address_notebook.get_current_page()
        if self.modified_add.count(tab_num) == 0:
            self.modified_add.append(self.address_notebook.get_current_page())
        self.apply_button.set_label("Save")

    def delete_address(self, widget_button):
        """
            Method to delete the actual selected address
        """
        tab_num = self.address_notebook.get_current_page()

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
