import base64
import pickle
from unittest import TestCase
from unittest.mock import patch

from prediction_model_wrapper.trained_model_data.trained_model_data_keys import *

from django_model_prediction_service import app_globals
from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.services.model_loader.loader.model_builder_service import ModelBuilderService
from django_model_prediction_service.services.model_loader.loader.model_loader import ModelLoader
from tests.dummy_objects import DummyMetricsRegistrar, DummyModel

TEST_MEMORY_USAGE = 'test_memory_usage'
TEST_BUILD_DURATION = 'test_build_duration'
TEST_BUILD_TIME = 'test_build_time'
TEST_IDENTIFIER = 'test_identifier'


def is_config_key_exists_side_effect(key):
    if key == 'model_source_builder_service_url' or key == 'model_source_builder_service_port':
        return 'not empty'
    return ''


class TestModelLoader(TestCase):

    @classmethod
    def setUpClass(cls):
        app_globals.metrics_registrar = DummyMetricsRegistrar()

    def test_get_model(self):
        model_loader = ModelLoader(config_manager=ConfigManager(),
                                   model_builder_service=ModelBuilderService('', ''))
        with patch.object(ConfigManager, 'is_config_key_exists') as mock_is_config_key_exists:
            with patch.object(ModelBuilderService, 'get_model') as mock_get_model:
                with patch.object(app_globals.metrics_registrar, 'gauge'):
                    dummy_model = DummyModel()
                    expected_result_dict = {
                        MODEL: base64.b64encode(pickle.dumps(dummy_model)).decode('utf-8'),
                        IDENTIFIER: TEST_IDENTIFIER,
                        BUILD_TIME: TEST_BUILD_TIME,
                        BUILD_DURATION: TEST_BUILD_DURATION,
                        STATS: {},
                        MEMORY_USAGE: TEST_MEMORY_USAGE
                    }

                    mock_is_config_key_exists.side_effect = is_config_key_exists_side_effect
                    mock_get_model.return_value = expected_result_dict

                    model_data = model_loader.get_model()
                    model = model_data.model
                    self.assertTrue(isinstance(model, DummyModel))

                    model_identifier = model_loader.get_model_identifier()
                    self.assertEqual(model_identifier, TEST_IDENTIFIER)
                    self.assertEqual(model_data.identifier, TEST_IDENTIFIER)

                    build_time = model_loader.get_model_build_time()
                    self.assertEqual(build_time, TEST_BUILD_TIME)
                    self.assertEqual(model_data.build_time, TEST_BUILD_TIME)

                    self.assertEqual(model_data.build_duration, TEST_BUILD_DURATION)
                    self.assertEqual(model_data.stats, {})
                    self.assertEqual(model_data.memory_usage, TEST_MEMORY_USAGE)
