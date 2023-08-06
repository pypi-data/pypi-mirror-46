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

import os
import optparse
import six
import unittest

from st2flake8.tests.fixtures import loader as fixture_loader


class Flake8PluginTest(unittest.TestCase):

    def get_fixture_path(self, fixture):
        return os.path.join(fixture_loader.get_fixtures_base_path(), fixture)

    def get_fixture_content(self, filename):
        with open(filename, 'r') as f:
            content = f.read()

        return content

    def configure_options(self, instance, **kwargs):
        # Set up the args parser.
        parser = optparse.OptionParser()
        parser.config_options = []
        instance.add_options(parser)

        # Setup the args to pass into the checker.
        cli_args = []

        for k, v in six.iteritems(kwargs):
            arg_name = '--' + k.replace('_', '-')
            cli_args.extend([arg_name, str(v)])

        (options, args) = parser.parse_args(cli_args)

        # Apply the options to the plugin instance.
        instance.parse_options(options)
