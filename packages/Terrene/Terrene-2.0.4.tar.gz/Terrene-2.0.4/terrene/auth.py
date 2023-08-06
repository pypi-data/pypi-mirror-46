from .contrib import BaseModel


class User(BaseModel):
    fields = BaseModel.fields + [
        'first_name', 'last_name', 'email', 'password',
        'is_admin', 'is_active', 'is_staff', 'roles',
        'days_since_last_active']
    namespace = ['users']


class UserAlertSettings(BaseModel):
    fields = BaseModel.fields + ['user', 'emails', 'webhooks']
    namespace = ['users', 'alert-settings']

    def test(self):
        self.client.session.post(self.api_path + 'test/')
