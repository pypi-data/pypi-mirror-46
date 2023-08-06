import unittest
import os
import time


class EndToEndTestCases(unittest.TestCase):
    def test_titanic_dataset(self):
        # test authentication
        from .contrib import Client

        print(os.environ.get('TERRENE_SDK_TEST_EMAIL'), os.environ.get('TERRENE_SDK_TEST_PASSWORD'))
        client = Client(os.environ.get('TERRENE_SDK_TEST_BASE_URL'))
        client.authenticate_with_email_and_password(
            os.environ.get('TERRENE_SDK_TEST_EMAIL'),
            os.environ.get('TERRENE_SDK_TEST_PASSWORD'))

        # create a new reducer to parse the titanic dataset
        from .store import BaseReducer

        reducer = client.create(BaseReducer, dict(
            name='CSV Reducer Python SDK',
            description='CSV Reducer created by the python sdk',
            code='import pandas\ncontent = pandas.read_csv(content)'))

        # test the reducer run method
        dataframe, stderr = reducer.run(open('dist/titanic.csv'))
        print(dataframe, stderr)

        time.sleep(1)
        # test if reducer notifications work
        reducer.warn('test', 'test', 'read')
        time.sleep(1)
        reducer.inform('test', 'test', 'read')

        time.sleep(1)
        # create a tframe and load the data into it
        from .store import TFrame

        tframe = client.create(TFrame, dict(
            name='Titanic dataset tframe',
            description='some test tframe'))

        background_job = tframe.from_reducer(reducer, open('dist/titanic.csv'))
        while True:
            background_job.sync()
            if background_job.progress == 100 or background_job.failed:
                break
            time.sleep(1)

        # print the loaded dataframe
        tframe_df = tframe.download_dataframe()

        # modify the tframe and upload it back
        time.sleep(3)
        tframe_df['New_Col'] = 'test'
        background_job = tframe.upload_dataframe(tframe_df)
        while True:
            background_job.sync()
            if background_job.progress == 100 or background_job.failed:
                break
            time.sleep(1)

        # create a predictive model and train it
        from .model import PredictiveModel

        time.sleep(2)
        model = client.create(PredictiveModel, dict(
            name='Titanic Predictive Model', description='Predictive Model',
            input_variables=['Age', 'Sex', 'Cabin', 'Parch'],
            output_variables=['Survived']))
        suggested_trainers = model.suggest(tframe)

        # display suggested_trainers
        print(suggested_trainers)

        time.sleep(3)
        # train model with suggested trainer
        background_job = model.train(tframe, suggested_trainers[0])
        while True:
            background_job.sync()
            if background_job.progress == 100 or background_job.failed:
                break
            time.sleep(1)

        # test predictions
        time.sleep(2)
        preds = model.predict({'Age': 12, 'Sex': 'male', 'Cabin': 'C30', 'Parch': 1})
        print(preds)

        # test batch predictions
        time.sleep(2)
        background_job = model.predict_from_tframe(tframe)
        while True:
            background_job.sync()
            if background_job.progress == 100 or background_job.failed:
                break
            time.sleep(1)

        # get the predicted tframe
        time.sleep(2)
        tframe_with_preds = tframe.download_dataframe()
        print(tframe_with_preds)

        # delete everything
        model.destroy()
        reducer.destroy()
        tframe.destroy()
