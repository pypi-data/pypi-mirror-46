import copy
import time
from unittest import TestCase
from unittest.mock import patch

from prediction_model_wrapper.exceptions.model_not_loaded_error import ModelNotLoadedError
from prediction_model_wrapper.exceptions.invalid_module_path_error import InvalidModulePathError
from prediction_model_wrapper.trained_model_data.trained_model_data import TrainedModelData
from prediction_model_wrapper.wrapper.prediction_model_wrapper import PredictionModelWrapper
from tests.dummy_objects import DummyModel, DummyModelWithoutBuildModelMethod

config = {
    'model': {
        # DATA_SERVICE_URL: 'https://reporting-production.swiss-iil.intel.com/reportingquerierformatter',
        # REPORTED_USER_NAME: 'RuntimePredictionModel_tests',
        # TRAIN_DATA_TIME_RANGE: '2m',
        # POOL_MASTER: 'iil_vp_tiers',
        # MIN_LONG_JOB_RUNTIME: '20m',
        # # CONSIDER_ONLY_X_OTHER_JOB: 3,
        # CLASSIFIER_MAX_ITER: 5000,
        # SHORT_JOB_CERTAINTY: 0.95,
        # USED_FIELDS_AS_INPUT: 'user,qslot,cmdname,class,queue,task,classreservation',
        # USED_FIELD_AS_OUTPUT: 'wtime'
    }
}


class TestPredictionModelWrapper(TestCase):

    def __exception_error_msg(self, e):
        return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))

    def setUp(cls):
        cls.wrapper = PredictionModelWrapper(
            model_class_fully_qualified_name='tests.dummy_objects.DummyModel',
            config=config)

    def test_model_init_when_model_not_exist(self):
        self.assertRaises(InvalidModulePathError, PredictionModelWrapper, 'tests.non_existing_model', {})

    def test_model_init_with_invalid_model(self):
        self.assertRaises(NotImplementedError, PredictionModelWrapper,
                          'tests.dummy_objects.DummyModelWithoutBuildModelMethod', {})
        self.assertRaises(NotImplementedError, PredictionModelWrapper,
                          'tests.dummy_objects.DummyModelWithoutGetPredictionMethod', {})

    def test_wrapper_build_model(self):
        try:
            with patch.object(DummyModel, 'build_model') as mock_build_model:
                def my_sleep():
                    time.sleep(1.1)

                mock_build_model.side_effect = my_sleep
                with patch.object(DummyModel, 'get_stats') as mock_get_stats:
                    mock_get_stats.return_value = {'stats': 'test get stats'}

                    self.model_data = self.wrapper.build()

                    self.assertEqual(mock_build_model.call_count, 1)
                    self.assertEqual(mock_get_stats.call_count, 1)

                    self.assertIsNotNone(self.model_data, msg='Model data is None!')
                    self.assertIsNotNone(self.model_data.model, msg='Model is None!')
                    self.assertTrue(self.model_data.identifier != '', msg='Model identifier is empty')
                    self.assertTrue(self.model_data.build_time != '', msg='Build time is empty')
                    self.assertTrue(self.model_data.stats != {'stats': 'not implemented'},
                                    msg='Model stats not implemented!')
                    self.assertTrue(self.model_data.build_duration > 0, msg='build time is not greater than 0 seconds!')
        except Exception as e:
            self.fail(self.__exception_error_msg(e))

    def test_load_model_with_invalid_model(self):
        self.assertRaises(ModelNotLoadedError, self.wrapper.load, None)

    def test_load_model_with_existing_model(self):
        try:
            with patch.object(DummyModel, 'build_model'):
                with patch.object(DummyModel, 'get_stats') as mock_get_stats:
                    mock_get_stats.return_value = {'stats': 'test get stats'}

                    trained_model_data = self.wrapper.build()

                    load_result = self.wrapper.load(new_trained_model_data=trained_model_data)
                    self.assertFalse(load_result, msg='Existing model was re-loaded successfully!')
        except Exception as e:
            self.fail(self.__exception_error_msg(e))

    def test_load_model_with_invalid_model(self):
        trained_model_data = TrainedModelData()
        trained_model_data.model = DummyModelWithoutBuildModelMethod(model_config={})
        trained_model_data.identifier = 'new_identifier'
        self.assertRaises(NotImplementedError, self.wrapper.load, trained_model_data)

    def test_load_model(self):
        try:
            trained_model_data = TrainedModelData()
            trained_model_data.model = DummyModel(model_config={})
            trained_model_data.identifier = 'new_identifier'

            load_result = self.wrapper.load(new_trained_model_data=trained_model_data)
            self.assertTrue(load_result, msg='Failed to load new trained model')
        except Exception as e:
            self.fail(self.__exception_error_msg(e))

    def test_wrapper_get_prediction(self):
        try:
            with patch.object(DummyModel, 'build_model') as mock_build_model:
                with patch.object(DummyModel, 'get_stats') as mock_get_stats:
                    mock_get_stats.return_value = {'stats': 'test get stats'}

                    with patch.object(DummyModel, 'get_prediction') as mock_get_prediction:
                        self.model_data = self.wrapper.build()

                        job = {
                            "class": "SLES11&&8G",
                            "qslot": "/DCG/Columbiaville/RTL/regression",
                            "classreservation": None,
                            "user": "orweiser1",
                            "queue": "iil_normal",
                            "cmdname": "trex",
                            "task": "fxp.cse_level2.2019_03_27_12_32_59"
                        }

                        pred_result = self.wrapper.get_prediction(input_features=job)
                        self.assertIsNotNone(pred_result, msg='Prediction result is None!')

                        self.assertEqual(mock_get_prediction.call_count, 1)

        except Exception as e:
            self.fail(self.__exception_error_msg(e))
