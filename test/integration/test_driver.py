#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright (c) 2002-2018 "Neo Technology,"
# Network Engine for Objects in Lund AB [http://neotechnology.com]
#
# This file is part of Neo4j.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from neo4j.v1 import GraphDatabase, ServiceUnavailable
from neo4j.exceptions import ProtocolError
from test.integration.tools import IntegrationTestCase


class DriverTestCase(IntegrationTestCase):

    def test_must_use_valid_url_scheme(self):
        with self.assertRaises(ProtocolError):
            GraphDatabase.driver("x://xxx", auth=self.auth_token)

    def test_connections_are_reused(self):
        with GraphDatabase.driver(self.bolt_uri, auth=self.auth_token) as driver:
            session_1 = driver.session()
            connection_1 = session_1._connection
            session_1.close()
            session_2 = driver.session()
            connection_2 = session_2._connection
            session_2.close()
            assert connection_1 is connection_2

    def test_fail_nicely_when_using_http_port(self):
        uri = "bolt://localhost:7474"
        with self.assertRaises(ServiceUnavailable):
            with GraphDatabase.driver(uri, auth=self.auth_token, encrypted=False):
                pass
