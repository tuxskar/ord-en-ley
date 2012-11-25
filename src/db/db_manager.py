'''
Created on Nov 17, 2012

@author: skar
'''
from models import Models

class db_manager(object):
    '''
    This module is the layer between physical DB to controller
    '''

    def __init__(self, user_name = None, user_password=None, session = None):
        '''
        This constructor has at least a session object to start petitions agains 
        '''
        if session != None:
            self.session = session
        elif user_name != None and user_password != None:
            self.session = Models.get_session(user_name, user_password)
        else:
            self.session = Models.get_session()
        
    def get_all_clients(self):
        return self.session.query(Models.Client).all()
    
    def get_client(self, dni):
        return self.session.query(Models.Client).filter(Models.Client.dni==dni).one()

if __name__ == '__main__':
    dbman = db_manager()
    print dbman.get_all_clients()