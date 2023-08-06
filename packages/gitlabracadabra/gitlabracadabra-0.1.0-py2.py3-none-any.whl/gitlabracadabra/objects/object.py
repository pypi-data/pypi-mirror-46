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

from gitlab.exceptions import GitlabCreateError, GitlabGetError, GitlabUpdateError

from jsonschema.validators import validator_for

import gitlabracadabra.manager


logger = logging.getLogger(__name__)


class GitLabracadabraObject(object):
    SCHEMA = {
        "$schema": "http://json-schema.org/schema#",
        "title": "Object",
        "type": "object",
        "properties": {
        },
        "additionalProperties": False,
        # "required": [],
    }

    # If not None, use find(FIND_PARAM=...) instead of get(...)
    FIND_PARAM = None

    CREATE_KEY = 'name'

    CREATE_PARAMS = []

    IGNORED_PARAMS = []

    def __init__(self, action_file, name, content):
        self._action_file = action_file
        self._name = name
        self._content = content
        validator_class = validator_for(self.SCHEMA)
        validator_class.check_schema(self.SCHEMA)
        validator = validator_class(self.SCHEMA)
        self._errors = sorted(validator.iter_errors(content), key=lambda e: e.path)
        self._create_object = self._content.pop('create_object', None)

    def errors(self):
        return self._errors

    """"type_name()

    GitLabracadabraProject -> project.
    """
    @classmethod
    def _type_name(cls):
        return cls.__name__[15:].lower()

    """"type_name_plural()

    GitLabracadabraProject -> projects.
    """
    @classmethod
    def _type_name_plural(cls):
        return cls._type_name() + 's'

    """"_gitlab_manager()

    Return the python-gitlab Gilab object.
    """
    def _gitlab_manager(self):
        return gitlabracadabra.manager.get_manager()

    """"_object_manager()

    Return the python-gitlab Gilab object.
    """
    def _object_manager(self):
        return getattr(self._gitlab_manager(), self._type_name_plural())

    """"_create()

    Create the object.
    """
    def _create(self, dry_run=False):
        obj_manager = self._object_manager()
        namespace_manager = self._gitlab_manager().namespaces
        namespaces = self._name.split("/")
        object_path = namespaces.pop()
        create_params = {
            'path': object_path,
        }
        if self.CREATE_KEY in self.SCHEMA['properties']:
            create_params[self.CREATE_KEY] = object_path
        for param_name in self.CREATE_PARAMS:
            if param_name in self._content:
                create_params[param_name] = self._content[param_name]
        if len(namespaces):
            try:
                parent_namespace = namespace_manager.get("/".join(namespaces))
            except GitlabGetError as e:
                error_message = e.error_message
                if e.response_code == 404:
                    error_message = 'parent namespace not found'
                logger.error('[%s] NOT Creating %s (%s)', self._name, self._type_name(), error_message)
                return None
            create_params['namespace_id'] = parent_namespace.id
        if dry_run:
            logger.info('[%s] NOT Creating %s (dry-run)', self._name, self._type_name())
            return None
        else:
            logger.info('[%s] Creating %s', self._name, self._type_name())
            try:
                return obj_manager.create(create_params)
            except GitlabCreateError as e:
                logger.error('[%s] NOT Creating %s (%s)', self._name, self._type_name(), e.error_message)
                return None

    """"_process_param()

    Process one param.
    """
    def _process_param(self, param_name, param_value, dry_run=False):
        if param_name in self.IGNORED_PARAMS:
            return
        if isinstance(param_value, list):
            param_value.sort()
        try:
            current_value = getattr(self._obj, param_name)
        except AttributeError:
            # FIXME Hidden attributes cannot be idempotent (i.e password)
            current_value = None
        if current_value is None:
            logger.info('[%s] NOT Changing param %s: %s -> %s (current value is None)',
                        self._name, param_name, current_value, param_value)
            return
        if isinstance(param_value, str):
            # GitLab normalize to CRLF
            # YAML normalize to LF
            param_value = param_value.replace('\n', '\r\n')
        if current_value != param_value:
            if dry_run:
                logger.info('[%s] NOT Changing param %s: %s -> %s (dry-run)',
                            self._name, param_name, current_value, param_value)
                setattr(self._obj, param_name, param_value)
            else:
                logger.info('[%s] Changing param %s: %s -> %s',
                            self._name, param_name, current_value, param_value)
                setattr(self._obj, param_name, param_value)
                try:
                    self._obj.save()
                except GitlabUpdateError as e:
                    logger.error('[%s] Unable to change param %s (%s -> %s): %s',
                                 self._name, param_name, current_value, param_value, e.error_message)

    """"process()

    Process the object.
    """
    def process(self, dry_run=False):
        obj_manager = self._object_manager()
        if self.FIND_PARAM:
            params = {self.FIND_PARAM: self._name}
            try:
                self._obj = obj_manager.list(**params)[0]
            except IndexError:
                self._obj = None
        else:
            try:
                self._obj = obj_manager.get(self._name)
            except GitlabGetError as err:
                if err.response_code != 404:
                    pass
                self._obj = None
        if self._obj is None:
            if self._create_object:
                self._obj = self._create(dry_run)
                if self._obj is None:
                    return
            else:
                logger.info('[%s] NOT Creating %s (create_project is false)', self._name, self._type_name())
                return
        for param_name, param_value in sorted(self._content.items()):
            process_method = getattr(self, '_process_' + param_name, self._process_param)
            process_method(param_name, param_value, dry_run)
