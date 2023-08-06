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

import logging

from gitlab.exceptions import GitlabCreateError, GitlabListError

from gitlabracadabra.mixins.members import MembersMixin
from gitlabracadabra.objects.group import GitLabracadabraGroup
from gitlabracadabra.objects.object import GitLabracadabraObject
from gitlabracadabra.utils import access_level


logger = logging.getLogger(__name__)


class GitLabracadabraProject(GitLabracadabraObject, MembersMixin):
    SCHEMA = {
        "$schema": "http://json-schema.org/schema#",
        "title": "Project",
        "type": "object",
        "properties": {
            # Standard properties
            "create_object": {
                "type": "boolean",
                "description": "Create object if it does not exists",
            },
            # From https://docs.gitlab.com/ee/api/projects.html#create-project
            # and https://docs.gitlab.com/ee/api/projects.html#edit-project
            "name": {
                "type": "string",
                "description": "The name of the new project. Equals path if not provided.",
            },
            # "path": {
            #     "type": "string",
            #     "description": "Repository name for new project. "
            #                    "Generated based on name if not provided (generated lowercased with dashes).",
            # },
            "default_branch": {
                "type": "string",
                "description": "`master` by default",
            },
            "description": {
                "type": "string",
                "description": "Short project description",
            },
            "issues_enabled": {
                "type": "boolean",
                "description": "Enable issues for this project",
            },
            "merge_requests_enabled": {
                "type": "boolean",
                "description": "Enable merge requests for this project",
            },
            "jobs_enabled": {
                "type": "boolean",
                "description": "Enable jobs for this project",
            },
            "wiki_enabled": {
                "type": "boolean",
                "description": "Enable wiki for this project",
            },
            "snippets_enabled": {
                "type": "boolean",
                "description": "Enable snippets for this project",
            },
            "resolve_outdated_diff_discussions": {
                "type": "boolean",
                "description": "Automatically resolve merge request diffs discussions on lines changed with a push",
            },
            "container_registry_enabled": {
                "type": "boolean",
                "description": "Enable container registry for this project",
            },
            "shared_runners_enabled": {
                "type": "boolean",
                "description": "Enable shared runners for this project",
            },
            "visibility": {
                "type": "string",
                "description": "The group’s visibility. Can be private, internal, or public.",
                "enum": ["private", "internal", "public"],
            },
            "import_url": {
                "type": "string",
                "description": "URL to import repository from",
            },
            "public_builds": {
                "type": "boolean",
                "description": "If true, jobs can be viewed by non-project-members",
            },
            "only_allow_merge_if_pipeline_succeeds": {
                "type": "boolean",
                "description": "Set whether merge requests can only be merged with successful jobs",
            },
            "only_allow_merge_if_all_discussions_are_resolved": {
                "type": "boolean",
                "description": "Set whether merge requests can only be merged when all the discussions are resolved",
            },
            "merge_method": {
                "type": "string",
                "description": "Set the merge method used",
                "enum": ["merge", "rebase_merge", "ff"],
            },
            "lfs_enabled": {
                "type": "boolean",
                "description": "Enable LFS",
            },
            "request_access_enabled": {
                "type": "boolean",
                "description": "Allow users to request member access",
            },
            "tag_list": {
                "type": "array",
                "description": "The list of tags for a project; "
                               "put array of tags, that should be finally assigned to a project",
            },
            "avatar": {
                "type": "string",
                "description": "Image file for avatar of the project",
            },
            "printing_merge_request_link_enabled": {
                "type": "boolean",
                "description": "Show link to create/view merge request when pushing from the command line",
            },
            "ci_config_path": {
                "type": "string",
                "description": "The path to CI config file",
            },
            "repository_storage": {
                "type": "string",
                "description": "Which storage shard the repository is on. Available only to admins",
            },
            "approvals_before_merge": {
                "type": "integer",
                "description": "How many approvers should approve merge request by default",
                "multipleOf": 1,
                "minimum": 0,
            },
            "external_authorization_classification_label": {
                "type": "string",
                "description": "The classification label for the project",
            },
            "mirror": {
                "type": "boolean",
                "description": "Enables pull mirroring in a project",
            },
            "mirror_user_id": {
                "type": "integer",
                "description": "User responsible for all the activity surrounding a pull mirror event",
            },
            "mirror_trigger_builds": {
                "type": "boolean",
                "description": "Pull mirroring triggers builds",
            },
            "only_mirror_protected_branches": {
                "type": "boolean",
                "description": "Only mirror protected branches",
            },
            "mirror_overwrites_diverged_branches": {
                "type": "boolean",
                "description": "Pull mirror overwrites diverged branches",
            },
            "packages_enabled": {
                "type": "boolean",
                "description": "Enable or disable packages repository feature",
            },
            "initialize_with_readme": {
                "type": "boolean",
                "description": "false by default",
            },
            # From https://docs.gitlab.com/ee/api/branches.html#create-repository-branch
            "branches": {
                "type": "array",
                "description": "The list of tags for a project; "
                               "put array of tags, that should be finally assigned to a project",
            },
            # From https://docs.gitlab.com/ee/api/projects.html#share-project-with-group_access_level
            # and https://docs.gitlab.com/ee/api/projects.html#delete-a-shared-project-link-within-a-group
            # FIXME expires_at not supported
            "groups": {
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                    "description": "The permissions level to grant the group.",
                    "enum": ["guest", "reporter", "developer", "maintainer"],
                },
            },
            "unknown_groups": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown groups (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/members.html#add-a-member-to-a-group-or-project
            # FIXME expires_at not supported
            "members": {
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                    "description": "The permissions level to grant the member.",
                    "enum": ["guest", "reporter", "developer", "maintainer", "owner"],
                },
            },
            "unknown_members": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown members (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/protected_branches.html#protect-repository-branches
            # FIXME EE features: unprotect_access_level, allowed_to_push, allowed_to_merge, allowed_to_unprotect
            "protected_branches": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "push_access_level": {
                            "type": "string",
                            "description": "Access levels allowed to push (defaults: maintainer access level)",
                            "enum": ["noone", "developer", "maintainer"],
                        },
                        "merge_access_level": {
                            "type": "string",
                            "description": "Access levels allowed to merge (defaults: maintainer access level)",
                            "enum": ["noone", "developer", "maintainer"],
                        },
                    },
                },
            },
            "unknown_protected_branches": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown protected branches (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
            # From https://docs.gitlab.com/ee/api/protected_tags.html#protect-repository-tags
            "protected_tags": {
                "type": "object",
                "additionalProperties": {
                    "type": "string",
                    "description": "Access levels allowed to create (defaults: maintainer access level)",
                    "enum": ["noone", "developer", "maintainer"],
                },
            },
            "unknown_protected_tags": {  # GitLabracadabra
                "type": "string",
                "description": "What to do with unknown protected tags (`warn` by default).",
                "enum": ["warn", "delete", "remove", "ignore", "skip"],
            },
        },
        "additionalProperties": False,
    }

    IGNORED_PARAMS = ['initialize_with_readme', 'unknown_groups', 'unknown_members', 'unknown_protected_branches',
                      'unknown_protected_tags']

    CREATE_PARAMS = ['initialize_with_readme']

    def _get_current_branches(self):
        if not hasattr(self, '_current_branches'):
            try:
                self._current_branches = [branch.name for branch in self._obj.branches.list(all=True)]
            except GitlabListError as err:
                if err.response_code != 403:  # repository_enabled=false?
                    pass
                self._current_branches = None
        return self._current_branches

    """"_process_branches()

    Process the branches param.
    """
    def _process_branches(self, param_name, param_value, dry_run=False):
        assert param_name == 'branches'  # noqa: S101
        if 'default_branch' in self._content and self._content['default_branch'] in self._get_current_branches():
            # Create from target default branch if it exists
            ref = self._content['default_branch']
        elif self._obj.default_branch in self._get_current_branches():
            # Create from current default branch otherwise
            ref = self._obj.default_branch
        else:
            ref = None
        for branch_name in param_value:
            if branch_name not in self._get_current_branches():
                if ref is None:
                    logger.info('[%s] NOT Creating branch: %s (no reference)',
                                self._name, branch_name)
                elif dry_run:
                    logger.info('[%s] NOT Creating branch: %s (dry-run)',
                                self._name, branch_name)
                    self._current_branches.append(branch_name)
                else:
                    logger.info('[%s] Creating branch: %s',
                                self._name, branch_name)
                    self._obj.branches.create({
                        'branch': branch_name,
                        'ref': ref
                    })
                    self._current_branches.append(branch_name)
            if branch_name in self._get_current_branches():
                # Next branch will be created from this ref
                ref = branch_name

    """"_process_groups()

    Process the groups param.
    """
    def _process_groups(self, param_name, param_value, dry_run=False):
        assert param_name == 'groups'  # noqa: S101
        unknown_groups = self._content.get('unknown_groups', 'warn')
        # We first check for already shared groups
        for group in self._obj.shared_with_groups:
            if 'group_full_path' not in group:
                # Gitlab < 11.8
                # https://gitlab.com/gitlab-org/gitlab-ce/merge_requests/24052
                group['group_full_path'] = GitLabracadabraGroup.get_full_path_from_id(group['group_id'])
            GitLabracadabraGroup.map_group(group['group_id'], group['group_full_path'])
            if group['group_full_path'] in param_value.keys():
                target_access_level = access_level(param_value[group['group_full_path']])
                if group['group_access_level'] != target_access_level:
                    if dry_run:
                        logger.info('[%s] NOT Changing group %s access level: %s -> %s (dry-run)',
                                     self._name, group['group_full_path'],
                                     group['group_access_level'], target_access_level)
                    else:
                        logger.info('[%s] Changing group %s access level: %s -> %s',
                                     self._name, group['group_full_path'],
                                     group['group_access_level'], target_access_level)
                        self._obj.unshare(group['group_id'])
                        self._obj.share(group['group_id'], target_access_level)
                param_value.pop(group['group_full_path'])
            else:
                if unknown_groups in ['delete', 'remove']:
                    if dry_run:
                        logger.info('[%s] NOT Unsharing from unknown group: %s (dry-run)',
                                    self._name, group['group_full_path'])
                    else:
                        logger.info('[%s] Unsharing from unknown group: %s',
                                    self._name, group['group_full_path'])
                        self._obj.unshare(group['group_id'])
                elif unknown_groups not in ['ignore', 'skip']:
                    logger.warning('[%s] NOT Unsharing from unknown group: %s (unknown_groups=%s)',
                                   self._name, group['group_full_path'], unknown_groups)
        # Remaining groups
        for group_full_path, target_group_access in sorted(param_value.items()):
            group_id = GitLabracadabraGroup.get_id_from_full_path(group_full_path)
            if group_id is None:
                logger.warning('[%s] Group not found %s',
                                self._name, group_full_path)
                continue
            target_access_level = access_level(target_group_access)
            if dry_run:
                logger.info('[%s] NOT Sharing group %s: %s -> %s (dry-run)',
                            self._name, group_full_path,
                            0, target_access_level)
            else:
                logger.info('[%s] Sharing group %s: %s -> %s',
                            self._name, group_full_path,
                            0, target_access_level)
                self._obj.share(group_id, target_access_level)

    """"_process_protected_branches()

    Process the protected_branches param.
    """
    def _process_protected_branches(self, param_name, param_value, dry_run=False):
        assert param_name == 'protected_branches'  # noqa: S101
        unknown_protected_branches = self._content.get('unknown_protected_branches', 'warn')
        current_protected_branches = dict([[protected_branch.name, protected_branch]
                                          for protected_branch in self._obj.protectedbranches.list(all=True)])
        # We first check for already protected branches
        for protected_name, target_config in sorted(param_value.items()):
            target_config_int = {}
            for k, v in target_config.items():
                if k.endswith('_access_level'):
                    target_config_int[k] = access_level(v)
                else:
                    target_config_int[k] = v
            target_config_int['name'] = protected_name
            if protected_name in current_protected_branches:
                current_protected_branch = current_protected_branches[protected_name]
                current_config = {
                    'name': protected_name,
                    'push_access_level': current_protected_branch.push_access_levels[0]['access_level'],
                    'merge_access_level': current_protected_branch.merge_access_levels[0]['access_level'],
                }
            else:
                current_config = {}
            if current_config != target_config_int:
                if dry_run:
                    logger.info('[%s] NOT Changing protected branch %s access level: %s -> %s (dry-run)',
                                 self._name, protected_name, current_config, target_config_int)
                else:
                    logger.info('[%s] Changing protected branch %s access level: %s -> %s',
                                 self._name, protected_name, current_config, target_config_int)
                    if 'name' in current_config:
                        self._obj.protectedbranches.delete(protected_name)
                    try:
                        self._obj.protectedbranches.create(target_config_int)
                    except GitlabCreateError as err:
                        if err.response_code != 409:
                            pass
                        logger.warning('[%s] Unable to create protected branch %s: %s',
                                        self._name, protected_name, err.error_message)
        # Remaining protected branches
        if unknown_protected_branches not in ['ignore', 'skip']:
            for protected_name in current_protected_branches:
                if protected_name not in param_value:
                    if unknown_protected_branches in ['delete', 'remove']:
                        if dry_run:
                            logger.info('[%s] NOT Deleting unknown protected branch: %s (dry-run)',
                                        self._name, protected_name)
                        else:
                            logger.info('[%s] Deleting unknown protected branch: %s',
                                        self._name, protected_name)
                            self._obj.protectedbranches.delete(protected_name)
                    else:
                        logger.warning('[%s] NOT Deleting unknown protected branch: %s'
                                       ' (unknown_protected_branches=%s)',
                                       self._name, protected_name, unknown_protected_branches)

    """"_process_protected_tags()

    Process the protected_tags param.
    """
    def _process_protected_tags(self, param_name, param_value, dry_run=False):
        assert param_name == 'protected_tags'  # noqa: S101
        unknown_protected_tags = self._content.get('unknown_protected_tags', 'warn')
        try:
            current_protected_tags = dict([[protected_tag.name, protected_tag]
                                           for protected_tag in self._obj.protectedtags.list(all=True)])
        except AttributeError:
            logger.error('[%s] Unable to create protected tags: %s',
                         self._name, 'protected tags requires python-gitlab >= 1.7.0')
            return
        # We first check for already protected tags
        for protected_name, target_config in sorted(param_value.items()):
            target_config = {
                'name': protected_name,
                'create_access_level': access_level(target_config),
            }
            if protected_name in current_protected_tags:
                current_protected_tag = current_protected_tags[protected_name]
                current_config = {
                    'name': protected_name,
                    'create_access_level': current_protected_tag.create_access_levels[0]['access_level'],
                }
            else:
                current_config = {}
            if current_config != target_config:
                if dry_run:
                    logger.info('[%s] NOT Changing protected tag %s access level: %s -> %s (dry-run)',
                                self._name, protected_name, current_config, target_config)
                else:
                    logger.info('[%s] Changing protected tag %s access level: %s -> %s',
                                self._name, protected_name, current_config, target_config)
                    if 'name' in current_config:
                        self._obj.protectedtags.delete(protected_name)
                    self._obj.protectedtags.create(target_config)
        # Remaining protected tags
        if unknown_protected_tags not in ['ignore', 'skip']:
            current_protected_tags = sorted([protected_tag.name
                                             for protected_tag in self._obj.protectedtags.list(all=True)])
            for protected_name in current_protected_tags:
                if protected_name not in param_value:
                    if unknown_protected_tags in ['delete', 'remove']:
                        if dry_run:
                            logger.info('[%s] NOT Deleting unknown protected tag: %s (dry-run)',
                                        self._name, protected_name)
                        else:
                            logger.info('[%s] Deleting unknown protected tag: %s',
                                        self._name, protected_name)
                            self._obj.protectedtags.delete(protected_name)
                    else:
                        logger.warning('[%s] NOT Deleting unknown protected tag: %s (unknown_protected_tags=%s)',
                                       self._name, protected_name, unknown_protected_tags)
