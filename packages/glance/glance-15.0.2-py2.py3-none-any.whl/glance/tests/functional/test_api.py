# Copyright 2012 OpenStack Foundation
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

"""Version-independent api tests"""


import httplib2
from oslo_serialization import jsonutils
from six.moves import http_client

from glance.tests import functional

# TODO(rosmaita): all the EXPERIMENTAL stuff in this file can be ripped out
# when v2.6 becomes CURRENT in Queens


def _generate_v1_versions(url):
    v1_versions = {'versions': [
        {
            'id': 'v1.1',
            'status': 'DEPRECATED',
            'links': [{'rel': 'self', 'href': url % '1'}],
        },
        {
            'id': 'v1.0',
            'status': 'DEPRECATED',
            'links': [{'rel': 'self', 'href': url % '1'}],
        },
    ]}
    return v1_versions


def _generate_v2_versions(url, include_experimental=False):
    version_list = []
    if include_experimental:
        version_list.append(
            {
                'id': 'v2.6',
                'status': 'EXPERIMENTAL',
                'links': [{'rel': 'self', 'href': url % '2'}],
            })
    version_list.extend([
        {
            'id': 'v2.5',
            'status': 'CURRENT',
            'links': [{'rel': 'self', 'href': url % '2'}],
        },
        {
            'id': 'v2.4',
            'status': 'SUPPORTED',
            'links': [{'rel': 'self', 'href': url % '2'}],
        },
        {
            'id': 'v2.3',
            'status': 'SUPPORTED',
            'links': [{'rel': 'self', 'href': url % '2'}],
        },
        {
            'id': 'v2.2',
            'status': 'SUPPORTED',
            'links': [{'rel': 'self', 'href': url % '2'}],
        },
        {
            'id': 'v2.1',
            'status': 'SUPPORTED',
            'links': [{'rel': 'self', 'href': url % '2'}],
        },
        {
            'id': 'v2.0',
            'status': 'SUPPORTED',
            'links': [{'rel': 'self', 'href': url % '2'}],
        }
    ])
    v2_versions = {'versions': version_list}
    return v2_versions


def _generate_all_versions(url, include_experimental=False):
    v1 = _generate_v1_versions(url)
    v2 = _generate_v2_versions(url, include_experimental)
    all_versions = {'versions': v2['versions'] + v1['versions']}
    return all_versions


class TestApiVersions(functional.FunctionalTest):

    def test_version_configurations(self):
        """Test that versioning is handled properly through all channels"""
        # v1 and v2 api enabled
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = _generate_all_versions(url)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(versions, content)

    def test_version_configurations_EXPERIMENTAL(self):
        """Test that versioning is handled properly through all channels"""
        self.api_server.enable_v1_api = True
        self.api_server.enable_v2_api = True
        self.api_server.enable_image_import = True
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = _generate_all_versions(url, include_experimental=True)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(versions, content)

    def test_v2_api_configuration(self):
        self.api_server.enable_v1_api = False
        self.api_server.enable_v2_api = True
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = _generate_v2_versions(url)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(versions, content)

    def test_v2_api_configuration_EXPERIMENTAL(self):
        self.api_server.enable_v1_api = False
        self.api_server.enable_v2_api = True
        self.api_server.enable_image_import = True
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = _generate_v2_versions(url, include_experimental=True)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(versions, content)

    def test_v1_api_configuration(self):
        self.api_server.enable_v1_api = True
        self.api_server.enable_v2_api = False
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = _generate_v1_versions(url)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(versions, content)

    def test_v1_api_configuration_EXPERIMENTAL(self):
        # enabling image import should have no effect, but
        # nothing else should blow up, either
        self.api_server.enable_v1_api = True
        self.api_server.enable_v2_api = False
        self.api_server.enable_image_import = True
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        versions = _generate_v1_versions(url)

        # Verify version choices returned.
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(versions, content)


class TestApiPaths(functional.FunctionalTest):
    def setUp(self):
        super(TestApiPaths, self).setUp()
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        self.versions = _generate_all_versions(url)
        images = {'images': []}
        self.images_json = jsonutils.dumps(images)

    def test_get_root_path(self):
        """Assert GET / with `no Accept:` header.
        Verify version choices returned.
        Bug lp:803260  no Accept header causes a 500 in glance-api
        """
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_images_path(self):
        """Assert GET /images with `no Accept:` header.
        Verify version choices returned.
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v1_images_path(self):
        """GET /v1/images with `no Accept:` header.
        Verify empty images list returned.
        """
        path = 'http://%s:%d/v1/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.OK, response.status)

    def test_get_root_path_with_unknown_header(self):
        """Assert GET / with Accept: unknown header
        Verify version choices returned. Verify message in API log about
        unknown accept header.
        """
        path = 'http://%s:%d/' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'unknown'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_root_path_with_openstack_header(self):
        """Assert GET / with an Accept: application/vnd.openstack.images-v1
        Verify empty image list returned
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v1'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.OK, response.status)
        self.assertEqual(self.images_json, content.decode())

    def test_get_images_path_with_openstack_header(self):
        """Assert GET /images with a
        `Accept: application/vnd.openstack.compute-v1` header.
        Verify version choices returned. Verify message in API log
        about unknown accept header.
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.compute-v1'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v10_images_path(self):
        """Assert GET /v1.0/images with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/v1.a/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)

    def test_get_v1a_images_path(self):
        """Assert GET /v1.a/images with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/v1.a/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)

    def test_get_va1_images_path(self):
        """Assert GET /va.1/images with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/va.1/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_versions_path(self):
        """Assert GET /versions with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.OK, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_versions_path_with_openstack_header(self):
        """Assert GET /versions with the
        `Accept: application/vnd.openstack.images-v1` header.
        Verify version choices returned.
        """
        path = 'http://%s:%d/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v1'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.OK, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v1_versions_path(self):
        """Assert GET /v1/versions with `no Accept:` header
        Verify 404 returned
        """
        path = 'http://%s:%d/v1/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.NOT_FOUND, response.status)

    def test_get_versions_choices(self):
        """Verify version choices returned"""
        path = 'http://%s:%d/v10' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_images_path_with_openstack_v2_header(self):
        """Assert GET /images with a
        `Accept: application/vnd.openstack.compute-v2` header.
        Verify version choices returned. Verify message in API log
        about unknown version in accept header.
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v10'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v12_images_path(self):
        """Assert GET /v1.2/images with `no Accept:` header
        Verify version choices returned
        """
        path = 'http://%s:%d/v1.2/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)


# NOTE(rosmaita): yes, this is a lot of duplicated code from the above
# class, but it will be much easier to rip out in Queens if we simply
# do a copy-pasta now
class TestApiPathsEXPERIMENTAL(functional.FunctionalTest):
    def setUp(self):
        super(TestApiPathsEXPERIMENTAL, self).setUp()
        self.api_server.enable_image_import = True
        self.start_servers(**self.__dict__.copy())

        url = 'http://127.0.0.1:%d/v%%s/' % self.api_port
        self.versions = _generate_all_versions(url, include_experimental=True)
        images = {'images': []}
        self.images_json = jsonutils.dumps(images)

    def test_get_root_path(self):
        """Assert GET / with `no Accept:` header.
        Verify version choices returned.
        Bug lp:803260  no Accept header causes a 500 in glance-api
        """
        path = 'http://%s:%d' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_images_path(self):
        """Assert GET /images with `no Accept:` header.
        Verify version choices returned.
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v1_images_path(self):
        """GET /v1/images with `no Accept:` header.
        Verify empty images list returned.
        """
        path = 'http://%s:%d/v1/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.OK, response.status)

    def test_get_root_path_with_unknown_header(self):
        """Assert GET / with Accept: unknown header
        Verify version choices returned. Verify message in API log about
        unknown accept header.
        """
        path = 'http://%s:%d/' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'unknown'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_root_path_with_openstack_header(self):
        """Assert GET / with an Accept: application/vnd.openstack.images-v1
        Verify empty image list returned
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v1'}
        response, content = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.OK, response.status)
        self.assertEqual(self.images_json, content.decode())

    def test_get_images_path_with_openstack_header(self):
        """Assert GET /images with a
        `Accept: application/vnd.openstack.compute-v1` header.
        Verify version choices returned. Verify message in API log
        about unknown accept header.
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.compute-v1'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v10_images_path(self):
        """Assert GET /v1.0/images with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/v1.a/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)

    def test_get_v1a_images_path(self):
        """Assert GET /v1.a/images with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/v1.a/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)

    def test_get_va1_images_path(self):
        """Assert GET /va.1/images with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/va.1/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_versions_path(self):
        """Assert GET /versions with no Accept: header
        Verify version choices returned
        """
        path = 'http://%s:%d/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.OK, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_versions_path_with_openstack_header(self):
        """Assert GET /versions with the
        `Accept: application/vnd.openstack.images-v1` header.
        Verify version choices returned.
        """
        path = 'http://%s:%d/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v1'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.OK, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v1_versions_path(self):
        """Assert GET /v1/versions with `no Accept:` header
        Verify 404 returned
        """
        path = 'http://%s:%d/v1/versions' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content = http.request(path, 'GET')
        self.assertEqual(http_client.NOT_FOUND, response.status)

    def test_get_versions_choices(self):
        """Verify version choices returned"""
        path = 'http://%s:%d/v10' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_images_path_with_openstack_v2_header(self):
        """Assert GET /images with a
        `Accept: application/vnd.openstack.compute-v2` header.
        Verify version choices returned. Verify message in API log
        about unknown version in accept header.
        """
        path = 'http://%s:%d/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        headers = {'Accept': 'application/vnd.openstack.images-v10'}
        response, content_json = http.request(path, 'GET', headers=headers)
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)

    def test_get_v12_images_path(self):
        """Assert GET /v1.2/images with `no Accept:` header
        Verify version choices returned
        """
        path = 'http://%s:%d/v1.2/images' % ('127.0.0.1', self.api_port)
        http = httplib2.Http()
        response, content_json = http.request(path, 'GET')
        self.assertEqual(http_client.MULTIPLE_CHOICES, response.status)
        content = jsonutils.loads(content_json.decode())
        self.assertEqual(self.versions, content)
