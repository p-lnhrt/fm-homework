import joblib
import os

import flask

import predictionws.bases as bases


class LocalModelWarehouse(bases.AbstractModelWarehouse):

    def __init__(self):
        self._wh_path = flask.current_app.config.get('MODEL_WAREHOUSE')

    def get_model(self, model_id):
        model_path = os.path.join(self._wh_path, '{}.joblib'.format(model_id))
        return joblib.load(model_path)


def get_warehouse():
    if 'wh' not in flask.g:
        flask.g.wh = LocalModelWarehouse()
    return flask.g.wh


def teardown_warehouse(error):
    flask.g.pop('wh', None)

