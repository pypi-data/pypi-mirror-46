# -*- coding: utf-8 -*-
# Copyright (c) 2018  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Written by Chenxiong Qi <cqi@redhat.com>
#            Qixiang Wan <qwan@redhat.com>

import os
import json
try:
    import unittest2 as unittest
except ImportError:
    import unittest


from ursa_major.utils import Modulemd
from six.moves.configparser import ConfigParser

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_DATA_DIR = os.path.join(TESTS_DIR, 'test_data')

CONFIG_FILE = os.path.join(TEST_DATA_DIR, 'ursa-major-test.conf')
URSA_MAJOR_TEST_CONFIG = ConfigParser()
URSA_MAJOR_TEST_CONFIG.read(CONFIG_FILE)


def make_mmd(name, stream, version, context, requires=None, buildrequires=None):
    """Creates new Modulemd.Module instance

    :param name: module name
    :param stream: module stream
    :param version: module version
    :param context: module context
    :param requires: Dict of requires, example:
        {'platform': ['rhel-8.0'], 'python3': 'master'}
    :param buildrequires: Dict of build_requires, example:
        {'platform': 'rhel-8.0', 'bootstrap': ['rhel-8.0']}
    :rtype: Modulemd.Module instance
    """
    mmd = Modulemd.Module()
    mmd.set_name(name)
    mmd.set_stream(stream)
    mmd.set_version(int(version))
    mmd.set_context(context)
    # required options
    mmd.set_mdversion(2)
    mmd.set_summary("A test module in all its beautiful beauty.")
    description = ("This module demonstrates how to write simple "
                   "modulemd files And can be used for testing "
                   "the build and release pipeline.")
    mmd.set_description(description)
    licenses = Modulemd.SimpleSet()
    licenses.add("GPL")
    mmd.set_module_licenses(licenses)

    deps_list = []
    requires = requires or {}
    buildrequires = buildrequires or {}

    deps = Modulemd.Dependencies()
    for req_name, req_streams in requires.items():
        if not isinstance(req_streams, list):
            req_streams = [req_streams]
        deps.add_requires(req_name, req_streams)

    for req_name, req_streams in buildrequires.items():
        if not isinstance(req_streams, list):
            req_streams = [req_streams]
        deps.add_buildrequires(req_name, req_streams)
    deps_list.append(deps)
    mmd.set_dependencies(deps_list)

    return mmd


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class UrsaMajorTestCase(unittest.TestCase):
    def load_json_from_file(self, filename):
        test_data_file = os.path.join(TEST_DATA_DIR, filename)
        with open(test_data_file, 'r') as f:
            return json.load(f)


def make_mbs_response(module_builds, per_page=None):
    """Helper function to make fake MBS response JSON

    When calling this method, developer only needs to pass a list of module
    builds. Finally, a full response JSON data with only one page data set is
    returned.
    """
    total = len(module_builds)
    per_page = per_page or total
    pages = int(total / per_page)
    if total % per_page > 0:
        pages += 1

    def page_url(page_number):
        return (
            'https://mbs.example.com/module-build-service/1/module-builds/'
            '?per_page={}&page={}'.format(per_page, page_number)
        )

    result = []
    offset = 0

    for page in range(1, pages + 1):
        page_result = {
            'items': module_builds[offset:offset + per_page],
            'meta': {
                'first': page_url(1), 'prev': None, 'next': None, 'last': page_url(pages),
                'total': total, 'per_page': per_page, 'pages': pages, 'page': page
            }
        }

        meta = page_result['meta']
        if page - 1 > 0:
            meta['prev'] = page_url(page - 1)
        if page + 1 <= pages:
            meta['next'] = page_url(page + 1)

        offset += per_page
        result.append(page_result)

    return result
