#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2017 Gauvain Pocentek <gauvain@pocentek.net>
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

import yaml


class GitlabracadabraParser(object):
    """"YAML parser
    """
    def __init__(self, action_file, config):
        self._action_file = action_file
        self._config = config
        self._objects = None

    @classmethod
    def from_yaml(cls, action_file, yaml_blob):
        config = yaml.safe_load(yaml_blob)
        return GitlabracadabraParser(action_file, config)

    @classmethod
    def from_yaml_file(cls, action_file):
        with open(action_file) as yaml_blob:
            return cls.from_yaml(action_file, yaml_blob)

    """"items()

    Handle hidden objects (starting with a dot) and extends.
    """
    def _items(self):
        for k, v in sorted(self._config.items()):
            if k.startswith('.'):
                continue
            recursion = 0
            while 'extends' in v:
                recursion += 1
                if recursion >= 10:
                    raise ValueError('%s: nesting too deep in `extends`' % k)
                v2 = self._config[v['extends']].copy()
                v3 = v.copy()
                v3.pop('extends', None)
                v2.update(v3)
                v = v2
            # Drop None values from v
            yield (k, {a: b for a, b in v.items() if b is not None})

    """"objects()

    Returns .
    """
    def objects(self):
        if self._objects is not None:
            return self._objects
        self._objects = {}
        for k, v in self._items():
            if 'type' in v:
                obj_type = v['type']
                v.pop('type')
            elif k.endswith('/'):
                obj_type = 'group'
                k = k[:-1]
            else:
                obj_type = 'project'
            obj_classname = 'GitLabracadabra' + obj_type[0].upper() + obj_type[1:].lower()
            obj_module = __import__('gitlabracadabra.objects.' + obj_type.lower(), globals(), locals(), [obj_classname])
            obj_class = getattr(obj_module, obj_classname)
            self._objects[k] = obj_class(self._action_file, k, v)
        return self._objects
