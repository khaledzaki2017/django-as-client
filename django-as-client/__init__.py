import httplib
import socket
from django.conf import settings
from django.utils import simplejson as json



class AnnounceClient(object):
   
    def __init__(self):
        self.base_url = getattr(settings, 'ANNOUNCE_API', 'localhost:6000')

    def make_requist(self, method, path):
        
        try:
            con = httplib.HTTPConnection(self.base_url)
            con.request(method, path)
            return con.getresponse()
        except (httplib.HTTPException, socket.error):
            return None

    def get_token(self, user_id):
        
        # for a given user ID, return a token.
        
        path = '/auth/token/%s' % (user_id)
        response = self.make_requist('POST', path)
        if not response:
            return None
        try:
            resp = json.loads(response.read())
        except ValueError:
            return None
        if resp:
            if 'token' in resp:
                return '%s|%s' % (user_id, resp['token'])
        return None

    

    def broadcast(self, channel, data):
        
        #emit the given message to all connected users.
        
        path = '/emit/broadcast/%s' % (channel)
        headers = {'Content-Type' : 'application/json'}
        data = json.dumps(data)
        response = self.make_requist('POST', path, data, headers)
        response.read()

    

