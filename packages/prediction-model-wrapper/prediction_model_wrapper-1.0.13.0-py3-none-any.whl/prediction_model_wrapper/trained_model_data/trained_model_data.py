import datetime
import pickle

from prediction_model_wrapper.exceptions.invalid_type_error import InvalidTypeError
from prediction_model_wrapper.trained_model_data.trained_model_data_keys import *


class TrainedModelData:

    def __init__(self, trained_model_data_dict=None):
        self._model = None
        self._identifier = ''
        self._build_time = ''
        self._stats = {'stats': 'not implemented'}
        self._build_duration = 0
        self._memory_usage = ''

        if trained_model_data_dict:
            if MODEL in trained_model_data_dict:
                self._model = pickle.loads(trained_model_data_dict[MODEL])
            if IDENTIFIER in trained_model_data_dict:
                self._identifier = trained_model_data_dict[IDENTIFIER]
            if BUILD_TIME in trained_model_data_dict:
                self._build_time = trained_model_data_dict[BUILD_TIME]
            if STATS in trained_model_data_dict:
                self._stats = trained_model_data_dict[STATS]
            if BUILD_DURATION in trained_model_data_dict:
                self._build_duration = trained_model_data_dict[BUILD_DURATION]
            if MEMORY_USAGE in trained_model_data_dict:
                self._memory_usage = trained_model_data_dict[MEMORY_USAGE]

    def __generate_invalid_type_error_msg(self, field_name, expected, actual):
        return 'Setting {} failed due to invalid types. Expected: {}, Actual: {}'.format(field_name, expected, actual)

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        if not isinstance(identifier, str):  # Must be a string
            raise InvalidTypeError(
                self.__generate_invalid_type_error_msg('identifier', 'str', identifier.__class__.__name__))

        self._identifier = identifier

    @property
    def build_time(self):
        return self._build_time

    @build_time.setter
    def build_time(self, build_time):
        if not isinstance(build_time, datetime.datetime):  # Must be a datetime object
            raise InvalidTypeError(
                self.__generate_invalid_type_error_msg('build_time', 'str', build_time.__class__.__name__))

        self._build_time = build_time

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, stats):
        if not isinstance(stats, dict):  # Must be a dict
            raise InvalidTypeError(
                self.__generate_invalid_type_error_msg('stats', 'str', stats.__class__.__name__))

        self._stats = stats

    @property
    def build_duration(self):
        return self._build_duration

    @build_duration.setter
    def build_duration(self, build_duration):
        self._build_duration = build_duration

    @property
    def memory_usage(self):
        return self._memory_usage

    @memory_usage.setter
    def memory_usage(self, memory_usage):
        self._memory_usage = memory_usage

    def as_dict(self):
        model = self.model
        if type(model) == 'bytes':
            model = pickle.dumps(model)
        return {
            MODEL: model,
            IDENTIFIER: self.identifier,
            BUILD_TIME: str(self.build_time),
            STATS: self.stats,
            BUILD_DURATION: self.build_duration,
            MEMORY_USAGE: self.memory_usage
        }
