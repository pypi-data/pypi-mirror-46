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
import os
from cortex_client.utils import get_cortex_profile
from cortex.exceptions import BadTokenException

DEFAULT_API_ENDPOINT = 'https://api.cortex.insights.ai'

class CortexEnv:
    """
    gets the configured profile from the local machine
    """
    @staticmethod
    def getCortexProfile():
        return get_cortex_profile()

    """
    gets the cortex token from the local machine
    """
    @staticmethod
    def getCortexToken():
        return os.getenv('CORTEX_TOKEN')

    """
    Sets environment variables for Cortex.
    """
    def __init__(self):
        profile = CortexEnv.getCortexProfile()
        cortexToken = CortexEnv.getCortexToken() or profile.get('token')

        if not cortexToken:
            raise BadTokenException('Your Cortex credentials cannot be retrieved. Refer to https://docs.cortex-dev.insights.ai/docs/cortex-tools/access/ for more information.')

        self.api_endpoint = os.getenv('CORTEX_URI', profile.get('url'))
        self.token = cortexToken
        self.account = os.getenv('CORTEX_ACCOUNT', profile.get('account'))
        self.username = os.getenv('CORTEX_USERNAME', profile.get('username'))
        self.password = os.getenv('CORTEX_PASSWORD')
