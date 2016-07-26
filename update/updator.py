# Pentakill update module
# 
# Update module contains methods to update
# summoner data, match data and statistics data
#
# How to use is easy
# 1. call init() method to initialize database and LOL API
# 2. call update methods to update data
# 3. call close() method to close db connection and LOL API

from pentakill.lolapi import lolapi
from pentakill.update import lolfastapi
from pentakill.db import connector


# Simple configuration
T_WAIT = 10.0     # timeout for api data

class UpdateModule(object):
    def __init__(self):
        self.db = connector.PentakillDB()
        self.api = lolfastapi.LOLFastAPI()
    
    def init(self):
        self.db.init()
        self.api.start_multiple_get_mode()
        self.api.set_keep_alive(True)
        
    def close(self):
        self.api.close_multiple_get_mode()
        self.db.close()

    def getSummonerUpdator(self):
        return SummonerUpdator(self)
    
    

class SummonerUpdator(object):
    def __init__(self, module):
        self.module = module
        self.api = module.api
        self.db = module.db
        
    # Update summoner data by id or name
    # at least one of two must be not None.
    # If both are not None, id is used to identify summoner
    # name : utf8 encoded string name
    def update(self, id=None, name=None):
        reqs = lolfastapi.FastRequest()
        if id:
            reqs.add_request_name('summoner', (lolapi.LOLAPI.get_summoners_by_ids, (id,)))
        elif name:
            reqs.add_request_name('summoner', (lolapi.LOLAPI.get_summoners_by_names, (name,)))
        else:
            raise InvalidArgumentError("id or name must be given")
        
        respond = self.api.get_multiple_data(reqs)
        respond.wait_response(T_WAIT)
        res = respond.get_response('summoner')
        
    
'''
errno
'''
E_UNKNOWN = 0
E_INVALID_ARG_ERROR = 1
E_PYTHON_ERROR = 2
    
class Error(Exception):
    def __init__(self, msg, errno=None):
        self.msg = msg
        self.errno = errno or -1
        
    def __str__(self):
        return self.msg + " (" + str(self.errno) + ")"
    
class InvalidArgumentError(Error):
    def __init__(self, msg):
            Error.__init__(self, msg, E_INVALID_ARG_ERROR)
            
class PythonBuiltInError(Error):
    def __init__(self, msg):
        Error.__init__(self, msg, E_PYTHON_ERROR)
        

if __name__ == '__main__':
    print 'test update'
    module = UpdateModule()
    module.init()
    module.close()
    