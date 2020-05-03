import flask
from flask import request as request
import pandas as pd

import analytics.factories
import predictionws.db as db
import predictionws.exceptions as exceptions
import predictionws.inference as inference
import predictionws.utils as utils

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

    single_prediction, *_ = apply_model(model_id=model_id, data=pd.DataFrame(data=[data]))
    return flask.jsonify(single_prediction)


@prediction_bp.route(rule='/outputs/<string:model_id>', methods=['POST'])
def return_outputs(model_id):
    if not request.json:
        flask.abort(400)

    data = request.json['data']

    predictions = apply_model(model_id=model_id, data=pd.DataFrame(data=data))
    return flask.jsonify({'predictions': predictions})


def apply_model(model_id, data):
    model_file = utils.build_model_from_id(db_client=db.get_db(), model_id=model_id)
    predictor = inference.Predictor(pipeline_factory=analytics.factories.CreditDefaultFactory(), model_file=model_file)
    try:
        predictions = predictor.predict(data=data)
    except exceptions.ModelNotFoundException:
        # Queried model not found
        flask.abort(404)
    return predictions


def make_public_model(model_id):
    return {'id': model_id,
            'single_input_uri': flask.url_for(endpoint='prediction.return_output', model_id=model_id, _external=True),
            'multi_input_uri': flask.url_for(endpoint='prediction.return_outputs', model_id=model_id, _external=True)}
