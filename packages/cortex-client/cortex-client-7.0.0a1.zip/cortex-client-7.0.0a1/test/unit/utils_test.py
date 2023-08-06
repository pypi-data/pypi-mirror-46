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

from cortex.utils import decodeJWT
from cortex.exceptions import BadTokenException

from .fixtures import john_doe_token


class TestUtils(unittest.TestCase):
    # decodeJWT tests
    @mocketize
    def test_can_decode_token(self):
        decodedJWT = decodeJWT(john_doe_token(), verify=False)
        self.assertEqual(
            decodedJWT,
            {
            "sub": "1234567890",
            "name": "John Doe",
            "iat": 1516239022,
            "tenant": "Acme Inc."
            }
        )
    @mocketize
    def test_bad_token_throws(self):
        with self.assertRaisesRegexp(BadTokenException, 'Your Cortex Token is invalid.  Refer to https://docs.cortex-dev.insights.ai/docs/cortex-tools/access/ for more information.'):
            decodeJWT('nonsensicaltoken', verify=False)
