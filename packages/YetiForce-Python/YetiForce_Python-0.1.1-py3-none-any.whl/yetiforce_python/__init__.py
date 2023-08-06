import requests


class YetiForceAPIException(Exception):

    def __init__(self, *args, message=None, code=None):
        super(YetiForceAPIException, self).__init__(*args)

        self.message = message
        self.code = code

    def __str__(self):
        ret = 'Operation unsuccessful'
        if self.message is not None:
            ret += ': {}'.format(self.message)
        if self.code is not None:
            ret += ' (code: {})'.format(self.code)

        return ret

    def __repr__(self):
        return self.__str__()


class YetiForceAPI(object):
    WEBSERVICE = 'webservice'

    class Module(object):

        def __init__(self, api, name):
            self._api = api
            self._name = name

        def __str__(self):
            return 'Module: {}, {}'.format(self._name, self._api)

        def __repr__(self):
            return self.__str__()

        def get_list(self, limit=1000, offset=0, fields=None):
            return self._api.get_list(self._name, limit=limit, offset=offset,
                                      fields=fields)

        def fields(self):
            return self._api.fields(self._name)

        def privileges(self):
            return self._api.privileges(self._name)

        def hierarchy(self):
            return self._api.hierarchy(self._name)

        def get(self, record_id):
            return self._api.get_record(self._name, record_id)

        def delete(self, record_id):
            return self._api.delete_record(self._name, record_id)

        def create(self, data):
            return self._api.create_record(self._name, data)

        def update(self, record_id, data):
            return self._api.update_record(self._name, record_id, data)

    def __init__(self, url, ws_user, ws_pass, ws_key, username, password):
        self._ws_url = url.rstrip('/')
        self._ws_auth = (ws_user, ws_pass)
        self._ws_key = ws_key

        self._username = username
        self._password = password

        self._session = None
        self._modules = None

    def __str__(self):
        return 'YetiForce API (url: {}, WS: {}, User: {})'.format(
            self._ws_url, self._ws_auth[0], self._username)

    def __repr__(self):
        return self.__str__()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def __getattr__(self, item):
        if not self.is_logged_in:
            raise YetiForceAPIException('Not logged in')

        if item not in self._modules:
            raise YetiForceAPIException(
                message='Module {} not available'.format(item))

        module = self.Module(self, item)
        setattr(self, item, module)

        return module

    def _request(self, method='GET', module=None, action=None, params=None,
                 data=None, json=None, extra_headers=None):
        if not self.is_logged_in and action != 'Login':
            raise YetiForceAPIException('Not logged in')

        headers = dict(self._session.headers)
        headers.update(extra_headers or {})

        url = '/'.join([x for x in
                        [self._ws_url, self.WEBSERVICE, module, action]
                        if x is not None])
        response = self._session.request(method=method, url=url, params=params,
                                         data=data, json=json, headers=headers)
        if response.status_code >= 500:
            raise YetiForceAPIException(
                message='Could not process request: {}'.format(
                    response.status_code))

        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            raise YetiForceAPIException(
                message='Could not process request: {}'.format(
                    response.status_code))

        if not data['status']:
            raise YetiForceAPIException(message=data['error']['message'],
                                        code=data['error']['code'])

        return data['result']

    @property
    def is_logged_in(self):
        if self._session is None:
            return False

        return 'X-Token' in self._session.headers

    @property
    def modules(self):
        return self._modules

    def login(self):
        if self.is_logged_in:
            self.logout()

        self._session = requests.Session()
        self._session.headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'yeti-rest-api/1.0',
            'X-ENCRYPTED': '0',
            'X-API-KEY': self._ws_key,
        }
        self._session.auth = self._ws_auth

        payload = {
            'userName': self._username,
            'password': self._password,
            'params': [],
        }

        result = self._request(method='POST', module='Users', action='Login',
                               json=payload)

        self._session.headers['X-Token'] = result.pop('token')
        self._modules = list(self._list('Modules').keys())

        return result

    def logout(self):
        result = True
        if self.is_logged_in:
            result = self._request(method='PUT', module='Users',
                                   action='Logout')

        self._session = None
        self._modules = None
        return result

    def _list(self, module, action=None, limit=None, offset=None, fields=None):
        extra_headers = {}
        if isinstance(limit, int):
            extra_headers['X-ROW-LIMIT'] = str(limit)
        if isinstance(offset, int):
            extra_headers['X-ROW-OFFSET'] = str(offset)
        if isinstance(fields, (list, tuple)):
            extra_headers['X-FIELDS'] = str(list(fields))

        return self._request(module=module, action=action,
                             extra_headers=extra_headers)

    def list_modules(self):
        return self._list('Modules')

    def list_methods(self):
        return self._list('Methods')

    def fields(self, module):
        return self._list(module, action='Fields')

    def privileges(self, module):
        return self._list(module, action='Privileges')

    def hierarchy(self, module):
        return self._list(module, action='Hierarchy')

    def get_list(self, module, limit=1000, offset=0, fields=None):
        return self._list(module, action='RecordsList', limit=limit,
                          offset=offset, fields=fields)

    def get_record(self, module, record_id):
        action = 'Record/{}'.format(record_id)
        try:
            return self._request(module=module, action=action)
        except YetiForceAPIException as ex:
            if ex.message == 'Record doesn\'t exist':
                raise KeyError(record_id) from ex

    def delete_record(self, module, record_id):
        action = 'Record/{}'.format(record_id)
        try:
            return self._request(method='DELETE', module=module, action=action)
        except YetiForceAPIException as ex:
            if ex.message == 'Record doesn\'t exist':
                raise KeyError(record_id) from ex

    def create_record(self, module, data):
        action = 'Record/'

        payload = dict(data)
        payload['module'] = module
        payload['action'] = 'Save'

        return self._request(method='POST', module=module, action=action,
                             json=payload)

    def update_record(self, module, record_id, data):
        action = 'Record/{}'.format(record_id)

        payload = dict(data)
        payload['module'] = module
        payload['action'] = 'Save'
        payload['record'] = record_id

        try:
            return self._request(method='PUT', module=module, action=action,
                                 json=payload)
        except YetiForceAPIException as ex:
            if ex.message == 'Record doesn\'t exist':
                raise KeyError(record_id) from ex
