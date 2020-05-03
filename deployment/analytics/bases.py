import abc


class AbstractPredictor(abc.ABC):

    @abc.abstractmethod
    def predict(self, data):
        pass
