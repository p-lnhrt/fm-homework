import abc


class AbstractModelDataBase(abc.ABC):

    @abc.abstractmethod
    def query_for_path(self, model_id):
        pass

    @abc.abstractmethod
    def list_models(self):
        pass
