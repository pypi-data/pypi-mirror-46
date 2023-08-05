# Copyright 2012 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_serialization import jsonutils
from six.moves import http_client as http
import webob

from glance.api.middleware import version_negotiation
from glance.api import versions
from glance.common.wsgi import Request as WsgiRequest
from glance.tests.unit import base


# NOTE(rosmaita): rip out all the EXPERIMENTAL stuff when 2.6 becomes
# CURRENT in Queens (or figure out a better way to write these tests!)

class VersionsTest(base.IsolatedUnitTest):

    """Test the version information returned from the API service."""

    def _get_versions_list(self, url):
        versions = [
            {
                'id': 'v2.5',
                'status': 'CURRENT',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            },
            {
                'id': 'v2.4',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            },
            {
                'id': 'v2.3',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            },
            {
                'id': 'v2.2',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            },
            {
                'id': 'v2.1',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            },
            {
                'id': 'v2.0',
                'status': 'SUPPORTED',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            },
            {
                'id': 'v1.1',
                'status': 'DEPRECATED',
                'links': [{'rel': 'self',
                           'href': '%s/v1/' % url}],
            },
            {
                'id': 'v1.0',
                'status': 'DEPRECATED',
                'links': [{'rel': 'self',
                           'href': '%s/v1/' % url}],
            },
        ]
        return versions

    def _get_versions_list_experimental(self, url):
        vplus = [
            {
                'id': 'v2.6',
                'status': 'EXPERIMENTAL',
                'links': [{'rel': 'self',
                           'href': '%s/v2/' % url}],
            }] + self._get_versions_list(url)
        return vplus

    def test_get_version_list(self):
        req = webob.Request.blank('/', base_url='http://127.0.0.1:9292/')
        req.accept = 'application/json'
        self.config(bind_host='127.0.0.1', bind_port=9292)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list('http://127.0.0.1:9292')
        self.assertEqual(expected, results)

    def test_get_version_list_EXPERIMENTAL(self):
        req = webob.Request.blank('/', base_url='http://127.0.0.1:9292/')
        req.accept = 'application/json'
        self.config(bind_host='127.0.0.1', bind_port=9292,
                    enable_image_import=True)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list_experimental(
            'http://127.0.0.1:9292')
        self.assertEqual(expected, results)

    def test_get_version_list_public_endpoint(self):
        req = webob.Request.blank('/', base_url='http://127.0.0.1:9292/')
        req.accept = 'application/json'
        self.config(bind_host='127.0.0.1', bind_port=9292,
                    public_endpoint='https://example.com:9292')
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list('https://example.com:9292')
        self.assertEqual(expected, results)

    def test_get_version_list_public_endpoint_EXPERIMENTAL(self):
        req = webob.Request.blank('/', base_url='http://127.0.0.1:9292/')
        req.accept = 'application/json'
        self.config(bind_host='127.0.0.1', bind_port=9292,
                    public_endpoint='https://example.com:9292',
                    enable_image_import=True)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list_experimental(
            'https://example.com:9292')
        self.assertEqual(expected, results)

    def test_get_version_list_secure_proxy_ssl_header(self):
        self.config(secure_proxy_ssl_header='HTTP_X_FORWARDED_PROTO')
        url = 'http://localhost:9292'
        environ = webob.request.environ_from_url(url)
        req = WsgiRequest(environ)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list(url)
        self.assertEqual(expected, results)

    def test_get_version_list_secure_proxy_ssl_header_EXPERIMENTAL(self):
        self.config(secure_proxy_ssl_header='HTTP_X_FORWARDED_PROTO',
                    enable_image_import=True)
        url = 'http://localhost:9292'
        environ = webob.request.environ_from_url(url)
        req = WsgiRequest(environ)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list_experimental(url)
        self.assertEqual(expected, results)

    def test_get_version_list_secure_proxy_ssl_header_https(self):
        self.config(secure_proxy_ssl_header='HTTP_X_FORWARDED_PROTO')
        url = 'http://localhost:9292'
        ssl_url = 'https://localhost:9292'
        environ = webob.request.environ_from_url(url)
        environ['HTTP_X_FORWARDED_PROTO'] = "https"
        req = WsgiRequest(environ)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list(ssl_url)
        self.assertEqual(expected, results)

    def test_get_version_list_secure_proxy_ssl_header_https_EXPERIMENTAL(self):
        self.config(secure_proxy_ssl_header='HTTP_X_FORWARDED_PROTO',
                    enable_image_import=True)
        url = 'http://localhost:9292'
        ssl_url = 'https://localhost:9292'
        environ = webob.request.environ_from_url(url)
        environ['HTTP_X_FORWARDED_PROTO'] = "https"
        req = WsgiRequest(environ)
        res = versions.Controller().index(req)
        self.assertEqual(http.MULTIPLE_CHOICES, res.status_int)
        self.assertEqual('application/json', res.content_type)
        results = jsonutils.loads(res.body)['versions']
        expected = self._get_versions_list_experimental(ssl_url)
        self.assertEqual(expected, results)


class VersionNegotiationTest(base.IsolatedUnitTest):

    def setUp(self):
        super(VersionNegotiationTest, self).setUp()
        self.middleware = version_negotiation.VersionNegotiationFilter(None)

    def test_request_url_v1(self):
        request = webob.Request.blank('/v1/images')
        self.middleware.process_request(request)
        self.assertEqual('/v1/images', request.path_info)

    def test_request_url_v1_0(self):
        request = webob.Request.blank('/v1.0/images')
        self.middleware.process_request(request)
        self.assertEqual('/v1/images', request.path_info)

    def test_request_url_v1_1(self):
        request = webob.Request.blank('/v1.1/images')
        self.middleware.process_request(request)
        self.assertEqual('/v1/images', request.path_info)

    def test_request_accept_v1(self):
        request = webob.Request.blank('/images')
        request.headers = {'accept': 'application/vnd.openstack.images-v1'}
        self.middleware.process_request(request)
        self.assertEqual('/v1/images', request.path_info)

    def test_request_url_v2(self):
        request = webob.Request.blank('/v2/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_0(self):
        request = webob.Request.blank('/v2.0/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_1(self):
        request = webob.Request.blank('/v2.1/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_2(self):
        request = webob.Request.blank('/v2.2/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_3(self):
        request = webob.Request.blank('/v2.3/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_4(self):
        request = webob.Request.blank('/v2.4/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_5(self):
        request = webob.Request.blank('/v2.5/images')
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_6_unsupported(self):
        request = webob.Request.blank('/v2.6/images')
        resp = self.middleware.process_request(request)
        self.assertIsInstance(resp, versions.Controller)

    def test_request_url_v2_6_EXPERIMENTAL(self):
        request = webob.Request.blank('/v2.6/images')
        self.config(enable_image_import=True)
        self.middleware.process_request(request)
        self.assertEqual('/v2/images', request.path_info)

    def test_request_url_v2_7_unsupported(self):
        request = webob.Request.blank('/v2.7/images')
        resp = self.middleware.process_request(request)
        self.assertIsInstance(resp, versions.Controller)

    def test_request_url_v2_7_unsupported_EXPERIMENTAL(self):
        request = webob.Request.blank('/v2.7/images')
        self.config(enable_image_import=True)
        resp = self.middleware.process_request(request)
        self.assertIsInstance(resp, versions.Controller)

    def test_request_url_v3_unsupported(self):
        request = webob.Request.blank('/v3/images')
        resp = self.middleware.process_request(request)
        self.assertIsInstance(resp, versions.Controller)

    def test_request_url_v3_unsupported_EXPERIMENTAL(self):
        request = webob.Request.blank('/v3/images')
        self.config(enable_image_import=True)
        resp = self.middleware.process_request(request)
        self.assertIsInstance(resp, versions.Controller)


class VersionsAndNegotiationTest(VersionNegotiationTest, VersionsTest):

    """
    Test that versions mentioned in the versions response are correctly
    negotiated.
    """

    def _get_list_of_version_ids(self, status):
        request = webob.Request.blank('/')
        request.accept = 'application/json'
        # TODO(rosmaita): remove in Queens when option is removed
        self.config(enable_image_import=True)
        response = versions.Controller().index(request)
        v_list = jsonutils.loads(response.body)['versions']
        return [v['id'] for v in v_list if v['status'] == status]

    def _assert_version_is_negotiated(self, version_id):
        request = webob.Request.blank("/%s/images" % version_id)
        # TODO(rosmaita): remove in Queens when option is removed
        self.config(enable_image_import=True)
        self.middleware.process_request(request)
        major = version_id.split('.', 1)[0]
        expected = "/%s/images" % major
        self.assertEqual(expected, request.path_info)

    def test_current_is_negotiated(self):
        # NOTE(rosmaita): Bug 1609571: the versions response was correct, but
        # the negotiation had not been updated for the CURRENT version.
        to_check = self._get_list_of_version_ids('CURRENT')
        self.assertTrue(to_check)
        for version_id in to_check:
            self._assert_version_is_negotiated(version_id)

    def test_supported_is_negotiated(self):
        to_check = self._get_list_of_version_ids('SUPPORTED')
        for version_id in to_check:
            self._assert_version_is_negotiated(version_id)

    def test_deprecated_is_negotiated(self):
        to_check = self._get_list_of_version_ids('DEPRECATED')
        for version_id in to_check:
            self._assert_version_is_negotiated(version_id)

    def test_experimental_is_negotiated(self):
        to_check = self._get_list_of_version_ids('EXPERIMENTAL')
        for version_id in to_check:
            self._assert_version_is_negotiated(version_id)
