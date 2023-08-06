import requests
from urllib.parse import urljoin


class BaseUrlSession(requests.Session):
    base_url = None

    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url
        super(BaseUrlSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = self.create_url(url)
        return super(BaseUrlSession, self).request(
            method, url, *args, **kwargs)

    def create_url(self, url):
        return urljoin(self.base_url, url)


class BaseModel:
    def __init__(self, client: 'Client' = None, data: dict = None):
        self.client = client
        self.data = data

    fields = ['object_id', 'updated_at', 'created_at']
    namespace = []

    @property
    def api_path(self):
        return '/'.join(self.namespace + [self.object_id]) + '/'

    def save(self, update_fields: list = []):
        if len(update_fields == 0):
            update_fields = self.fields
        update_data = {field: self[field] for field in update_fields}

        res = self.client.session.patch(self.api_path, json=update_data)
        if res.status_code != 200:
            raise ValueError(res.json())

    def sync(self):
        res = self.client.session.get(self.api_path)
        if res.status_code == 200:
            self.data = res.json()
        else:
            raise ValueError(res.json())

    def destroy(self):
        res = self.client.session.delete(self.api_path)
        if res.status_code != 204:
            raise ValueError(res.json())

    def __getattribute__(self, name):
        if name != 'fields' and name in self.fields:
            return self.data.get(name)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.fields:
            self.data[name] = value
            return None
        return super().__setattr__(name, value)


class BaseResource(BaseModel):
    fields = BaseModel.fields + [
        'name', 'description', 'tags', 'permissions', 'public', 'tags',
        'access_level', 'read_access', 'write_access', 'execute_access']

    def _notify(self, subject: str, content: str, target: str, severity: str):
        res = self.client.session.post(self.api_path + 'notify/', json=dict(
            subject=subject, content=content, target=target, severity=severity))
        if res.status_code != 200:
            open('index.html', 'w').writelines(res.text.split('.'))
            raise ValueError(res.json())

    def warn(self, subject: str, content: str, target: str):
        self._notify(subject, content, target, 'warn')

    def inform(self, subject: str, content: str, target: str):
        self._notify(subject, content, target, 'info')


class BaseResourcePermission(BaseModel):
    namespace = ['permissions']
    fields = BaseModel.fields + ['read', 'write', 'execute', 'user', 'write_access', 'resource']


class BackgroundJob(BaseModel):
    namespace = ['jobs']
    fields = BaseModel.fields + [
        'name', 'progress', 'resources', 'initiator',
        'failed', 'running_time', 'results']


class Client:
    current_user: 'User'
    session: BaseUrlSession

    def __init__(self, base_url: str):
        self.session = BaseUrlSession(base_url)

    def authenticate_with_token(self, token: str, method: str = 'JWT'):
        self.session.headers = {'Authorization': '{} {}'.format(method, token)}

    def authenticate_with_email_and_password(self, email: str, password: str):
        from .auth import User

        res = self.session.post('users/actions/login/obtain-token/', {'email': email, 'password': password})
        if res.status_code == 200:
            self.session.headers = {'Authorization': 'JWT {}'.format(res.json().get('token'))}
            self.current_user = User(client=self, data=res.json().get('user'))
            return self.current_user
        raise PermissionError(res.json())

    def create(self, model_class: BaseModel.__class__, data: dict):
        res = self.session.post('/'.join(model_class.namespace) + '/', json=data)
        if res.status_code == 201:
            return model_class(self, res.json())
        raise ValueError(res.json())

    def list(self, model_class: BaseModel.__class__, page: int = 1, params: dict = {}):
        request_url = '/'.join(model_class.namespace) + '/?page={}'.format(page)
        for key, value in params.items():
            request_url += '&{}={}'.format(key, value)

        res = self.session.get(request_url)
        if res.status_code == 200:
            results = []
            for result in res.json().get('results'):
                results.append(model_class(self, result))
            return results
        raise ValueError(res.json())
