from .contrib import BaseResource, BackgroundJob
import json
import pandas
import tempfile
import io


class BaseReducer(BaseResource):
    fields = BaseResource.fields + ['code']
    namespace = ['reducers']

    def run(self, content=None, tframe=None, context: dict={}):
        request_data = {'context': json.dumps(context)}
        if tframe is not None:
            request_data['store'] = tframe.object_id

        request_kwargs = dict(data=request_data)
        if content is not None:
            request_kwargs['files'] = {'content': content}

        res = self.client.session.post(self.api_path + 'run/', **request_kwargs)
        return pandas.DataFrame(res.json().get('results')), res.json().get('stderr')

    @staticmethod
    def csv_reducer(client):
        obj = BaseReducer(client, {'object_id': '6838dd2e-72be-4d6b-9656-086f8df637e2'})
        obj.sync()
        return obj

    @staticmethod
    def json_reducer(client):
        obj = BaseReducer(client, {'object_id': '8e81190e-e881-4193-8d6c-d765383757ba'})
        obj.sync()
        return obj

    @staticmethod
    def html_reducer(client):
        obj = BaseReducer(client, {'object_id': 'e0f582f6-7364-498d-b1c4-858780a488f6'})
        obj.sync()
        return obj

    @staticmethod
    def excel_reducer(client):
        obj = BaseReducer(client, {'object_id': '2c8fdb55-9594-4777-84c7-3a0de3abb65e'})
        obj.sync()
        return obj


class TFrame(BaseResource):
    fields = BaseResource.fields + ['columns']
    namespace = ['tframes']

    def from_reducer(self, reducer: BaseReducer, content=None, context: dict={}, override=False):
        request_kwargs = {'data': {
            'reducer': reducer.object_id,
            'context': json.dumps(context),
            'override': override
        }}
        if content is not None:
            request_kwargs['files'] = {'content': content}

        res = self.client.session.post(self.api_path + 'from_reducer/', **request_kwargs)
        if res.status_code == 200:
            return BackgroundJob(self.client, res.json())
        raise ValueError(res.json())

    def download_dataframe(self) -> pandas.DataFrame:
        res = self.client.session.get(self.api_path + 'dataframe_export/')
        return pandas.read_csv(io.StringIO(res.content.decode('utf-8')))

    def upload_dataframe(self, dataframe: pandas.DataFrame):
        with tempfile.NamedTemporaryFile(suffix='.csv') as temp:
            dataframe.to_csv(temp.name, index_label='Index')
            temp.seek(0)
            return self.from_reducer(BaseReducer.csv_reducer(self.client), content=temp, override=True)
