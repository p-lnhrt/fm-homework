import abc


class AbstractTransformer(abc.ABC):

    @abc.abstractmethod
    def transform(self, data):
        pass


class AbstractPredictor(abc.ABC):

    @abc.abstractmethod
    def predict(self, data):
        pass


class AbstractDataPipelineFactory(abc.ABC):

    @abc.abstractmethod
    def create_data_validator(self):
        pass

    @abc.abstractmethod
    def create_data_preprocessor(self):
        pass

    @abc.abstractmethod
    def create_predictor(self, model_file):
        pass
