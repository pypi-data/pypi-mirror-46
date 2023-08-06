# Copyright 2019 Extreme Networks, Inc.
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

from __future__ import absolute_import

import ast

from st2flake8 import license_rules
from st2flake8.tests.unit import base


class LicenseCheckerTest(base.Flake8PluginTest):

    def get_plugin_instance(self, fixture, **options):
        filename = self.get_fixture_path(fixture)
        tree = ast.parse(self.get_fixture_content(filename))
        instance = license_rules.LicenseChecker(tree, filename)
        self.configure_options(instance, **options)
        return instance

    def test_module_with_default_license(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_apache_license.py'
        )

        expected_error = []

        self.assertListEqual(list(instance.run()), expected_error)

    def test_module_with_proprietary_license(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_proprietary_license.py',
            license_type='proprietary'
        )

        expected_error = []

        self.assertListEqual(list(instance.run()), expected_error)

    def test_module_with_wrong_proprietary_license(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_gnu_license.py',
            license_type='proprietary'
        )

        expected_error = [(1, 1, 'L101 Proprietary license header not found', type(instance))]

        self.assertListEqual(list(instance.run()), expected_error)

    def test_module_with_apache_license(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_apache_license.py',
            license_type='apache'
        )

        expected_error = []

        self.assertListEqual(list(instance.run()), expected_error)

    def test_module_with_wrong_apache_license(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_gnu_license.py',
            license_type='apache'
        )

        expected_error = [(1, 1, 'L102 Apache 2.0 license header not found', type(instance))]

        self.assertListEqual(list(instance.run()), expected_error)

    def test_empty_module_with_license_check_on_zero_file_size(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_no_content.py',
            license_type='proprietary',
            license_min_file_size=0
        )

        expected_error = [(1, 1, 'L101 Proprietary license header not found', type(instance))]

        self.assertListEqual(list(instance.run()), expected_error)

    def test_empty_module_with_license_check_on_min_file_size(self):
        instance = self.get_plugin_instance(
            'license_check/module_with_no_content.py',
            license_type='proprietary',
            license_min_file_size=1
        )

        expected_error = []

        self.assertListEqual(list(instance.run()), expected_error)
