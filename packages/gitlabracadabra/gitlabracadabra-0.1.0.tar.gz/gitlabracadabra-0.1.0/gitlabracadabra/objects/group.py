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

from gitlab.exceptions import GitlabGetError

import gitlabracadabra.manager
from gitlabracadabra.mixins.members import MembersMixin
from gitlabracadabra.objects.object import GitLabracadabraObject


class GitLabracadabraGroup(GitLabracadabraObject, MembersMixin):
    SCHEMA = {
        "$schema": "http://json-schema.org/schema#",
        "title": "Group",
        "type": "object",
        "properties": {
            # Standard properties
            "create_object": {
                "type": "boolean",
                "description": "Create object if it does not exists",
            },
            # From https://docs.gitlab.com/ee/api/groups.html#new-group
            "name": {
                "type": "string",
                "description": "The name of the group",
            },
            # "path": {
            #     "type": "string",
            #     "description": "The path of the group",
            # },
            "description": {
                "type": "string",
                "description": "The group’s description",
            },
            "membership_lock": {
                "type": "boolean",
                "description": "Prevent adding new members to project membership within this group",
            },
            "share_with_group_lock": {
                "type": "boolean",
                "description": "Prevent sharing a project with another group within this group",
            },
            "visibility": {
                "type": "string",
                "description": "The group’s visibility. Can be private, internal, or public.",
                "enum": ["private", "internal", "public"],
            },
            "lfs_enabled": {
                "type": "boolean",
                "description": "Enable/disable Large File Storage (LFS) for the projects in this group",
            },
            "request_access_enabled": {
                "type": "boolean",
                "description": "Allow users to request member access.",
            },
            "file_template_project_id": {
                "type": "integer",
                "description": "(Premium) The ID of a project to load custom file templates from",
                "multipleOf": 1,
                "minimum": 0,
            },
            "shared_runners_minutes_limit": {
                "type": "integer",
                "description": "(admin-only) Pipeline minutes quota for this group.",
                "multipleOf": 1,
                "minimum": 0,
            },
            "extra_shared_runners_minutes_limit": {
                "type": "integer",
                "description": "(admin-only) Extra pipeline minutes quota for this group.",
                "multipleOf": 1,
                "minimum": 0,
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
        },
        "additionalProperties": False,
    }

    IGNORED_PARAMS = ['unknown_members']

    """"Groups mapping

    indexed by id and full path.
    """
    _GROUPS_PATH2ID = {}
    _GROUPS_ID2PATH = {}

    """"Map group id and full path
    """
    @classmethod
    def map_group(cls, group_id, group_full_path):
        cls._GROUPS_ID2PATH[group_id] = group_full_path
        cls._GROUPS_PATH2ID[group_full_path] = group_id

    """"Get group full path from id
    """
    @classmethod
    def get_full_path_from_id(cls, group_id):
        if group_id not in cls._GROUPS_ID2PATH:
            try:
                obj_manager = gitlabracadabra.manager.get_manager().groups
                group = obj_manager.get(group_id)
                cls._GROUPS_ID2PATH[group.id] = group.full_path
                cls._GROUPS_PATH2ID[group.full_path] = group.id
            except GitlabGetError as e:
                if e.response_code != 404:
                    pass
                cls._GROUPS_ID2PATH[group_id] = None
        return cls._GROUPS_ID2PATH[group_id]

    """"Get group id from full path
    """
    @classmethod
    def get_id_from_full_path(cls, group_full_path):
        if group_full_path not in cls._GROUPS_PATH2ID:
            try:
                obj_manager = gitlabracadabra.manager.get_manager().groups
                group = obj_manager.get(group_full_path)
                cls._GROUPS_ID2PATH[group.id] = group.full_path
                cls._GROUPS_PATH2ID[group.full_path] = group.id
            except GitlabGetError as e:
                if e.response_code != 404:
                    pass
                cls._GROUPS_PATH2ID[group_full_path] = None
        return cls._GROUPS_PATH2ID[group_full_path]
