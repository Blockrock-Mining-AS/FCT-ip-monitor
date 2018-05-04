from datetime import datetime

import htmls
import requests
from bs4 import BeautifulSoup

from .response.api import Api


def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

class Node(object):
    def __init__(self, url):
        self._node = 'http://' + url
        self._status = ''
        self._version = ''
        self._git_build = ''
        self._my_height = ''
        self._leader_height = ''
        self._complete_height = ''
        self._node_type = ''
        self._chainID = ''
        self._last_update = None

    def get_response(self):
        api = Api(self._node)
        response = None
        try:
            response = api.get()
            if response and response.status_code == 200:
                self._status = "ONLINE"
        except Exception as e:
            # print(e)
            self._status = "OFFLINE"
        return response

    def refresh(self):
        response = self.get_response()
        if response:
            selector = htmls.S(response.content)
            selector_soup = BeautifulSoup(response.content, 'html.parser')
            selector_soup = remove_attrs(selector_soup)
            self.set_version(selector)
            self.set_git_build(selector_soup)
            self.set_my_height()
            self.set_leader_height()
            self.set_complete_height()
            self.set_node_type()
            self.set_chainID()
            self._last_update = datetime.now()
        else:
            self._version = "n/a"
            self._git_build = "n/a"
            self._my_height = "n/a"
            self._leader_height = "n/a"
            self._complete_height = "n/a"
            self._node_type = "n/a"
            self._chainID = "n/a"
            self._last_update = datetime.now()

    def set_version(self, selector):
        self._version = selector.list('small')[1].text_normalized[1:]

    def set_git_build(self, selector):
        self._git_build = selector.find('h1').find_all('small')[1].get_text()[11:]

    def set_my_height(self):
        try:
            r = requests.get(self._node + '/factomdBatch?batch=myHeight,leaderHeight,completeHeight')
            self._my_height = int(r.json()[0]['Height'])
        except Exception as e:
            # print(e)
            self._my_height = "n/a"

    def set_leader_height(self):
        try:
            r = requests.get(self._node + '/factomdBatch?batch=myHeight,leaderHeight,completeHeight')
            self._leader_height = int(r.json()[1]['Height'])
        except Exception as e:
            # print(e)
            self._leader_height = "n/a"

    def set_complete_height(self):
        try:
            r = requests.get(self._node + '/factomdBatch?batch=myHeight,leaderHeight,completeHeight')
            self._complete_height = int(r.json()[2]['Height'])
        except Exception as e:
            # print(e)
            self._complete_height = "n/a"

    def set_node_type(self):
        try:
            r = requests.get(self._node + '/factomd?item=dataDump')
            dump = r.json()['DataDump1']['RawDump']

            if dump.find('A___') != -1:
                self._node_type = 'Audit'
            elif dump.find('A_I_') != -1:
                self._node_type = 'Audit'
            elif dump.find('A_W_') != -1:
                self._node_type = 'Audit'
            elif dump.find('L___') != -1:
                self._node_type = 'Federated'
            elif dump.find('L_I_') != -1:
                self._node_type = "Federated"
            elif dump.find('L_W_') != -1:
                self._node_type = "Federated"
            else:
                self._node_type = "Follower"
        except Exception as e:
            # print(e)
            self._node_type = "n/a"

    def set_chainID(self):
        try:
            r = requests.get(self._node + '/factomd?item=dataDump')
            dump = r.json()['DataDump4']['MyNode']

            start = r.json()['DataDump4']['MyNode'].find('Identity ChainID: ')
            length = len('Identity ChainID: ')

            self._chainID = dump[start + length: 64 + start + length]
        except Exception as e:
            # print(e)
            self._chainID = "n/a"

    @property
    def node(self):
        return self._node

    @property
    def status(self):
        return self._status

    @property
    def version(self):
        return self._version

    @property
    def git_build(self):
        return self._git_build

    @property
    def sync_status(self):
        if self._my_height != "n/a" and self._complete_height != "n/a":
            return round((int(self._my_height) / int(self._complete_height)) * 100, 2)
        else:
            return "n/a"

    @property
    def my_height(self):
        return self._my_height

    @property
    def leader_height(self):
        return self._leader_height

    @property
    def complete_height(self):
        return self._complete_height

    @property
    def node_type(self):
        return self._node_type

    @property
    def chainID(self):
        return self._chainID

    @property
    def last_update(self):
        return self._last_update


    def print_info(self):
        print(
            """ 
                Node: {}
                Status: {}
                Version: {}
                Git build: {}
                My height: {}
                Sync status (%): {}
                Leader height: {}
                Complete Height: {}
                Node type: {}
                ChainID: {}
                last update: {}
            """.format(self.node,
                       self.status,
                       self.version,
                       self.git_build,
                       self.my_height,
                       self.sync_status,
                       self.leader_height,
                       self.complete_height,
                       self.node_type,
                       self.chainID,
                       self.last_update)
        )

