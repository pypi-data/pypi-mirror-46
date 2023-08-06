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

import mock

from tests import UrsaMajorTestCase, MockResponse, make_mbs_response
from ursa_major.mbs import MBS


class TestMBS(UrsaMajorTestCase):
    def _mock_requests_get_for_modules_list(self, url, **kwargs):
        params = kwargs.get('params', {})
        q_name = params.get('name', None)
        if q_name == 'testmodule':
            page = params.get('page', None)
            if page is None or page == '1':
                filename = 'mbs_modules_testmodule_page1.json'
            elif page == '2':
                filename = 'mbs_modules_testmodule_page2.json'
            elif page == '3':
                filename = 'mbs_modules_testmodule_page3.json'
            else:
                raise RuntimeError('Unsupported page in mock helper')
            json_data = self.load_json_from_file(filename)
            return MockResponse(json_data, 200)
        return MockResponse({}, 404)

    @mock.patch('ursa_major.mbs.requests.get')
    def test_get_modules_without_auto_next_page(self, get):
        get.return_value = mock.Mock(status_code=200)
        get.return_value.json.side_effect = make_mbs_response([
            # First page
            {'id': 1, 'name': 'mariadb', 'stream': '10.4'},
            {'id': 2, 'name': 'mariadb', 'stream': '10.3'},
            # Second page
            {'id': 3, 'name': 'ant', 'stream': '1.10'},
            {'id': 4, 'name': 'fish', 'stream': '3'},
            # Third page
            {'id': 5, 'name': 'ruby', 'stream': 'master'},
        ], per_page=2)

        mbs = MBS('http://mbs.example.com')
        modules = mbs.get_modules(auto_next_page=False, name='mariadb')

        expected = [
            {'id': 1, 'name': 'mariadb', 'stream': '10.4'},
            {'id': 2, 'name': 'mariadb', 'stream': '10.3'},
        ]

        self.assertEqual(modules, expected)

    @mock.patch('ursa_major.mbs.requests.get')
    def test_get_modules_with_auto_next_page(self, get):
        get.side_effect = self._mock_requests_get_for_modules_list

        mbs = MBS('http://mbs.example.com')
        modules = mbs.get_modules(auto_next_page=True, name='testmodule')

        data1 = self.load_json_from_file('mbs_modules_testmodule_page1.json')
        data2 = self.load_json_from_file('mbs_modules_testmodule_page2.json')
        data3 = self.load_json_from_file('mbs_modules_testmodule_page3.json')
        expected = []
        expected.extend(data1['items'])
        expected.extend(data2['items'])
        expected.extend(data3['items'])

        self.assertEqual(modules, expected)

    @mock.patch('ursa_major.mbs.requests.get')
    def test_get_module_mmd(self, get):

        testmodule_file = 'mbs_testmodule_604_verbose.json'
        resp_data = self.load_json_from_file(testmodule_file)
        get.return_value = MockResponse(resp_data, 200)

        mbs = MBS('http://mbs.example.com')
        mmd = mbs.get_module_mmd(604)
        self.assertEqual(mmd.peek_name(), 'testmodule')
        self.assertEqual(mmd.peek_stream(), 'rhel-8.0')
        self.assertEqual(str(mmd.peek_version()), '20180507102412')
        self.assertEqual(mmd.peek_context(), 'c2c572ec')

    @mock.patch('ursa_major.mbs.requests.get')
    def test_module_has_requires(self, get):

        testmodule_file = 'mbs_testmodule_604_verbose.json'
        resp_data = self.load_json_from_file(testmodule_file)
        get.return_value = MockResponse(resp_data, 200)

        mbs = MBS('http://mbs.example.com')
        self.assertTrue(mbs.module_has_requires(604, {'platform': 'el8'}))

    @mock.patch('ursa_major.mbs.requests.get')
    def test_module_not_has_requires(self, get):

        testmodule_file = 'mbs_testmodule_604_verbose.json'
        resp_data = self.load_json_from_file(testmodule_file)
        get.return_value = MockResponse(resp_data, 200)

        mbs = MBS('http://mbs.example.com')
        self.assertFalse(mbs.module_has_requires(604, {'platform': 'f28'}))

    def test_get_modules(self):
        mbs_resp_data = self.load_json_from_file('test_get_modules_with_requires.json')
        mbs = MBS('http://mbs.example.com')

        # name, stream, requires, buildrequires, expected module build ids
        test_matrix = (
            ('testmodule', 'rhel-8.0', None, None, [604, 605]),
            ('testmodule', 'rhel-8.0', {'platform': 'el8'}, None, [604, 605]),
            ('testmodule', 'rhel-8.0', None, {'platform': 'el8'}, [604]),
            ('testmodule', 'rhel-8.0', {'platform': 'el8'}, {'platform': 'el8'}, [604]),
            ('testmodule', 'rhel-8.0', {'platform': 'f30'}, None, []),
            ('testmodule', 'rhel-8.0', {'platform': 'f30'}, {'platform': 'f30'}, []),
            ('testmodule', 'rhel-8.0', None, {'platform': 'f30'}, []),
        )

        for name, stream, requires, buildrequires, expected_build_ids in test_matrix:
            with mock.patch('ursa_major.mbs.requests.get') as get:
                get.return_value = MockResponse(mbs_resp_data, 200)

                module_builds = mbs.get_modules(
                    name=name,
                    stream=stream,
                    requires=requires,
                    buildrequires=buildrequires)

                params = {'name': name, 'stream': stream}
                if requires or buildrequires:
                    params['verbose'] = 'true'
                get.assert_called_once_with(mbs.module_builds_api_url, params=params)

                build_ids = sorted(build_info['id'] for build_info in module_builds)
                assert expected_build_ids == build_ids
