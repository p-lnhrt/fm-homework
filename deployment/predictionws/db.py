import os
import re

import flask

import predictionws.bases as bases

class TrainedModel:
    def __init__(self, path, id_):
        self.path = path
        self.id = id_


class ModelStore(bases.AbstractModelDataBase):
    def __init__(self):
        self._wh_path = flask.current_app.config.get('MODEL_WAREHOUSE')
        regex = re.compile(r'\w+')
        self._models = [TrainedModel(path=os.path.join(self._wh_path, filename), id_=regex.match(filename).group())
                        for filename in os.listdir(self._wh_path)]

    def query_for_path(self, model_id):
        try:
            queried_model, *_ = [model for model in self._models if model.id == model_id]
            path = queried_model.path
        except ValueError:
            path = None
        return path

    def list_models(self):
        return [model.id for model in self._models]


def get_db():
    if 'db' not in flask.g:
        flask.g.db = ModelStore()
    return flask.g.db


def teardown_db(error):
    flask.g.pop('db', None)
