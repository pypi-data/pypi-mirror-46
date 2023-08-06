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
from gitlabracadabra.objects.object import GitLabracadabraObject


class GitLabracadabraUser(GitLabracadabraObject):
    SCHEMA = {
        "$schema": "http://json-schema.org/schema#",
        "title": "User",
        "type": "object",
        "properties": {
            # Standard properties
            "create_object": {
                "type": "boolean",
                "description": "Create object if it does not exists",
            },
            # From https://docs.gitlab.com/ee/api/users.html#user-creation
            "email": {
                "type": "string",
                "description": "Email",
            },
            "password": {
                "type": "string",
                "description": "Password",
            },
            "reset_password": {
                "type": "boolean",
                "description": "Send user password reset link",
            },
            "username": {
                "type": "string",
                "description": "Username",
            },
            "name": {
                "type": "string",
                "description": "Name",
            },
            "skype": {
                "type": "string",
                "description": "Skype ID",
            },
            "linkedin": {
                "type": "string",
                "description": "LinkedIn",
            },
            "twitter": {
                "type": "string",
                "description": "Twitter account",
            },
            "website_url": {
                "type": "string",
                "description": "Website URL",
            },
            "organization": {
                "type": "string",
                "description": "Organization name",
            },
            "projects_limit": {
                "type": "integer",
                "description": "Number of projects user can create",
                "multipleOf": 1,
                "minimum": 0,
            },
            "extern_uid": {
                "type": "string",
                "description": "External UID",
            },
            "provider": {
                "type": "string",
                "description": "External provider name",
            },
            "bio": {
                "type": "string",
                "description": "User’s biography",
            },
            "location": {
                "type": "string",
                "description": "User’s location",
            },
            "public_email": {
                "type": "string",
                "description": "The public email of the user",
            },
            "admin": {
                "type": "boolean",
                "description": "User is admin - true or false (default)",
            },
            "can_create_group": {
                "type": "boolean",
                "description": "User can create groups - true or false",
            },
            "skip_confirmation": {
                "type": "boolean",
                "description": "Skip confirmation - true or false (default)",
            },
            "external": {
                "type": "boolean",
                "description": "Flags the user as external - true or false(default)",
            },
            "avatar": {
                "type": "string",
                "description": "Image file for user’s avatar",
            },
            "private_profile": {
                "type": "boolean",
                "description": "User’s profile is private - true or false",
            },
            "shared_runners_minutes_limit": {
                "type": "integer",
                "description": "Pipeline minutes quota for this user",
                "multipleOf": 1,
                "minimum": 0,
            },
            "extra_shared_runners_minutes_limit": {
                "type": "integer",
                "description": "Extra pipeline minutes quota for this user",
                "multipleOf": 1,
                "minimum": 0,
            },
        },
        "additionalProperties": False,
    }

    FIND_PARAM = 'username'

    CREATE_KEY = 'username'

    CREATE_PARAMS = ['email', 'password', 'reset_password', 'name']

    """"Users mapping

    indexed by id and username.
    """
    _USERS_USERNAME2ID = {}
    _USERS_ID2USERNAME = {}

    """"Map user id and username
    """
    @classmethod
    def map_user(cls, user_id, user_username):
        cls._USERS_ID2USERNAME[user_id] = user_username
        cls._USERS_USERNAME2ID[user_username] = user_id

    """"Get user username from id
    """
    @classmethod
    def get_username_from_id(cls, user_id):
        if user_id not in cls._USERS_ID2USERNAME:
            try:
                obj_manager = gitlabracadabra.manager.get_manager().users
                user = obj_manager.get(user_id)
                cls._USERS_ID2USERNAME[user.id] = user.username
                cls._USERS_USERNAME2ID[user.username] = user.id
            except GitlabGetError as e:
                if e.response_code != 404:
                    pass
                cls._USERS_ID2USERNAME[user_id] = None
        return cls._USERS_ID2USERNAME[user_id]

    """"Get user id from username
    """
    @classmethod
    def get_id_from_username(cls, user_username):
        if user_username not in cls._USERS_USERNAME2ID:
            try:
                obj_manager = gitlabracadabra.manager.get_manager().users
                user = obj_manager.list(username=user_username)[0]
                cls._USERS_ID2USERNAME[user.id] = user.username
                cls._USERS_USERNAME2ID[user.username] = user.id
            except IndexError:
                cls._USERS_USERNAME2ID[user_username] = None
        return cls._USERS_USERNAME2ID[user_username]
