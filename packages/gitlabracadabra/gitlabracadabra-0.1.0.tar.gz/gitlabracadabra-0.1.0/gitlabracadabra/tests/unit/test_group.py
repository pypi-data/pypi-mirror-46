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
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch  # Python 2

from gitlab import Gitlab

from vcr import VCR

import gitlabracadabra.manager
from gitlabracadabra.objects.group import GitLabracadabraGroup

my_vcr = VCR(
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query', 'body'],
)


class TestGroup(TestCase):
    def setUp(self):
        gitlabracadabra.manager._gitlab = Gitlab(  # noqa: S106
            'http://localhost',
            private_token='DKkdC5JmKWWZgXZGzg83',
        )

    def tearDown(self):
        gitlabracadabra.manager._gitlab = None

    def test_no_create(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_no_create.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/no_create_group', {})
            obj.process()

    def test_create(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_create.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/create_group', {'create_object': True})
            obj.process()

    def test_missing_parent(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_missing_parent.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/missing_parent/subgroup', {'create_object': True})
            with patch('gitlabracadabra.objects.object.logger', autospec=True) as logger:
                obj.process()
                logger.error.assert_called_once_with('[%s] NOT Creating %s (%s)',
                                                     'test/missing_parent/subgroup',
                                                     'group',
                                                     'parent namespace not found')

    def test_exists(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_exists.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/group_exists', {})
            obj.process()

    def test_simple_parameters(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_simple_parameters.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/group_simple_parameters', {
                'name': 'group-with-simple-parameters',
                'description': 'Group with simple parameters',
                # 'membership_lock': true,  # EE-only
                # 'share_with_group_lock': true,  # EE-only
                'visibility': 'public',
                # 'file_template_project_id': 12,  # EE-only
                'lfs_enabled': False,
                'request_access_enabled': True,
                # 'shared_runners_minutes_limit': 42,  # EE, admin-only
                # 'extra_shared_runners_minutes_limit': 42,  # EE, admin-only
            })
            obj.process()

    def test_members(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_members.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/group_members', {
                'members': {'some_member': 'developer'},
            })
            obj.process()

    def test_members_change_access_level(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_members_change_access_level.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/group_members', {
                'members': {'some_member': 'maintainer'},
            })
            obj.process()

    def test_members_not_found(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_members_not_found.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/group_members', {
                'members': {'member_not_found': 'maintainer'},
                'unknown_members': 'ignore',
            })
            with patch('gitlabracadabra.mixins.members.logger', autospec=True) as logger:
                obj.process()
                logger.warning.assert_called_once_with('[%s] User not found %s',
                                                       'test/group_members', 'member_not_found')

    def test_members_delete_unknown(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_members_delete_unknown.yaml'):
            obj = GitLabracadabraGroup('memory', 'test/group_members', {
                'members': {},
                'unknown_members': 'delete',
            })
            obj.process()

    def test_get_id_from_full_path(self):
        # Clean up
        GitLabracadabraGroup._GROUPS_PATH2ID = {}
        GitLabracadabraGroup._GROUPS_ID2PATH = {}
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_get_id_from_full_path.yaml'):
            ret = GitLabracadabraGroup.get_id_from_full_path('test/group_mapping')
            self.assertEqual(ret, 9)

    def test_get_full_path_from_id(self):
        # Clean up
        GitLabracadabraGroup._GROUPS_PATH2ID = {}
        GitLabracadabraGroup._GROUPS_ID2PATH = {}
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/group_get_full_path_from_id.yaml'):
            ret = GitLabracadabraGroup.get_full_path_from_id(9)
            self.assertEqual(ret, 'test/group_mapping')
