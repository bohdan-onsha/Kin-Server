import pyrebase

from configuration import config


"""
user - firebase uid,  email, password hash, public wallet address,  recovery string

transactions - from uid, to uid, count, description, date etc.

"""

firebase = pyrebase.initialize_app(config)


auth = firebase.auth()
db = firebase.database()
db_store = db.child('store1')


def register(email, pwd):
    pass

    '''
        -> uid, email, public wallet address, recovery string
    '''

def auth(uid):
    pass

    '''
    -> public wallet address, recovery string
    '''

def get_kins(uid, count, description):
    pass

    '''
    
    '''
def get_wallet(uid):
    pass

    '''
    -> public wallet address
    
    '''

def histiry(uid):
    pass

    '''
    -> transactions list (descr, count, status(bool))
    '''