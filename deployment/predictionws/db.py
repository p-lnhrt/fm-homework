import json

import flask
import pandas as pd

import predictionws.bases as bases


class ModelMetadata:
    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, value)


class LocalModelMetadataDatabase(bases.AbstractModelMetadataDatabase):
    def __init__(self):
        self._db_uri = flask.current_app.config.get('MODEL_METADATA_DB')

        with open(self._db_uri, 'r') as file:
            database = json.load(file)
            self._models = [ModelMetadata(data=data) for data in database]

    def list_models(self):
        return [model.id for model in self._models]

    def get_model_metadata(self, model_id):
        metadata, *_ = [model_data for model_data in self._models if model_data.id == model_id]
        return metadata


def get_db():
    if 'db' not in flask.g:
        flask.g.db = LocalModelMetadataDatabase()
    return flask.g.db


def teardown_db(error):
    flask.g.pop('db', None)
