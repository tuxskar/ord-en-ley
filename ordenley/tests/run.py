'''
Created on Dec 4, 2012

@author: tuxskar
'''
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:  
    import pygtk  
    pygtk.require("2.0")  
except:  
    pass  
import controllers.controller
import views.main
import views.client
import gtk


def main():
    #To use mysql with user=skar and pass=mypass uncomment next line
    #cont = controllers.controller.Controller(user_name="skar", user_password="mypass")
    cont = controllers.controller.Controller()
    cont.insert_test_clients()
    main_view = views.main.main_view(cont)
    cont.connect_main_view(main_view)
    cont.init_main()
    gtk.main()

if __name__ == '__main__':
    main()
