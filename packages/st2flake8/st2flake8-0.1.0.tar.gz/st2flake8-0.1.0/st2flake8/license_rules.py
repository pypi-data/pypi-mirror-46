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

import st2flake8

from flake8_polyfill import options


PROPRIETARY_LICENSE = """
# Unauthorized copying of this file, via any medium is strictly
# prohibited. Proprietary and confidential. See the LICENSE file
# included with this work for details.
"""

APACHE_20_LICENSE = """
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
"""

PROPRIETARY_LICENSE = PROPRIETARY_LICENSE.strip('\n')
APACHE_20_LICENSE = APACHE_20_LICENSE.strip('\n')

LICENSE_TYPES = {
    'proprietary': PROPRIETARY_LICENSE,
    'apache': APACHE_20_LICENSE
}

ERROR_MESSAGES = {
    'proprietary': 'L101 Proprietary license header not found',
    'apache': 'L102 Apache 2.0 license header not found'
}


class LicenseChecker(object):
    name = 'st2flake8_license'
    version = st2flake8.__version__
    off_by_default = True

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        options.register(
            parser,
            '--license-type',
            type='choice',
            choices=['proprietary', 'apache'],
            default='apache',
            action='store',
            parse_from_config=True,
            help='Checks for specific type of license header.'
        )

        options.register(
            parser,
            '--license-min-file-size',
            type='int',
            default=1,
            action='store',
            parse_from_config=True,
            help='Minimum number of characters in a file before requiring a license header.'
        )

    @classmethod
    def parse_options(cls, parsed_options):
        cls.license_type = parsed_options.license_type
        cls.min_file_size = parsed_options.license_min_file_size

    def run(self):
        """Check for license header given license type.
        L101 Proprietary license header not found
        L102 Apache 2.0 license header not found
        """
        with open(self.filename, 'r') as f:
            content = f.read()

        if len(content) >= self.min_file_size and LICENSE_TYPES[self.license_type] not in content:
            yield 1, 1, ERROR_MESSAGES[self.license_type], type(self)
