import datetime
import io
import time

from memory_profiler import profile
from swiss_common_utils.datetime.datetime_utils import format_time_length, datetime_to_millis
from swiss_python.logger.log_utils import get_logger, log_enter_and_exit

from prediction_model_wrapper.exceptions.invalid_module_path_error import InvalidModulePathError
from prediction_model_wrapper.exceptions.model_not_loaded_error import ModelNotLoadedError
from prediction_model_wrapper.trained_model_data.trained_model_data import TrainedModelData

build_model_memory_usage_stream = io.StringIO('')


def exception_error_msg(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


class PredictionModelWrapper(object):
    logger = get_logger(name='prediction_model_wrapper_logger')

    def __init__(self, model_class_fully_qualified_name, config):
        self.logger.info('Initializing prediction model wrapper object')
        self.trained_model_data = TrainedModelData()

        self.config = {}
        if config:
            self.config = config

        self.model_config = {}
        if 'model' in self.config:
            self.model_config = self.config['model']

        self.model_class_fully_qualified_name = model_class_fully_qualified_name

        self.logger.info('Initializing model object: {}'.format(self.model_class_fully_qualified_name))
        self.trained_model_data.model = self.init_model_object(
            model_class_fully_qualified_name=self.model_class_fully_qualified_name,
            model_config=self.model_config)

        self.__validate_model_class()

    def init_model_object(self, model_class_fully_qualified_name, model_config):
        try:
            # Dynamically instantiate the model with its configuration
            model_class = self.get_class(model_class_fully_qualified_name)
            return model_class(model_config)
        except Exception as e:
            self.logger.error(exception_error_msg(e))
            raise InvalidModulePathError('Failed to find module: {}'.format(self.model_class_fully_qualified_name))

    @staticmethod
    def get_class(kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    @log_enter_and_exit
    def __validate_model_class(self):
        if not hasattr(self.trained_model_data.model, 'get_prediction'):
            err = 'model class does not implement "get_prediction" method'
            self.logger.error(err)
            raise NotImplementedError(err)

        if not hasattr(self.trained_model_data.model, 'build_model'):
            err = 'model class does not implement "build_model" method'
            self.logger.error(err)
            raise NotImplementedError(err)

        if not hasattr(self.trained_model_data.model, 'get_stats'):
            warning = 'model class does not implement "get_stats" method. This is not mandatory, but can help you evaluate your model...'
            self.logger.warning(warning)

        self.logger.info('model class is valid!')

    @log_enter_and_exit
    def load(self, new_trained_model_data):

        if not new_trained_model_data:
            err = 'no valid input for loading model'
            self.logger.error(err)
            raise ModelNotLoadedError(err)

        try:
            new_model_identifier = new_trained_model_data.identifier
            if new_model_identifier == self.trained_model_data.identifier:
                self.logger.info('no change in model hash. No new model to load...')
                return False

            self.trained_model_data = new_trained_model_data

            self.__validate_model_class()
            self.logger.info('New model successfully loaded!')
            return True
        except Exception as e:
            self.logger.error(exception_error_msg(e))
            raise e

    @log_enter_and_exit
    def get_prediction(self, input_features):
        if not self.trained_model_data.model:
            msg = 'model not loaded, cannot hand predictions'
            self.logger.error(msg)
            raise ModelNotLoadedError(msg)
        else:
            try:
                self.logger.info('Getting prediction')
                self.__validate_model_class()

                prediction_result = self.trained_model_data.model.get_prediction(input_features)

                return prediction_result

            except Exception as e:
                self.logger.error(exception_error_msg(e))

    @profile(stream=build_model_memory_usage_stream)
    def __build_with_memory_profiling(self):
        self.trained_model_data.model.build_model()

    @log_enter_and_exit
    def build(self):
        self.__validate_model_class()
        build_start = int(time.time())
        self.__build_with_memory_profiling()
        build_duration = int(time.time()) - build_start
        self.logger.info('Build duration: {}'.format(format_time_length(seconds=build_duration)))
        self.trained_model_data.build_duration = build_duration
        self.trained_model_data.build_time = datetime.datetime.now()
        build_time_str = str(self.trained_model_data.build_time)
        identifier = datetime_to_millis(datetime.datetime.strptime(build_time_str, '%Y-%m-%d %H:%M:%S.%f'))
        self.trained_model_data.identifier = str(identifier)
        self.trained_model_data.memory_usage = build_model_memory_usage_stream.getvalue()

        if hasattr(self.trained_model_data.model, 'get_stats'):
            self.trained_model_data.stats = self.trained_model_data.model.get_stats()
        else:
            self.logger.warning('Model not implementing get_stats method!')

        return self.trained_model_data
