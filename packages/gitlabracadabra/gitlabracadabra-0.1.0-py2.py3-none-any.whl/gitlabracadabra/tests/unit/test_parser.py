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

from gitlabracadabra.objects.group import GitLabracadabraGroup
from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.parser import GitlabracadabraParser


class TestParser(TestCase):
    def test_extend(self):
        p = GitlabracadabraParser.from_yaml('-', '''
            .hidden-key:
              param1: value1
              param2: value2
            shown-key:
              extends: .hidden-key
              param3: value3
            another-key:
              param4: value4
            ''')
        d = {k: v for k, v in p._items()}

        self.assertNotIn('.hidden-key', d)
        self.assertIn('shown-key', d)
        self.assertIn('another-key', d)
        self.assertEqual(d['another-key'], {'param4': 'value4'})

    def test_recursion(self):
        p = GitlabracadabraParser.from_yaml('-', '''
            key1:
              extends: key3
              foo: bar
            key2:
              extends: key1
              foo2: bar2
            key3:
              extends: key2
              foo3: bar3
            ''')
        with self.assertRaises(ValueError) as cm:
            {k: v for k, v in p._items()}

        self.assertEqual(str(cm.exception), 'key1: nesting too deep in `extends`')

    def test_objects(self):
        p = GitlabracadabraParser.from_yaml('-', '''
            .project-template:
              wiki_enabled: true
              issues_enabled: true
            group1/:
              description: My group
            group1/project1:
              extends: .project-template
              wiki_enabled: false
              description: My project
              buggy_param: Oh no!
            ''')
        d = p.objects()

        self.assertNotIn('.project-template', d)

        self.assertIn('group1', d)
        group1 = d['group1']
        self.assertIsInstance(group1, GitLabracadabraGroup)
        self.assertEqual(group1._errors, [])
        self.assertEqual(group1._content, {'description': 'My group'})

        self.assertIn('group1/project1', d)
        project1 = d['group1/project1']
        self.assertIsInstance(project1, GitLabracadabraProject)
        self.assertEqual(len(project1._errors), 1)
        self.assertEqual(project1._errors[0].message, "Additional properties are not allowed "
                                                      "('buggy_param' was unexpected)")
        self.assertEqual(project1._content, {'buggy_param': 'Oh no!',
                                             'description': 'My project',
                                             'issues_enabled': True,
                                             'wiki_enabled': False})
