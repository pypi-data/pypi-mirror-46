# Copyright (c) 2017 RedHat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_config import cfg
import webob.exc

from glance.common import wsgi
from glance.i18n import _


CONF = cfg.CONF


class InfoController(object):
    def get_image_import(self, req):
        # TODO(jokke): Will be removed after the config option
        # is removed. (deprecated)
        if not CONF.enable_image_import:
            msg = _("Image import is not supported at this site.")
            raise webob.exc.HTTPNotFound(explanation=msg)

        # TODO(jokke): All the rest of the boundaries should be implemented.
        # TODO(jokke): Once we have the rest of the methods implemented
        # the value should be inherited from the CONF rather than hard-
        # coded.
        import_methods = {
            'description': 'Import methods available.',
            'type': 'array',
            'value': ['glance-direct']
        }

        return {
            'import-methods': import_methods
        }


def create_resource():
    return wsgi.Resource(InfoController())
