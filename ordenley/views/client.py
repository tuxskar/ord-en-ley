'''
Created on Nov 17, 2012

@author: tuxskar
'''
import sys
import glib
import tests

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

import models.Models
import db.db_manager
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
        if tests.debbuging:
            #For debug
            self.client_id_label.set_visible(True)

        ######## address 1 variables #########
        #to manage the address notebook it create a list of address_view objects
        #with the same index of the notebook page index
        #If the client doesn't have any address its insert in the page 0 an empty
        #address table as an address_view object without filled up
        self.address_pages = []
        self.address_notebook = self.builder.get_object("address_notebook")
        self.modified = [] # Store what kind of object has been modified either client, or address
        self.to_modify_add = [] # Store the tab_number of the modified address
        self.to_new_add = [] # For address added
        self.to_delete_add = [] # For address deleted
        self.has_new_add = -1 # n_page of the new_address
        
        dic = {
            "on_client_info_destroy" : self.quit,
            "on_cancel_clicked" : self.cancel,
            "client_entry_changed" : self.client_changed,
            "address_entry_changed" : self.address_changed,
            "on_new_address_clicked" : self.new_address,
            "on_delete_address" : self.delete_address,
            "on_apply_clicked" : self.save_apply,
              }

        self.window.set_title(title)
        self.client = client
        self.populate_client_view(client)
        self.builder.connect_signals(dic)

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
            if tests.debbuging:
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
        if self.client == None or len(client.address)==0:
            self.address_notebook.remove_page(0)
            #insert an empty table
            title = gtk.Label("Address 1")
            add_v = Address_view(self,None,0)
            self.address_notebook.insert_page(add_v.pack,title, 0)
            self.address_pages.append(add_v)
            self.has_new_add = 0 

    def save_apply(self, apply_button):
        """
            Method to save all the changes done on the view
        """
        #modify every change made in the view to close it 
        if "address" in self.modified:
            if tests.debbuging:
                print "to_modify "
                print self.to_modify_add
                print "to_new_add "
                print self.to_new_add
                print "to_delete_add "
                print self.to_delete_add
            #to add new address
            for n in self.to_new_add:
                a = self.get_address_from_page(n)
                a.clients.append(self.client)
                self.controller.client_returned_values("address","new",a,None)
            for mod in self.to_modify_add:
                a = self.get_address_from_page_with_id(mod)
                self.controller.client_returned_values("address","modified",a,mod)
            for d in self.to_delete_add:
                self.controller.client_returned_values("address","delete",None, d)
        if "client" in self.modified:
            c = self.get_client_from_view()
            if c.id != -1:
                self.controller.client_returned_values("client","modified",c,c.id)
            else:
                self.controller.client_returned_values("client","new",c,None)
        self.cancel(None)

    def get_address_from_page(self, n):
        """
            Method to return the address in the page n
        """
        return self.from_add_v_to_add(self.address_pages[n])

    def get_address_from_page_with_id(self, add_id):
        """
            Method to return an address using add_id to find it
        """
        for add_v in self.address_pages:
            if add_v.add_id == add_id:
                return self.from_add_v_to_add(add_v)

    def from_add_v_to_add(self, add_v):
            id = add_v.add_id
            street      = add_v.street_entry.get_text()
            #number      = int(add_v.street_number_entry.get_text())
            number      = add_v.street_number_entry.get_text()
            city        = add_v.city_entry.get_text()
            state       = add_v.state_entry.get_text()
            country     = add_v.country_entry.get_text()
            #postal_code = int(add_v.postal_code_entry.get_text()) 
            postal_code = add_v.postal_code_entry.get_text()
            return models.Models.Address(street,number, city,state,country,postal_code,id)
        
    def get_client_from_view(self):
        """
            Mehtod to return a client from this view
        """
        id = int(self.client_id_label.get_text())
        name    = self.name_entry.get_text()
        surname = self.surname_entry.get_text()
        dni     = self.dni_entry.get_text()
        email   = self.email_entry.get_text()
        web     = self.web_entry.get_text()
        return models.Models.Client(name, surname, dni,email,web, id=id)







        #if self.client == None:
            #self.cancel(None)
        #else:
            #if self.modified_add.count("address") > 0:
                #for to_del in self.deleted_address:
                    #self.controller.client_returned_values("client","delete",None,self.deleted_address[to_del])
                ##for to_add in self.new_address:


            

        #if self.entry_changed#
            #new_dni = self.dni_entry.get_text().decode('utf-8')
            #exist = self.controller.client_exist(new_dni)
            #if new_dni=="":
                #self.warning_label.set_text("DNI field must be filled")
                #self.warning_label.show()
            #elif new_dni[0] == "#":
                #self.warning_label.set_text("DNI not able to start with #")
                #self.warning_label.show()
            #elif (self.old_dni != new_dni and exist):
                #self.warning_label.set_text("DNI already in the system")
                #self.warning_label.show()
            #else:
                #self.warning_label.hide()
                #client = models.Models.Client(self.name_entry.get_text(),
                                          #self.surname_entry.get_text(),
                                          #new_dni,
                                          #self.email_entry.get_text(),
                                          #self.web_entry.get_text(),
                                          #)
                ##if new_dni != self.old_dni or exist:
                #if exist:
                    #self.controller.to_modify(self.old_dni, client)
                #else:
                    #self.controller.insert_new_client(client)
                #self.controller.refresh_clients_main_view(client, old_dni=self.old_dni)
                #self.window.hide()
        #else:
            #self.window.hide()

    def cancel(self, widget):
        """
            Method to handle on cancel button clicked
        """
        self.address_pages = []
        self.modified      = []
        self.to_modify_add = []
        self.to_new_add    = []
        self.to_delete_add = []
        self.quit(widget)

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
        self.notification_label.show()

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
        add_v = Address_view(self,add,num)
        title = gtk.Label("Address %s" % str(num+1))
        self.address_notebook.insert_page(add_v.pack, title, position=num)
        return add_v

    def address_changed(self, widget_button):
        tab_num = self.address_notebook.get_current_page()
        print self.address_pages
        add_id = self.address_pages[tab_num].add_id
        if add_id == -1 and tab_num == self.has_new_add:
            #empty address changed 
            self.to_new_add.append(tab_num)
            self.has_new_add = -1
        elif add_id == -1:
            #already as in to_new_add list
            return None
        else:
            #already stored address to modify
            if not (add_id in self.to_modify_add):
                self.to_modify_add.append(add_id)
        if not("address" in self.modified):
            self.modified.append("address")
        self.apply_button.set_label("Save")

    def new_address(self, widget_button):
        """
            Method to handle the signal of on_new_address_button_clicked
        """
        if self.has_new_add != -1:
            self.info("Already empty address number %d to be added" % self.has_new_add)
            return None
        else:
            n_pages = self.address_notebook.get_n_pages()
            #self.to_new_add.append(n_pages)
            add_v = self.add_address_tab(add=None, num=n_pages)
            current = self.address_notebook.get_current_page()
            #get focus on the just inserted tab
            for pages in range(0,n_pages-current):
                self.address_notebook.next_page()
            self.info("New tab Address %s"%str(n_pages+1))
            self.address_pages.append(add_v)
            self.has_new_add = n_pages

    def delete_address(self, widget_button):
        """
            Method to delete the actual selected address
        """
        # if add_id != -1 the address is already in the system
        tab_num = self.address_notebook.get_current_page()
        add_id = self.address_pages[tab_num].add_id
        total_pages = self.address_notebook.get_n_pages()
        if add_id != -1:
            if total_pages > 1:
                if self.has_new_add == tab_num:
                    self.has_new_add = -1
                self.update_to_new_add_list(tab_num)
            else:
                self.address_notebook.remove_page(tab_num)
                self.address_pages.pop(tab_num)
                add_v = Address_view(self,address=None,page_n=0)
                self.address_pages.append(add_v)
                title = gtk.Label("Address 1")
                self.address_notebook.insert_page(add_v.pack,title, 0)
                self.info("No address to be deleted")
                return None
        else:
            if add_id in self.to_modify_add:
                self.to_modify_add.pop(add_id)
        self.to_delete_add.append(add_id)
        self.address_pages.pop(tab_num)
        self.address_notebook.remove_page(tab_num)
        self.update_address_labels(tab_num)
        if not ("address" in self.modified):
            self.modified.append("address")
        self.info("Deleted address %s" % str(tab_num+1))
    
    def update_to_new_add_list(self, tab_num):
        """
            Method to update the index of the list to_new_add
        """
        if len(self.to_new_add) > 0:
            self.to_new_add.remove(tab_num)
            self.to_new_add = [a-1 if a>tab_num else a for a in self.to_new_add]

    def update_address_labels(self, tab_num):
        """
            Update the address <num> tab title for all the tab greaters 
            than tab_num
        """
        n_pages = self.address_notebook.get_n_pages()
        for page in range(tab_num,n_pages):
            self.address_notebook.set_tab_label_text(self.address_pages[page].pack,"Address %s" % str(page+1))

class Address_view(object):
    """
        This object repressent an address in some view
        Its store the entries, labels, page number and id of the 
        address normal object plus all the gtk object associated
    """
    def __init__(self, view, address, page_n=-1):
        self.add_id = -1
        self.street_entry        = gtk.Entry()
        self.street_number_entry = gtk.Entry()
        self.city_entry          = gtk.Entry()
        self.state_entry         = gtk.Entry()
        self.country_entry       = gtk.Entry()
        self.postal_code_entry   = gtk.Entry()
        self.id_address_label    = gtk.Label("-1")
        self.street_label        = gtk.Label("Street")
        self.street_number_label = gtk.Label("Number")
        self.city_label          = gtk.Label("City")
        self.state_label         = gtk.Label("State")
        self.country_label       = gtk.Label("Country")
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
            self.add_id = address.id
            self.street_entry.set_text(_None_to_str(address.street))
            self.street_number_entry.set_text(_None_to_str(address.number))
            self.city_entry.set_text(_None_to_str(address.city))
            self.state_entry.set_text(_None_to_str(address.state))
            self.country_entry.set_text(_None_to_str(address.country))
            self.postal_code_entry.set_text(_None_to_str(address.postal_code))
            self.id_address_label.set_text(str(address.id))
        vbox.show_all()
        if not tests.debbuging:
            self.id_address_label.hide()
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
