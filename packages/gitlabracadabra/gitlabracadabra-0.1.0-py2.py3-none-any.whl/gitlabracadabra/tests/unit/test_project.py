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
from gitlabracadabra.objects.project import GitLabracadabraProject

my_vcr = VCR(
    match_on=['method', 'scheme', 'host', 'port', 'path', 'query', 'body'],
)


class TestProject(TestCase):
    def setUp(self):
        gitlabracadabra.manager._gitlab = Gitlab(  # noqa: S106
            'http://localhost',
            private_token='DKkdC5JmKWWZgXZGzg83',
        )

    def tearDown(self):
        gitlabracadabra.manager._gitlab = None

    def test_no_create(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_no_create.yaml'):
            obj = GitLabracadabraProject('memory', 'test/no_create_object', {})
            obj.process()

    def test_create(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_create.yaml'):
            obj = GitLabracadabraProject('memory', 'test/create_object', {'create_object': True})
            obj.process()

    def test_exists(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_exists.yaml'):
            obj = GitLabracadabraProject('memory', 'test/exists', {})
            obj.process()

    def test_simple_parameters(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_simple_parameters.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_simple_parameters', {
                'name': 'project-with-simple-parameters',
                'description': 'Project with simple parameters',
                'issues_enabled': False,
                'merge_requests_enabled': False,
                'jobs_enabled': False,
                'wiki_enabled': False,
                'snippets_enabled': False,
                'resolve_outdated_diff_discussions': True,
                'container_registry_enabled': False,
                'shared_runners_enabled': False,
                'visibility': 'public',
                # 'import_url': 'http://example.com/foo.git',  # FIXME
                # 'public_builds': False,  # FIXME
                'only_allow_merge_if_pipeline_succeeds': True,
                'only_allow_merge_if_all_discussions_are_resolved': True,
                'merge_method': 'ff',
                'lfs_enabled': False,
                'request_access_enabled': True,
                'tag_list': ['foo', 'bar'],
                # 'avatar': 'http://example.com/foo.png',  # FIXME
                'printing_merge_request_link_enabled': False,
                'ci_config_path': 'debian/gitlab-ci.yml',
                # 'repository_storage': 'foo',  # EE
                # 'approvals_before_merge': False,  # EE
                # 'external_authorization_classification_label': 'foo',  # EE
                # 'mirror': False,  # EE
                # 'mirror_user_id': 2,  # EE
                # 'mirror_trigger_builds': False,  # EE
                # 'only_mirror_protected_branches': True,  # EE
                # 'mirror_overwrites_diverged_branches': True,  # EE
                # 'packages_enabled': True,  # EE
            })
            obj.process()

    def test_default_branch_exists(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_default_branch_exists.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_default_branch', {
                'default_branch': 'exists',
            })
            obj.process()

    def test_default_branch_not_exists(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_default_branch_not_exists.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_default_branch', {
                'default_branch': 'not_exists',
            })
            with patch('gitlabracadabra.objects.object.logger', autospec=True) as logger:
                obj.process()
                logger.error.assert_called_once_with('[%s] Unable to change param %s (%s -> %s): %s',
                                                     'test/project_default_branch',
                                                     'default_branch',
                                                     'exists',
                                                     'not_exists',
                                                     {'base': [
                                                      "Could not change HEAD: branch 'not_exists' does not exist"]})

    def test_branches(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_branches.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_branches', {
                'branches': ['a', 'b', 'c'],

            })
            obj.process()

    def test_groups(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_groups.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_groups', {
                'groups': {'test2': 'developer'},
            })
            obj.process()

    def test_groups_change_access_level(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_groups_change_access_level.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_groups', {
                'groups': {'test2': 'maintainer'},
            })
            obj.process()

    def test_groups_not_found(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_groups_not_found.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_groups', {
                'groups': {'group_not_found': 'maintainer'},
                'unknown_groups': 'ignore',
            })
            with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
                obj.process()
                logger.warning.assert_called_once_with('[%s] Group not found %s',
                                                               'test/project_groups',
                                                               'group_not_found')

    def test_groups_delete_unknown(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_groups_delete_unknown.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_groups', {
                'groups': {},
                'unknown_groups': 'delete',
            })
            obj.process()

    def test_members(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_members.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_members', {
                'members': {'some_member': 'developer'},
            })
            obj.process()

    def test_members_change_access_level(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_members_change_access_level.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_members', {
                'members': {'some_member': 'maintainer'},
            })
            obj.process()

    def test_members_not_found(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_members_not_found.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_members', {
                'members': {'member_not_found': 'maintainer'},
                'unknown_members': 'ignore',
            })
            with patch('gitlabracadabra.mixins.members.logger', autospec=True) as logger:
                obj.process()
                logger.warning.assert_called_once_with('[%s] User not found %s',
                                                       'test/project_members', 'member_not_found')

    def test_members_delete_unknown(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_members_delete_unknown.yaml'):
            obj = GitLabracadabraProject('memory', 'test/project_members', {
                'members': {},
                'unknown_members': 'delete',
            })
            obj.process()

    def test_protected_branches_wildcard(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_protected_branches_wildcard.yaml'):
            obj = GitLabracadabraProject('memory', 'test/protected_branches', {
                'protected_branches': {'release/*': {'push_access_level': 'noone', 'merge_access_level': 'maintainer'}},
            })
            with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
                obj.process()
                logger.warning.assert_called_once_with('[%s] NOT Deleting unknown protected branch: %s'
                                                       ' (unknown_protected_branches=%s)',
                                                       'test/protected_branches', 'master', 'warn')

    def test_protected_branches_delete(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_protected_branches_delete.yaml'):
            obj = GitLabracadabraProject('memory', 'test/protected_branches', {
                'protected_branches': {},
                'unknown_protected_branches': 'delete',
            })
            with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
                obj.process()
                logger.info.assert_called_once_with('[%s] Deleting unknown protected branch: %s',
                                                       'test/protected_branches', 'master')

    def test_protected_tags_wildcard(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_protected_tags_wildcard.yaml'):
            obj = GitLabracadabraProject('memory', 'test/protected_tags', {
                'protected_tags': {'v*': 'maintainer'},
            })
            with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
                obj.process()
                logger.info.assert_called_once_with('[%s] Changing protected tag %s access level: %s -> %s',
                                                    'test/protected_tags', 'v*',
                                                    {}, {'name': 'v*', 'create_access_level': 40})

    def test_protected_tags_change(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_protected_tags_change.yaml'):
            obj = GitLabracadabraProject('memory', 'test/protected_tags', {
                'protected_tags': {'v1.0': 'maintainer'},
            })
            with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
                obj.process()
                logger.info.assert_called_once_with('[%s] Changing protected tag %s access level: %s -> %s',
                                                    'test/protected_tags', 'v1.0',
                                                    {'name': 'v1.0', 'create_access_level': 30},
                                                    {'name': 'v1.0', 'create_access_level': 40})

    def test_protected_tags_delete(self):
        with my_vcr.use_cassette('fixtures/vcr_cassettes/unit/project_protected_tags_delete.yaml'):
            obj = GitLabracadabraProject('memory', 'test/protected_tags', {
                'protected_tags': {},
                'unknown_protected_tags': 'delete',
            })
            with patch('gitlabracadabra.objects.project.logger', autospec=True) as logger:
                obj.process()
                logger.info.assert_called_once_with('[%s] Deleting unknown protected tag: %s',
                                                       'test/protected_tags', 'unknown')
