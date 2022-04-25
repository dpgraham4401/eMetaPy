import json
import logging
import os
import urllib.parse
import requests
from datetime import datetime, timedelta


def post(endpoint, data) -> requests.Response:
    meta_head = {'Content-Type': 'application/json'}
    resp = requests.post(endpoint, data=data, headers=meta_head)
    if not resp.ok:
        logging.error(resp.json())
    return resp


def parse_params(parameters):
    """convert query parameters to payload"""
    # ToDo: remove url encoded hardcode so can handle multiple parameters
    if parameters is None:
        return ""
    else:
        parameter_string = ""
        for index, i in enumerate(parameters):
            partial_param_string = '{"type":"category","target":["variable",["template-tag","{0}"]],"value":"{1}"}'
            partial_param_string = partial_param_string.replace(
                '{0}', i).replace('{1}', parameters[i])
            if index > 0:
                partial_param_string = "," + partial_param_string
            parameter_string = parameter_string + partial_param_string
        parameter_string = "[" + parameter_string + "]"
        url_encoded = urllib.parse.quote(parameter_string)
        return "?parameters=" + url_encoded


class MetaClient:
    def __init__(self, base_url=None):
        if not base_url:
            self.base_url = 'https://rcraquery.epa.gov/metabase/'
        self.config_path = None
        self.token = None
        self.expiration = None
        self.username = None
        self.password = None
        self.u_and_p_env = None

    def user_password_env_set(self):
        if os.getenv('META_USER') and os.getenv('META_PASSWORD'):
            self.u_and_p_env = True
        else:
            self.u_and_p_env = False

    def load_config_file(self, path=None):
        if path:
            self.config_path = path
        if self.config_path:
            with open(self.config_path, 'rt') as env_file:
                lines = env_file.read().splitlines()
            for line in lines:
                name, value = line.partition('=')[::2]
                if name == 'META_TOKEN':
                    self.token = value
                elif name == 'META_EXPIRATION':
                    self.expiration = value
                elif name == 'META_USER':
                    self.username = value
                elif name == 'META_PASSWORD':
                    self.password = value
        else:
            logging.error('Pass a config file path or set config_path attribute')

    def save(self, path=None):
        if path:
            self.config_path = path
        if self.config_path:
            data = {'META_TOKEN': self.token,
                    'META_EXPIRATION': str(self.expiration),
                    'META_USER': self.username,
                    'META_PASSWORD': self.password}
            with open(self.config_path, 'wt') as config_file:
                for key, value in data.items():
                    if value:
                        config_file.writelines([key, '=', value, '\n'])

    def is_token_expired(self):
        current_time = datetime.now().isoformat()
        if current_time < self.expiration:
            return False
        else:
            return True

    def authenticate(self):
        if self.token and self.expiration:
            expired = self.is_token_expired()
            if not expired:
                return True
            else:
                self.__get_token()
        elif self.username and self.password:
            self.__get_token()
        else:
            logging.error('cannot authorize without token and expiration, or username and password')

    def __get_token(self):
        if self.username and self.password:
            data = json.dumps({"username": self.username, "password": self.password})
            auth_url = f'{self.base_url}api/session'
            resp = post(auth_url, data)
            if resp.ok:
                self.expiration = datetime.now() + timedelta(days=12)
                self.token = resp.json()['id']
            else:
                logging.error(f'Received : {resp.status_code}')
        else:
            logging.error(f'Cannot Authenticate without username and password')

    def get_query(self, card_id, response_format='json', parameters=None):
        """
        Request query (card) options

        Args:
            card_id (str): Metabase query ID number in string format
            response_format (str): "json" or "csv"
            parameters (dict): dictionary with key values corresponding to metabase variable names
        """
        url_parameters = parse_params(parameters)
        endpoint = self.base_url + '/api/card/' + str(card_id) + '/query/' + response_format + url_parameters
        meta_head = {'Content-Type': 'application/json',
                     'X-Metabase-Session': self.token}
        resp = requests.post(endpoint, headers=meta_head)
        if resp.ok:
            return resp
        else:
            logging.error(f'Problem retrieving query {card_id}')
            return resp
