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

debbuging = True
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
        if debbuging:
            #For debug
            self.client_id_label.set_visible(True)

        ######## address 1 variables #########
        #to manage the address notebook it create a list of address_view objects
        #with the same index of the notebook page index
        #If the client doesn't have any address its insert in the page 0 an empty
        #address table as an address_view object without filled up
        self.address_pages = []
        self.address_notebook = self.builder.get_object("address_notebook")
        
        dic = {
            "on_client_info_destroy" : self.quit,
            "on_cancel_clicked" : self.quit,
            "client_entry_changed" : self.client_changed,
            "address_entry_changed" : self.address_changed,
            "on_delete_address" : self.delete_address,
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
            if debbuging:
                self.client_id_label.set_visible(True)
            #first it removes the sample page, then it insert all address
            #that has the client
            self.address_notebook.remove_page(0)
            if len(client.address)>0: 
                for add in client.address:
                    i = client.address.index(add)
                    title = gtk.Label("Address %s" % str(i+1))
                    add_v = Address_view(self,add,i)
                    self.address_notebook.insert_page(add_v.pack,title, i)
                    self.address_pages.append(add_v)
            else:
                #insert an empty table
                title = gtk.Label("Address 1")
                add_v = Address_view(None,0)
                self.address_notebook.insert_page(add_v.pack,title, 0)
                self.address_pages.append(add_v)

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
            if add is None just insert a new empty table
        """
        title = gtk.Label("Address %s" % str(num+1))
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
        else:
            self.id_address_labels[tab_num] = gtk.Label(str(-1))
        #connect the handlers for the address entries
        self.street_entries[tab_num]
        self.street_number_entries[tab_num].connect("changed",self.address_changed)
        self.city_entries[tab_num].connect("changed",self.address_changed)
        self.state_entries[tab_num].connect("changed",self.address_changed)
        self.country_entries[tab_num].connect("changed",self.address_changed)
        self.postal_code_entries[tab_num].connect("changed",self.address_changed)
        vbox = gtk.VBox()
        vbox.pack_start(table)
        #Just show id if you are debbuging the applicacion
        if debbuging:
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
        print tab_num
        print self.id_address_labels
        if tab_num > -1:
            print tab_num
            address_id = int(self.id_address_labels[tab_num].get_text())
            #check if address_id isn't already in the list
            print address_id
            if self.deleted_address.count(address_id) == 0 and address_id != -1:
                self.deleted_address.append(address_id)
        #substract 1 unit for the greaters numbers in list new_address and modified_add
        for mod in self.modified_add:
            if mod > tab_num:
                self.modified_add[self.modified_add.index(mod)] = mod-1
        for n in self.new_address:
            if n > tab_num:
                self.new_address[self.new_address.index(n)] = n-1
        #update the key in the entries and labels dictionaries
        self.id_address_labels = self.__update_dic_from_n(self.id_address_labels,tab_num)
        self.street_entries        = self.__update_dic_from_n(self.street_entries,tab_num)
        self.street_number_entries = self.__update_dic_from_n(self.street_number_entries,tab_num)
        self.city_entries          = self.__update_dic_from_n(self.city_entries,tab_num)
        self.state_entries         = self.__update_dic_from_n(self.state_entries,tab_num)
        self.country_entries       = self.__update_dic_from_n(self.country_entries,tab_num)
        self.postal_code_entries   = self.__update_dic_from_n(self.postal_code_entries,tab_num)
        print self.id_address_labels
        if self.address_notebook.get_n_pages() == 1:
            self.address_notebook.remove_page(tab_num)
            self.add_address_tab(add=None, num=0)
            self.info("There is no more address to delete")
        else:
            self.address_notebook.remove_page(tab_num)
            self.info("Deleted address %s" % str(tab_num+1))
        print self.deleted_address 
    
    def __update_dic_from_n(self, dic, n):
        """
            Method to substrac 1 unit to every key in the dictionary _dic_
            after n
        """
        def f(mydict):
            return dict((k-1,f(v) if hasattr(v,'keys') else v) for k,v in mydict.items() if k > n)
        dic.pop(n)
        dic = f(dic)
        return dic

class Address_view(object):
    """
        This object repressent an address in some view
        Its store the entries, labels, page number and id of the 
        address normal object plus all the gtk object associated
    """
    def __init__(self, view, address, page_n=-1):
        self.n_page = page_n
        self.street_entry        = gtk.Entry()
        self.street_number_entry = gtk.Entry()
        self.city_entry          = gtk.Entry()
        self.state_entry         = gtk.Entry()
        self.country_entry       = gtk.Entry()
        self.postal_code_entry   = gtk.Entry()
        self.id_address_label    = gtk.Label("-1")
        self.street_label        = gtk.Label("Street")
        self.street_number_label = gtk.Label("City")
        self.city_label          = gtk.Label("Country")
        self.state_label         = gtk.Label("Number")
        self.country_label       = gtk.Label("State")
        self.postal_code_label   = gtk.Label("Postal Code")
        self.pack = self.create_pack(address)
        #connecting signals to entry objects
        self.street_entry.connect("changed",view.address_changed)
        self.street_number_entry.connect("changed",view.address_changed)
        self.city_entry.connect("changed",view.address_changed)
        self.state_entry.connect("changed",view.address_changed)
        self.country_entry.connect("changed",view.address_changed)
        self.postal_code_entry.connect("changed",view.address_changed)

    def create_pack(self, address=None):
        """
            This method creates a pack with an address table
            and inside a horizontal box and label id as end of 
            VBox
            If address is None create a empty pack, otherwise
            it creates an pack filled up with it
        """
        table = gtk.Table(3,4)
        #First column
        table.attach(self.street_label,0,1,0,1)
        table.attach(self.city_label,0,1,1,2)
        table.attach(self.country_label,0,1,2,3)
        #Second column
        table.attach(self.street_entry,1,2,0,1)
        table.attach(self.city_entry,1,2,1,2)
        table.attach(self.country_entry,1,2,2,3)
        #third column
        table.attach(self.street_number_label,2,3,0,1)
        table.attach(self.state_label,2,3,1,2)
        table.attach(self.postal_code_label,2,3,2,3)
        #fourth column
        table.attach(self.street_number_entry,3,4,0,1)
        table.attach(self.state_entry,3,4,1,2)
        table.attach(self.postal_code_entry,3,4,2,3)
        vbox = gtk.VBox()
        vbox.pack_start(table)
        vbox.pack_start(self.id_address_label)
        if address != None:
            self.street_entry.set_text(_None_to_str(address.street))
            self.street_number_entry.set_text(_None_to_str(str(address.number)))
            self.city_entry.set_text(_None_to_str(address.city))
            self.state_entry.set_text(_None_to_str(address.state))
            self.country_entry.set_text(_None_to_str(address.country))
            self.postal_code_entry.set_text(_None_to_str(str(address.postal_code)))
            self.id_address_label.set_text(str(address.id))
        vbox.show_all()
        if not debbuging:
            self.id_address_label.hidde()
        return vbox

        

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
