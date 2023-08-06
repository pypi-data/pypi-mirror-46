from .authenticator import Authenticator
from base64 import b64encode, b64decode
from urllib.parse import urlparse
from functools import lru_cache
import requests
import json


class StackService(Authenticator):
    def __init__(self, service_url, client_key_id, shared_secret, **kwargs):
        self.service_url = service_url
        self.service_token = 'StackService'
        super().__init__(client_key_id, shared_secret, **kwargs)

    @property
    def region(self):
        return(self.get_identity()['region'])

    @property
    def stackname(self):
        return(self.get_identity()['stackname'])

    @lru_cache(maxsize=None)
    def get_identity(self):
        path = '/identity'

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def get_server_status(self):
        path = '/status'

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def webserver_list(self):
        status = self.get_server_status()

        return list(status)

    def get_installation_typo3_configuration(self, installation_name):
        path = '/installation-management/installation/%s/typo3config' % installation_name

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        data = json.loads(r.text)

        decoded_data = {}
        for file_entry, value in data.items():
            decoded_data[file_entry] = b64decode(value).decode('utf-8')

        return(decoded_data)

    def update_installation_typo3_configuration(self, installation_name, local_configuration):
        path = '/installation-management/installation/%s/typo3config' % installation_name
        encoded_localconfiguration = b64encode(local_configuration)

        payload = {}
        payload['LocalConfiguration'] = encoded_localconfiguration

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.put(self.service_url + path, data=payload, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def installations_list(self):
        path = '/installation-management/installations'

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def backup_installation_to_bucket(self, installation, signed_metadata_url, signed_filedata_url, signed_dbdata_url, callback_url):
        path = '/installation-management/installation/%s/backup' % installation
        payload = {'filedata_s3_url': signed_filedata_url, 'manifest_s3_url': signed_metadata_url, 'database_s3_url': signed_dbdata_url, 'callback_url': callback_url}

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.post(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def web_server_status(self):
        path = '/status'
        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def web_server_reload(self):
        path = '/web/reload'
        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.post(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def maintenance_script_list(self):
        path = '/maintenance/list_scripts'
        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))

    def maintenance_script_execute(self, installation_name, context, script):
        path = '/installation-management/installation/%s/execute_script' % (installation_name)

        if not isinstance(script, str):
            raise ValueError('Script argument must be a string')

        if not isinstance(context, dict):
            raise ValueError('Context argument must be a dict')

        payload = {'script': script, 'context': context}
        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.post(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'Authorization': bearer_token})
        return(json.loads(r.text))
