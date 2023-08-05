import json
from unittest import TestCase
from unittest.mock import patch

from django_model_prediction_service import app_globals
from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.services.model_loader.handler.prediction_model_handler import \
    PredictionModelHandler, JOB_ID, JOB_PREDICTION_RESULT, RESULT, CLASSIFIER_ID
from tests.dummy_objects import DummyMetricsRegistrar, DummyWrapper

DATA_JSON = {
    JOB_ID: 'test_job_id',
    'poolName': 'test_pool_name',
    'predictionRequiredFields': {
        'class': 'test_class',
        'qslot': 'test_qslot',
        'classreservation': 'test_classreservation',
        'user': 'test_user',
        'queue': 'test_queue',
        'cmdname': 'test_cmdname',
        'task': 'test_task'
    }
}


class TestPredictionService(TestCase):

    @classmethod
    def setUpClass(cls):
        app_globals.metrics_registrar = DummyMetricsRegistrar()

    def setUp(self):
        # Target
        self.prediction_service = PredictionModelHandler(prediction_model_wrapper=DummyWrapper(),
                                                         config_manager=ConfigManager())

    def test_get_prediction(self):
        with patch.object(DummyWrapper, 'get_prediction') as mock_get_prediction:
            with patch.object(DummyMetricsRegistrar, 'counter'):
                with patch.object(DummyMetricsRegistrar, 'gauge'):
                    mock_get_prediction.return_value = 'test_prediction_result'
                    prediction_result = self.prediction_service.get_prediction(data_json=DATA_JSON)

                    self.assertEqual(mock_get_prediction.call_count, 1)

                    # Verify fields
                    self.assertTrue(JOB_ID in prediction_result)
                    self.assertTrue(JOB_PREDICTION_RESULT in prediction_result)
                    self.assertTrue(RESULT in prediction_result[JOB_PREDICTION_RESULT])
                    self.assertTrue(CLASSIFIER_ID in prediction_result)

                    # Verify values
                    expected_result = {
                        JOB_ID: 'test_job_id',
                        JOB_PREDICTION_RESULT: {
                            RESULT: prediction_result
                        },
                        CLASSIFIER_ID: prediction_result[CLASSIFIER_ID]
                    }
                    self.assertTrue(prediction_result, expected_result)

    def test_get_prediction_when_wrapper_not_loaded(self):
        # Target
        prediction_service = PredictionModelHandler(prediction_model_wrapper=None,
                                                    config_manager=ConfigManager())

        prediction_result = prediction_service.get_prediction(data_json=DATA_JSON)
        self.assertEqual(prediction_result, {'error': 'model not loaded'})

    def test_get_prediction_when_request_missing_job_id(self):
        data_json = json.loads('{}')
        result = self.prediction_service.get_prediction(data_json=data_json)
        self.assertEqual(result, {'error': 'field jobID is missing'})

    def test_get_prediction_when_request_missing_prediction_required_fields(self):
        data_json = json.loads('{"jobID": "test_job_id"}')
        result = self.prediction_service.get_prediction(data_json=data_json)
        self.assertEqual(result, {'error': 'field predictionRequiredFields is missing'})
