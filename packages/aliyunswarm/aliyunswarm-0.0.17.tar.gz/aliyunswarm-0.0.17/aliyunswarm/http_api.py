import json
import requests
from .config import *
from .common import *

class HttpApi():
    def __init__(self, swarm_url, ca_pem, cert_pem, key_pem):
        self.swarm_url=swarm_url
        self.ca_pem=ca_pem
        self.cert_pem=cert_pem
        self.key_pem=key_pem

    @auto_retry()
    def send_get_request(self, path, params=None):
        require_path = self.swarm_url + path
        res = requests.get(require_path,
                        params=params,
                        verify=self.ca_pem,
                        cert=(self.cert_pem, self.key_pem))
        return res.status_code, res.text

    @auto_retry()
    def send_post_request(self, path, headers=None, params=None, data=None):
        require_path = self.swarm_url + path
        res = requests.post(require_path,
                            headers=headers,
                            params=params,
                            data=json.dumps(data),
                            verify=self.ca_pem,
                            cert=(self.cert_pem, self.key_pem))
        return res.status_code, res.text

    @auto_retry()
    def send_delete_request(self, path, headers=None, data=None):
        require_path = self.swarm_url + path
        res = requests.delete(require_path,
                            headers=headers,
                            data=json.dumps(data),
                            verify=self.ca_pem,
                            cert=(self.cert_pem, self.key_pem))
        return res.status_code, res.text
