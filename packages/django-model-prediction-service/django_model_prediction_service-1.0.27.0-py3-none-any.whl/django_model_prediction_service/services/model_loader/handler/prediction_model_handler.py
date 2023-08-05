from swiss_common_utils.sync.mrow_lock.mrow import RWLock
from swiss_logger.log_utils import log_enter_and_exit, print_ascii_art

from django_model_prediction_service import app_globals
from django_model_prediction_service.common.logger import get_logger
from django_model_prediction_service.services.model_loader.loader.model_loader import ModelLoader, model_loader_logger
from django_model_prediction_service.services.model_loader.stats.stats_collector import StatsCollector

JOB_ID = 'jobID'
JOB_PREDICTION_RESULT = 'jobPredictionResult'
RESULT = 'result'
CLASSIFIER_ID = 'classifierID'

logger = get_logger()


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


def load_trained_model():
    app_globals.metrics_registrar.counter(name='load_model_thread', documentation='load model thread start').inc()
    __load_trained_model()


@log_enter_and_exit
def __load_trained_model():
    try:
        app_globals.prediction_model_handler.load_trained_model()
    except Exception as e:
        error_msg = generate_exception_error_message(e)
        model_loader_logger.error(error_msg)
        model_loader_logger.error('FAIL TO LOAD MODEL')


class PredictionModelHandler:
    mrow_lock = RWLock()

    def lock(type):
        def wrap(org_func):
            def wrapped_func(self, *args, **kwargs):
                global logger
                logger.debug('acquiring {} lock'.format(type))

                lock = self.mrow_lock.get_lock(type)

                try:
                    result = org_func(self, *args, **kwargs)
                finally:
                    lock.release()
                    logger.debug('releasing {} lock'.format(type))

                return result

            return wrapped_func

        return wrap

    def __init__(self, prediction_model_wrapper, config_manager, model_loader=None):

        self.config_manager = config_manager

        self.wrapper = prediction_model_wrapper

        self.stats_collector = StatsCollector()

        if model_loader:
            self.model_loader = model_loader
        else:
            self.model_loader = ModelLoader(config_manager=self.config_manager)

    @lock(type='reader')
    def __get_prediction(self, features_json):
        return self.wrapper.get_prediction(input_features=features_json)

    @lock(type='writer')
    def __set_new_model(self, model_data):
        self.wrapper.load(new_trained_model_data=model_data)

    def __generate_result_dict(self, result=None, error=None, dict_result=None):
        if error:
            result_dict = {'error': error}
        elif dict_result:
            result_dict = dict_result
        else:
            if not result:
                result = ''
            result_dict = {self.RESULT: result}
        return result_dict

    def __generate_prediction_result(self, job_id, prediction_result):
        prediction_result = {
            JOB_ID: job_id,
            JOB_PREDICTION_RESULT: {
                RESULT: prediction_result
            },
            CLASSIFIER_ID: self.model_loader.get_model_identifier()
        }
        return prediction_result

    def __collect_prediction_result_metrics(self, prediction_result):
        # Count number of predictions provided by the current model
        app_globals.metrics_registrar.counter(name='predictions_count',
                                              documentation='number of predictions provided by the current model').inc()

        # Count number of prediction results provided by the current model
        prediction_result_str = str(prediction_result[JOB_PREDICTION_RESULT][RESULT])
        app_globals.metrics_registrar.counter(name='prediction_result_count',
                                              documentation='number of predictions made per result',
                                              labels=['result']).labels(result=prediction_result_str).inc()

    def __update_stats_collector(self, prediction_result):
        self.stats_collector.total_predictions_provided_inc()
        prediction_result_str = str(prediction_result[JOB_PREDICTION_RESULT][RESULT])
        self.stats_collector.result_inc(prediction_result_str)

    def get_prediction(self, data_json):
        global logger
        if not self.wrapper:
            msg = 'model not loaded'
            logger.error(msg)
            return self.__generate_result_dict(error=msg)

        if JOB_ID not in data_json:
            return self.__generate_result_dict(error='field jobID is missing')
        job_id = data_json[JOB_ID]

        pool_name = ''
        if 'poolName' in data_json:
            pool_name = data_json['poolName']

        if 'predictionRequiredFields' not in data_json:
            return self.__generate_result_dict(error='field predictionRequiredFields is missing')
        features_json = data_json['predictionRequiredFields']

        logger.info('Job ID: {}'.format(job_id))
        logger.info('Pool name: {}'.format(pool_name))
        logger.info('features: {}'.format(features_json))

        prediction_result = self.__get_prediction(features_json)
        prediction_result = self.__generate_prediction_result(job_id=job_id, prediction_result=prediction_result)

        self.__update_stats_collector(prediction_result=prediction_result)
        self.__collect_prediction_result_metrics(prediction_result=prediction_result)

        logger.info('prediction: {}'.format(prediction_result))
        return prediction_result

    @log_enter_and_exit
    def __dump_stats_collector_and_reset(self):
        total_predictions_provided = self.stats_collector.get_total_predictions_provided()
        results = self.stats_collector.get_results()

        model_loader_logger.info('Last model stats:')
        model_loader_logger.info('Total predictions provided: {}'.format(total_predictions_provided))

        app_globals.metrics_registrar.gauge(name='total_predictions_provided',
                                            documentation='total predictions provided by the model').set(
            total_predictions_provided)

        for result in results:
            prediction_result_provided = results[result]
            model_loader_logger.info('Total prediction result <{}> provided: {}'.format(result,
                                                                                        total_predictions_provided))
            app_globals.metrics_registrar.gauge(name='total_prediction_result_provided',
                                                documentation='total predictions provided per result',
                                                labels=['result']).labels(result).set(prediction_result_provided).set(
                prediction_result_provided)

        self.stats_collector.reset()

    def load_trained_model(self):
        print_ascii_art('LOAD MODEL')
        self.__dump_stats_collector_and_reset()
        model_data = self.model_loader.get_model()
        self.__set_new_model(model_data=model_data)
        app_globals.metrics_registrar.counter(name='load_model', documentation='load model event').inc()
        return True
