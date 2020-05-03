import analytics.bases as bases


class Predictor(bases.AbstractPredictor):
    def __init__(self, model_file):
        self._model = model_file
        self.input_features = ['residence_history', 'installment_rate', 'existing_credits', 'dependents',
                               'checking_balance', 'savings_balance', 'personal_status', 'installment_plan']

    def predict(self, data):
        probabilities = self._model.predict_proba(data[self.input_features])
        return [{'probability': probability} for probability in probabilities[:, 1]]
