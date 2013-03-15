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
        self.street_entry = self.builder.get_object("street_entry")
        self.street_number_entry = self.builder.get_object("street_number_entry")
        self.city_entry = self.builder.get_object("city_entry")
        self.state_entry = self.builder.get_object("state_entry")
        self.country_entry = self.builder.get_object("country_entry")
        self.postal_code_entry = self.builder.get_object("postal_code_entry")
        self.id_label = self.builder.get_object("id_label")
        if self.debbuging:
            #For debug
            self.id_label.set_visible(True)
        
        dic = {
            "on_client_info_destroy" : self.quit,
            "on_cancel_clicked" : self.quit,
            "client_entry_changed" : self.entry_changed,
            "on_apply_clicked" : self.save_apply,
              }

        self.window.set_title(title)
        self.client = client
        if self.client!=None:
            self.client_id_label.set_text(_None_to_str(str(client.id)))
            self.name_entry.set_text(_None_to_str(client.name))
            self.surname_entry.set_text(_None_to_str(client.surname))
            self.dni_entry.set_text(_None_to_str(client.dni))
            self.email_entry.set_text(_None_to_str(client.email))
            self.web_entry.set_text(_None_to_str(client.web))
            #TODO show the first address, and then create a new notebook tab for each aditional address to show all address stored in client
            if client.address != []:
                self.street_entry.set_text(_None_to_str(client.address[0].street))
                self.street_number_entry.set_text(_None_to_str(str(client.address[0].number)))
                self.city_entry.set_text(_None_to_str(client.address[0].city))
                self.state_entry.set_text(_None_to_str(client.address[0].state))
                self.country_entry.set_text(_None_to_str(client.address[0].country))
                self.postal_code_entry.set_text(_None_to_str(str(client.address[0].postal_code)))
                self.id_label.set_text(str(client.address[0].id))
        self.builder.connect_signals(dic)
        self.modified = [] # Store what kind of object has been modified
        self.new_address = [] # For address added
        self.deleted_address = [] # For address deleted
    
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
        
    def entry_changed(self, widget):
        self.entry_changed = True
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
