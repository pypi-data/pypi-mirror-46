from .contrib import BaseResource, BackgroundJob


class PredictiveModel(BaseResource):
    fields = BaseResource.fields + [
      'input_variables', 'output_variables', 'recent_files', 'active_file', 'feature_ranks',
      'loss', 'accuracy', 'recent_files', 'output_variable_format']
    namespace = ['models']

    def suggest(self, store, count=3):
        res = self.client.session.post(
            self.api_path + 'suggest_trainers/',
            {'count': count, 'store': store.object_id})
        if res.status_code == 200:
            return res.json().get('suggestions')
        raise ValueError(res.json())

    def train(self, store, trainer: str, epochs: int = 100):
        res = self.client.session.post(
            self.api_path + 'train/',
            {'store': store.object_id, 'trainer': trainer, 'epochs': epochs})
        if res.status_code == 200:
            return BackgroundJob(self.client, res.json())
        raise ValueError(res.json())

    def predict(self, payload):
        res = self.client.session.post(
            self.api_path + 'predict/', json={'payload': payload})
        if res.status_code == 200:
            return res.json()
        raise ValueError(res.json())

    def predict_from_tframe(self, store):
        res = self.client.session.post(self.api_path + 'predict_from_tframe/', json={'store': store.object_id})
        if res.status_code == 200:
            return BackgroundJob(self.client, res.json())
        raise ValueError(res.json())
