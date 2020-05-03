import joblib

import predictionws.exceptions as exceptions

def build_model_from_id(db_client, model_id):
    model_path = db_client.query_for_path(model_id=model_id)
    if not model_path:
        raise exceptions.ModelNotFoundException
    return joblib.load(model_path)

