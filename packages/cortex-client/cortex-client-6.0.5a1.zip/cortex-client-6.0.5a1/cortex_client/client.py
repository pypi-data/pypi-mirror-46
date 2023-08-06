"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
from typing import Dict
from urllib.parse import urlparse

import requests

from .authenticationclient import AuthenticationClient
from .serviceconnector import ServiceConnector
from .types import InputMessage, JSONType
from .utils import get_logger

log = get_logger(__name__)

class _Client:
    """
    A client.
    """

    URIs = {} # type: Dict[str, str]

    def __init__(self, url, version, token):
        self._serviceconnector = ServiceConnector(url, version, token)

    def _post_json(self, uri, obj: JSONType):
        body_s = json.dumps(obj)
        headers = {'Content-Type': 'application/json'}
        r = self._serviceconnector.request('POST', uri, body_s, headers)
        if r.status_code != requests.codes.ok:
            log.info(r.text)
        r.raise_for_status()
        return r.json()

    def _get_json(self, uri):
        r = self._serviceconnector.request('GET', uri)
        r.raise_for_status()
        return r.json()

    def _request_json(self, uri, method='GET'):
        r = self._serviceconnector.request(method, uri)
        r.raise_for_status()
        return r.json()


def build_client(type, input_message: InputMessage, version):
    """
    Builds a client.
    """
    return type(input_message.api_endpoint, version, input_message.token)
