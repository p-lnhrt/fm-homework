import flask
from flask import request as request
import pandas as pd

import predictionws.predictor
import predictionws.db as db
import predictionws.warehouse as wh

model_bp = flask.Blueprint(name='model', import_name=__name__)
prediction_bp = flask.Blueprint(name='prediction', import_name=__name__)


@model_bp.route(rule='/models', methods=['GET'])
def list_models():
    db_client = db.get_db()
    return flask.jsonify({'models': [make_public_model(model_id=model_id) for model_id in db_client.list_models()]})


@prediction_bp.route(rule='/output/<string:model_id>', methods=['POST'])
def return_output(model_id):
    if not request.json:
        flask.abort(400)

    data = request.json

    model_file = get_model_file(model_id=model_id)
    model_metadata = get_model_metadata(model_id=model_id)
    predictor = predictionws.predictor.Predictor(model_file=model_file, model_metadata=model_metadata)

    single_prediction, *_ = predictor.predict(data=pd.DataFrame(data=[data]))
    single_prediction.update({'model_id': model_metadata.id})
    return flask.jsonify(single_prediction)


@prediction_bp.route(rule='/outputs/<string:model_id>', methods=['POST'])
def return_outputs(model_id):
    if not request.json:
        flask.abort(400)

    data = request.json['data']

    model_file = get_model_file(model_id=model_id)
    model_metadata = get_model_metadata(model_id=model_id)
    predictor = predictionws.predictor.Predictor(model_file=model_file, model_metadata=model_metadata)
    predictions = predictor.predict(data=pd.DataFrame(data=data))

    return flask.jsonify({'model_id': model_metadata.id, 'predictions': predictions})


def get_model_file(model_id):
    wh_client = wh.get_warehouse()
    try:
        model_file = wh_client.get_model(model_id=model_id)
    except FileNotFoundError:
        # Queried model not found
        flask.abort(404)

    return model_file


def get_model_metadata(model_id):
    db_client = db.get_db()
    try:
        model_metadata = db_client.get_model_metadata(model_id=model_id)
    except ValueError:
        # Queried model metadata not found
        flask.abort(404)

    return model_metadata


def make_public_model(model_id):
    return {'id': model_id,
            'single_input_uri': flask.url_for(endpoint='prediction.return_output', model_id=model_id, _external=True),
            'multi_input_uri': flask.url_for(endpoint='prediction.return_outputs', model_id=model_id, _external=True)}
