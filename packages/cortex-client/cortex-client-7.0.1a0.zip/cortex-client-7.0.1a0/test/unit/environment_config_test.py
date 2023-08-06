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
import unittest

from mocket.mockhttp import Entry
from mocket import mocketize

from unittest.mock import Mock

from cortex.env import CortexEnv
from cortex.exceptions import BadTokenException


class TestCortexConfiguration(unittest.TestCase):
    def setUp(self):
        self.getCortexTokenOriginal = CortexEnv.getCortexToken
        self.getCortexProfileOriginal = CortexEnv.getCortexProfile

    @mocketize
    def test_get_cortex_token(self):
        token = 'some_token'
        CortexEnv.getCortexToken = Mock(return_value=token)
        self.assertEqual(CortexEnv.getCortexToken(), token)
    @mocketize
    def test_get_cortex_profile(self):
        profile = { "A" : 1, "B": 2 } 
        CortexEnv.getCortexProfile = Mock(return_value=profile)
        self.assertEqual(CortexEnv.getCortexProfile(), profile)
    @mocketize
    def test_permission_error_fail_no_profile_and_no_token(self):
        token = ''
        profile = {}
        CortexEnv.getCortexToken = Mock(return_value=token)
        CortexEnv.getCortexProfile = Mock(return_value=profile)
        self.assertRaises(BadTokenException, CortexEnv)
    # we don't want methods calls to CortexEnv to use the monkey patched methods
    # so we revert back to the original methods.
    def tearDown(self):
        CortexEnv.getCortexToken = self.getCortexTokenOriginal
        CortexEnv.getCortexProfile = self.getCortexProfileOriginal
