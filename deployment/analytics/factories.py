import analytics.bases as bases
import analytics.credit_default


class CreditDefaultFactory(bases.AbstractDataPipelineFactory):

    def create_data_validator(self):
        return analytics.credit_default.DataValidator()

    def create_data_preprocessor(self):
        return analytics.credit_default.DataPreprocessor()

    def create_predictor(self, model_file):
        return analytics.credit_default.Predictor(model_file=model_file)
