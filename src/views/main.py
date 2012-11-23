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
    import gtk.glade  
except:  
    print("GTK Not Availible")
    sys.exit(1)

class main_view(object):
    '''
    This is the main view that represent the whole application dashboard
    '''
#    wTree = None

    def __init__(self):
        '''
        Build the main dashboard view using the main_view.glade file 
        located in interfaces
        '''
        self.filename = "../interfaces/main_view.glade"
        self.main_window_name = "main_view"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.filename)
        
        self.window = self.builder.get_object(self.main_window_name)
        
        dic = {
        "on_main_view_destroy" : self.quit,
               }
        self.builder.connect_signals(dic)
        
        
    def quit(self, widget):
        sys.exit(0)

if __name__ == '__main__':
    gui = main_view()
    gui.window.show()
    gtk.main()
