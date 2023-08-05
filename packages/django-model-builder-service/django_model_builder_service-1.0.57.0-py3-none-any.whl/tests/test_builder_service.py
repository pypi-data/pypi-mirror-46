import pickle
from unittest import TestCase
from unittest.mock import patch

from prediction_model_wrapper.trained_model_data.trained_model_data import TrainedModelData

from django_model_builder_service import app_globals
from django_model_builder_service.config.config_manager import ConfigManager
from django_model_builder_service.services.builder.builder import BuilderService
from tests.dummy_objects import DummyWrapper, DummyMetricsRegistrar


class TestBuilderService(TestCase):

    @staticmethod
    def __exception_error_msg(e):
        return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))

    def setUp(self):
        self.wrapper = DummyWrapper()
        app_globals.metrics_registrar = DummyMetricsRegistrar()

    def tearDown(self):
        app_globals.metrics_registrar = None

    def test_build_model_verify_saving_old_model_verify_wrapper_build(self):
        builder_service = BuilderService(prediction_model_wrapper=self.wrapper, config_manager=ConfigManager())
        with patch.object(builder_service, '_save_model_to_db') as mock_save_old_model:
            with patch.object(builder_service.wrapper, 'build') as mock_wrapper_build:
                with patch.object(app_globals.metrics_registrar, 'counter'):
                    with patch.object(app_globals.metrics_registrar, 'gauge'):
                        dummy_trained_model_data = TrainedModelData({
                            'model': pickle.dumps(b'test_model'),
                            'identifier': 'test_identifier',
                            'build_time': 'test_build_time',
                            'build_duration': 777
                        })
                        mock_wrapper_build.return_value = dummy_trained_model_data
                        builder_service.build_model()
                        self.assertEqual(mock_save_old_model.call_count, 1)
                        self.assertEqual(mock_wrapper_build.call_count, 1)

    def test_get_model_data(self):
        builder_service = BuilderService(prediction_model_wrapper=self.wrapper, config_manager=ConfigManager())
        with patch.object(builder_service, '_save_model_to_db') as mock_save_old_model:
            with patch.object(builder_service.wrapper, 'build') as mock_wrapper_build:
                with patch.object(app_globals.metrics_registrar, 'counter'):
                    with patch.object(app_globals.metrics_registrar, 'gauge'):
                        dummy_trained_model_data = TrainedModelData({
                            'model': pickle.dumps(b'test_model'),
                            'identifier': 'test_identifier',
                            'build_time': 'test_build_time',
                            'build_duration': 777
                        })
                        mock_wrapper_build.return_value = dummy_trained_model_data
                        builder_service.build_model()
                        self.assertEqual(mock_save_old_model.call_count, 1)
                        self.assertEqual(mock_wrapper_build.call_count, 1)

                        trained_model_data = builder_service.get_model_data()
                        self.assertEqual(trained_model_data, dummy_trained_model_data)

    def test_get_model_data_when_model_not_built_yet(self):
        builder_service = BuilderService(prediction_model_wrapper=self.wrapper, config_manager=ConfigManager())
        with self.assertRaises(Exception) as context:
            builder_service.get_model_data()

        self.assertTrue('no model was build yet' in str(context.exception))
