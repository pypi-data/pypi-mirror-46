#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest import TestCase

from gitlab import Gitlab

from vcr import VCR

import gitlabracadabra.manager
from gitlabracadabra.objects.user import GitLabracadabraUser

my_vcr = VCR(
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query', 'body'],
)


class TestUser(TestCase):
    def setUp(self):
        gitlabracadabra.manager._gitlab = Gitlab(  # noqa: S106
            'http://localhost',
            private_token='DKkdC5JmKWWZgXZGzg83',
        )

    def tearDown(self):
        gitlabracadabra.manager._gitlab = None

    def test_no_create(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/user_no_create.yaml'):
            obj = GitLabracadabraUser('memory', 'no_create_user', {})
            obj.process()

    def test_create(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/user_create.yaml'):
            obj = GitLabracadabraUser('memory', 'create_user', {
                'create_object': True,
                'email': 'create_user@example.org',
                'name': 'Create User',
                'password': 'P@ssw0rdNot24get',
            })
            obj.process()

    def test_exists(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/user_exists.yaml'):
            obj = GitLabracadabraUser('memory', 'user_exists', {})
            obj.process()

    def notest_simple_parameters(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/user_simple_parameters.yaml'):
            obj = GitLabracadabraUser('memory', 'test/user_simple_parameters', {
                'name': 'user-with-simple-parameters',
                'description': 'user with simple parameters',
                'visibility': 'public',
                'lfs_enabled': False,
                'request_access_enabled': True,
                # 'shared_runners_minutes_limit': 42,  # EE, admin-only
            })
            obj.process()

    def test_get_id_from_username(self):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/user_get_id_from_username.yaml'):
            ret = GitLabracadabraUser.get_id_from_username('user_mapping')
            self.assertEqual(ret, 9)

    def test_get_username_from_id(self):
        # Clean up
        GitLabracadabraUser._USERS_USERNAME2ID = {}
        GitLabracadabraUser._USERS_ID2USERNAME = {}
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/user_get_username_from_id.yaml'):
            ret = GitLabracadabraUser.get_username_from_id(9)
            self.assertEqual(ret, 'user_mapping')
