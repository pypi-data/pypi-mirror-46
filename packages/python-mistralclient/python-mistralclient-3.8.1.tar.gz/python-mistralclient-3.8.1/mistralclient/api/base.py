# Copyright 2013 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import copy
import json
import six

from keystoneauth1 import exceptions

urlparse = six.moves.urllib.parse


class Resource(object):
    resource_name = 'Something'
    defaults = {}

    def __init__(self, manager, data):
        self.manager = manager
        self._data = data
        self._set_defaults()
        self._set_attributes()

    def _set_defaults(self):
        for k, v in self.defaults.items():
            if k not in self._data:
                self._data[k] = v

    def _set_attributes(self):
        for k, v in self._data.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass

    def to_dict(self):
        return copy.deepcopy(self._data)

    def __str__(self):
        vals = ", ".join(["%s='%s'" % (n, v)
                          for n, v in self._data.items()])
        return "%s [%s]" % (self.resource_name, vals)


def _check_items(obj, searches):
    try:
        return all(getattr(obj, attr) == value for (attr, value) in searches)
    except AttributeError:
        return False


def extract_json(response, response_key):
    if response_key is not None:
        return get_json(response)[response_key]
    else:
        return get_json(response)


class ResourceManager(object):
    resource_class = None

    def __init__(self, http_client):
        self.http_client = http_client

    def find(self, **kwargs):
        return [i for i in self.list() if _check_items(i, kwargs.items())]

    def list(self):
        """This is an abstract method

        This is added here so that the find method gains some clarity.
        It must be implemented by the child class in order to find to work
        """
        raise NotImplementedError("abstract method list must be implemented")

    @staticmethod
    def _build_query_params(marker=None, limit=None, sort_keys=None,
                            sort_dirs=None, fields=None, filters=None,
                            scope=None, namespace=None):
        qparams = {}

        if marker:
            qparams['marker'] = marker

        if limit and limit > 0:
            qparams['limit'] = limit

        if sort_keys:
            qparams['sort_keys'] = sort_keys

        if sort_dirs:
            qparams['sort_dirs'] = sort_dirs

        if fields:
            qparams['fields'] = ",".join(fields)

        if filters:
            for name, val in filters.items():
                qparams[name] = val

        if scope:
            qparams['scope'] = scope

        if namespace:
            qparams['namespace'] = namespace

        return ("?%s" % urlparse.urlencode(list(qparams.items()))
                if qparams else "")

    def _ensure_not_empty(self, **kwargs):
        for name, value in kwargs.items():
            if value is None or (isinstance(value, str) and len(value) == 0):
                raise APIException(
                    400,
                    '%s is missing field "%s"' %
                    (self.resource_class.__name__, name)
                )

    def _copy_if_defined(self, data, **kwargs):
        for name, value in kwargs.items():
            if value is not None:
                data[name] = value

    def _create(self, url, data, response_key=None, dump_json=True):
        if dump_json:
            data = json.dumps(data)

        try:
            resp = self.http_client.post(url, data)
        except exceptions.HttpError as ex:
            self._raise_api_exception(ex.response)

        if resp.status_code != 201:
            self._raise_api_exception(resp)

        return self.resource_class(self, extract_json(resp, response_key))

    def _update(self, url, data, response_key=None, dump_json=True):
        if dump_json:
            data = json.dumps(data)

        try:
            resp = self.http_client.put(url, data)
        except exceptions.HttpError as ex:
            self._raise_api_exception(ex.response)

        if resp.status_code != 200:
            self._raise_api_exception(resp)

        return self.resource_class(self, extract_json(resp, response_key))

    def _list(self, url, response_key=None):
        try:
            resp = self.http_client.get(url)
        except exceptions.HttpError as ex:
            self._raise_api_exception(ex.response)

        if resp.status_code != 200:
            self._raise_api_exception(resp)

        return [self.resource_class(self, resource_data)
                for resource_data in extract_json(resp, response_key)]

    def _get(self, url, response_key=None):
        try:
            resp = self.http_client.get(url)
        except exceptions.HttpError as ex:
            self._raise_api_exception(ex.response)

        if resp.status_code == 200:
            return self.resource_class(self, extract_json(resp, response_key))
        else:
            self._raise_api_exception(resp)

    def _delete(self, url):
        try:
            resp = self.http_client.delete(url)
        except exceptions.HttpError as ex:
            self._raise_api_exception(ex.response)

        if resp.status_code != 204:
            self._raise_api_exception(resp)

    def _plurify_resource_name(self):
        return self.resource_class.resource_name + 's'

    def _raise_api_exception(self, resp):
        try:
            error_data = (resp.headers.get("Server-Error-Message", None) or
                          get_json(resp).get("faultstring"))
        except ValueError:
            error_data = resp.content
        raise APIException(error_code=resp.status_code,
                           error_message=error_data)


def get_json(response):
    """Gets JSON representation of response.

    This method provided backward compatibility with old versions
    of requests library.
    """
    json_field_or_function = getattr(response, 'json', None)

    if callable(json_field_or_function):
        return response.json()
    else:
        return json.loads(response.content)


class APIException(Exception):
    def __init__(self, error_code=None, error_message=None):
        super(APIException, self).__init__(error_message)
        self.error_code = error_code
        self.error_message = error_message
