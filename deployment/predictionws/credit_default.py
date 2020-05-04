import predictionws.bases as bases


class Predictor(bases.AbstractPredictor):
    def __init__(self, model_file, model_metadata):
        self._model = model_file
        self.input_features = model_metadata.input_features

    def predict(self, data):
        probabilities = self._model.predict_proba(data[self.input_features])
        return [{'probability': probability} for probability in probabilities[:, 1]]
