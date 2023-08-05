"""
@author : puranjan

Keto Client PROPERTIES

"""
import json
import logging
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError

class NoCheck():
    def __init__(self):
        self.log = logging.getLogger("KETO-CLIENT")

    def checkAccess(self, userId=None, resourceId=None, action=None):

        return True

class CheckAllowed():
    def __init__(self, baseUrl):
        self.log = logging.getLogger("KETO-CLIENT")
        self.baseUrl = baseUrl

    def checkAccess(self, userId, resourceId, action):

        payload = {
                "action": action,
                "subject":'global::users::%s' %(userId),
                "resource": resourceId
            }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = '%s/engines/acp/ory/regex/allowed' % (self.baseUrl)
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            if response.status_code == 200:
                if json.loads(response.content.decode())['allowed']:
                   return True
            else :
                self.log.error('Error While calling ' + str(response.status_code))

        except ConnectionError as err:
            self.log.error(err)

        return False


