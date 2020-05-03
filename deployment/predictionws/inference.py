class Predictor:
    def __init__(self, pipeline_factory, model_file):
        self.factory = pipeline_factory
        self.validator = self.factory.create_data_validator()
        self.preprocessor = self.factory.create_data_preprocessor()
        self.predictor = self.factory.create_predictor(model_file=model_file)

    def predict(self, data):
        validated_data = self.validator.transform(data=data)
        preprocessed_data = self.preprocessor.transform(data=validated_data)
        return self.predictor.predict(data=preprocessed_data)