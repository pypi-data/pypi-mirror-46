class DummyModelBase:
    def __init__(self, model_config):
        self.config = model_config


class DummyModel(DummyModelBase):

    def build_model(self):
        pass

    def get_prediction(self, input_features):
        pass

    def get_stats(self):
        pass


class DummyModelWithoutBuildModelMethod(DummyModelBase):
    def get_prediction(self, input_features):
        pass

    def get_stats(self):
        pass


class DummyModelWithoutGetPredictionMethod(DummyModelBase):
    def build_model(self):
        pass

    def get_stats(self):
        pass
