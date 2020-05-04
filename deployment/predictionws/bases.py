import abc


class AbstractModelMetadataDatabase(abc.ABC):

    @abc.abstractmethod
    def list_models(self):
        pass

    @abc.abstractmethod
    def get_model_metadata(self, model_id):
        pass


class AbstractModelWarehouse(abc.ABC):

    @abc.abstractmethod
    def get_model(self, model_id):
        pass


class AbstractPredictor(abc.ABC):

    @abc.abstractmethod
    def predict(self, data):
        pass
