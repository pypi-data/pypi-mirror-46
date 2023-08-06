# -*- coding: utf-8 -*-

"""Main Module"""

import json
import logging
import re

import requests

_DEFAULT_API_URL_ = 'https://api.remot3.it/apv/v27/'


class Remot3(object):
    """Implements the remot3.it  API calls

    Args:
        user (str): account user
        password (str): account secret password
        developerkey (str): account secret developer key
        apiurl (str): API url and version

    Params:
        token (str): session token

    """

    def __init__(self,
                 developerkey,
                 user,
                 password,
                 apiurl=_DEFAULT_API_URL_):

        self.user = user
        self.password = password
        self.developerkey = developerkey
        self.apiurl = apiurl
        self.token = None

    def get_apiurl(self):
        """Returns the API url and version
        """
        return self.apiurl

    def get_token(self):
        return self.token

    def login(self,
              resource='/user/login' ):
        """Implements login api

        Args:
        - resource (str): Overrides API resource (suburl)

        Returns:
        - status (bool): whether the call returned successfully and the response is valid
        - token (str): a valid connection token or None
        - response_body (dict): the full response JSON object
        """

        headers = {
            "developerkey": self.developerkey
        }

        body = {
            "password": self.password,
            "username": self.user
        }
        url = self.apiurl + resource

        try:
            token = None
            response = requests.post(
                url, data=json.dumps(body), headers=headers)
            response_body = response.json()
            status = (response.status_code == 200)\
                and (response_body['status'] == 'true')

            if status:
                token = response_body['token']
                self.token = token
            return status, token, response_body
        except Exception:
            logging.exception('API login failed')

    def list_devices(self, resource='/device/list/all',
                     token=None):
        """Implements the device/list API call
        Args:
            resource (str): API resource
            token (str): Optional token to be used instead of self.token
            headers (dict): Optional JSON object overriding the request header

        .. Note: requires a valid session token

        Returns:
            - status (bool): whether the call returned successfully and the response is valid
            - devices (list): a list of devices
            - response_body (dict): the full response JSON object
        """

        if token is None:
            # Login to retrieve token
            token = self.token

        if token is None:
            raise Exception(
                'Session token is not defined. login() must be called first')

        headers = {
            "developerkey": self.developerkey,
            "token": token
        }
        try:
            url = self.apiurl + resource
            response = requests.get(url, headers=headers)
            response_body = response.json()
            status = (response.status_code == 200)\
                and (response_body['status'] == 'true')

            if status:
                devices = response_body['devices']
            else:
                devices = []
            return status, devices, response_body
        except Exception:
            logging.exception('API call device/list failed')

    def parse_server_name(self, servername, regEx=None):
        """Parses a server name

        Args:
            servername (str): string containing the server name
            regEx (str): an optional,  custom regEx can be passed

        Returns:
            The filtered server name if a match is found or the 
            same string otherwise
        """

        if regEx is None:
            reg = r".*=*(?P<server>proxy\S*).*"
        else:
            reg = regEx

        rmatch = re.match(reg, servername)
        if rmatch:
            servername = rmatch.groups()[0]

        return servername

    def get_server_name(self, 
                        deviceAddr,
                        resource='/device/connect',
                        token=None):
        """Implemented the connect to a device API call

        Args:
        - deviceAddres (str): the device address of the selected installation
        - token (str): Optional token to be used instead of self.token

        Returns:
            - status (bool): whether the call returned successfully and the
              response is valid
            - proxyserver (str): the connection sever name if any,
              otherwise None
            - proxyserver (str): the connection port number if any, 
              otherwise None
            - response_body (dict): the full response JSON object
        """

        if token is None:
            token = self.token

        if token is None:
            raise Exception(
                'Session token is not defined. login() must be called first')

        headers = {
            "developerkey": self.developerkey,
            "token": self.token
        }

        body = {
            "deviceaddress": deviceAddr
        }

        try:
            proxyserver, proxyport = None, None
            url = self.apiurl + resource
            response = requests.post(
                url, data=json.dumps(body), headers=headers)

            response_body = response.json()
            status = (response.status_code == 200)\
                and (response_body['status'] == 'true')

            if status:
                proxyport = response_body['connection']['proxyport']
                proxyserver = response_body['connection']['proxyserver']
                proxyserver = self.parse_server_name(proxyserver)
             
            return status, proxyserver, proxyport, response_body
        except Exception:
            logging.exception('API call /device/connect failed')

    def get_device_address(self, deviceName, serviceType=None):
        """Maps a device name to a device address

        Args:
        - deviceName (str): 
        - serviceType (str): the service type, e.g. SSH

        Returns:
        - deviceAddress(list): a list of matching device addresses
        """

        status, devices, _ = self.list_devices()

        if status:
            addresses = []
            for d in devices:
                if deviceName in d['devicealias']:
                    if serviceType is None:
                        addresses.append(d['deviceaddress'])
                    else:
                        if serviceType == d['servicetitle']:
                            addresses.append(d['deviceaddress'])
        return addresses
