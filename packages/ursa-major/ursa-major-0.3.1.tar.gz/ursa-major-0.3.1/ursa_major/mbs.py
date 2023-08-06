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

import requests
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

from ursa_major.utils import load_mmd, mmd_has_requires, mmd_has_buildrequires


class MBS(object):
    def __init__(self, server_url, api_version=1):
        self.server_url = server_url

        self.module_builds_api_url = (
            self.server_url.rstrip('/') +
            '/module-build-service/{!s}/module-builds/'.format(api_version))

    def _get_modules(self, auto_next_page=True, **params):
        """
        Query MBS modules with specified query parameters.

        :param auto_next_page: read next page items automatically if True
        :param params: query parameters in keyword arguments
        :return: a list of modules
        """
        resp = requests.get(self.module_builds_api_url, params=params)
        if resp.status_code != 200:
            resp.raise_for_status()

        resp_data = resp.json()

        modules = resp_data['items']
        if not auto_next_page:
            return modules

        next_page = resp_data['meta'].get('next', None)
        if next_page is not None:
            parsed_url = urlparse.urlparse(next_page)
            params = dict(urlparse.parse_qsl(parsed_url.query))
            next_modules = self.get_modules(auto_next_page=True, **params)
            modules.extend(next_modules)

        return modules

    def get_module_mmd(self, build_id):
        """
        Create and return Modulemd.Module object for a module build.

        :param build_id: module build id
        :return: Modulemd.Module object
        """
        module_url = self.module_builds_api_url + str(build_id)
        params = {'verbose': 'true'}
        resp = requests.get(module_url, params=params)
        if resp.status_code != 200:
            resp.raise_for_status()

        module = resp.json()
        mmd = load_mmd(module['modulemd'])
        return mmd

    def module_has_requires(self, build_id, requires):
        """
        Check whether a module has requires.

        :param build_id: module build id
        :param requires: dict of requires, example:
            {'platform': 'f28', 'python3': 'master'}
        :return: True or False
        """
        mmd = self.get_module_mmd(build_id)
        return mmd_has_requires(mmd, requires)

    def get_modules(self, **kwargs):
        """
        Query MBS modules with specified query parameters.

        :param dict kwargs: query parameters in keyword arguments for listing
            module builds. Modules can be filtered by either requires or
            buildrequires or both by passing ``requires`` and ``buildrequires``,
            which accepts a mapping containing requirements, for example,
            ``{"platform": "f30"}``.
        :return: a list of mappings each of them presents a module returned
            from MBS without modified.
        :rtype: list[dict]
        """
        # MBS does not support filtering module builds based on requires and
        # buildrequires. Pop either of them and filter modules later by
        # ourselves.
        requires = kwargs.pop('requires', None)
        buildrequires = kwargs.pop('buildrequires', None)
        auto_next_page = kwargs.pop('auto_next_page', False)

        inspect_modulemd = False
        if requires or buildrequires:
            inspect_modulemd = True

        # we need modulemd in result, so set verbose to true
        if inspect_modulemd:
            kwargs.update({'verbose': 'true'})

        modules = self._get_modules(auto_next_page=auto_next_page, **kwargs)

        if inspect_modulemd:
            matched = []
            for module in modules:
                mmd = load_mmd(module['modulemd'])
                b = True
                if requires:
                    b = b and mmd_has_requires(mmd, requires)
                if buildrequires:
                    b = b and mmd_has_buildrequires(mmd, buildrequires)
                if b:
                    matched.append(module)
            return matched

        return modules
