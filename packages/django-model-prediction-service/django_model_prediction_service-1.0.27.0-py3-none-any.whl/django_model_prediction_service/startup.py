import datetime
import os
import sys

from django.utils import timezone
from prediction_model_wrapper.wrapper.prediction_model_wrapper import PredictionModelWrapper
from swiss_common_utils.datetime.datetime_utils import time_string_to_seconds
from swiss_logger.log_utils import log_enter_and_exit

from django_model_prediction_service import app_globals
from django_model_prediction_service.common.logger import get_logger
from django_model_prediction_service.config.config_manager import ConfigManager
from django_model_prediction_service.metrics.metrics import MetricsRegistrar
from django_model_prediction_service.schedule_task.schedule_task_manager import ScheduleTaskManager
from django_model_prediction_service.services.model_loader.handler.prediction_model_handler import \
    PredictionModelHandler, load_trained_model
from django_model_prediction_service.services.monitoring.monitoring import monitor_schedule_tasks

logger = get_logger()


def initialize_load_trained_model_task():
    load_interval_str = app_globals.config_manager.get_config_val_with_default('model_load_interval', default='6h')
    logger.info('Model load interval: {}'.format(load_interval_str))
    load_interval_seconds = time_string_to_seconds(load_interval_str)

    # First build happens immediately and then every interval
    app_globals.schedule_task_manager.add_task(name='load_model_task', interval=load_interval_seconds,
                                               func=load_trained_model, next_run_time=timezone.now())


def is_debug():
    return os.environ.get('CONFIG_SERVICE_SETTINGS_DEBUG', 'true').lower() != 'false'


def is_manage_command(command):
    args = sys.argv
    if 'manage.py' in args:
        if command in args:
            logger.info('Running manage.py runserver --> service init')
            return True
        else:
            logger.info('Running some manage.py command other than runserver --> no service init')
            return False

    return False


def should_start_initialize_sequence():
    if is_manage_command('runserver'):
        return True

    if not is_debug():
        logger.info('DEBUG=False --> service init')
        return True

    logger.info('should_start_initialize_sequence returned True')
    return False


def initialize_schedule_task_monitoring_task():
    app_globals.schedule_task_manager.add_task(name='monitoring_task', interval=10,
                                               func=monitor_schedule_tasks, next_run_time=datetime.datetime.now())


def initialize_app_globals(model_class_fully_qualified_name):
    # Initialization order matters - do not change!

    # Config manager
    app_globals.config_manager = ConfigManager()

    # Schedule task manager
    app_globals.schedule_task_manager = ScheduleTaskManager()

    # Metrics registrar
    app_globals.metrics_registrar = MetricsRegistrar()

    # Model loader service
    config = app_globals.config_manager.get_config_dict()
    wrapper = PredictionModelWrapper(model_class_fully_qualified_name=model_class_fully_qualified_name, config=config)
    app_globals.prediction_model_handler = PredictionModelHandler(prediction_model_wrapper=wrapper,
                                                                  config_manager=app_globals.config_manager)


def initialize_scheduled_tasks():
    # Must be first
    initialize_schedule_task_monitoring_task()

    initialize_load_trained_model_task()


@log_enter_and_exit
def initialize_service(model_class_fully_qualified_name):
    # migrate & test command may not finish due to the recurring task initialized next.
    # Initialize the recurring task only on runserver command
    if not should_start_initialize_sequence():
        return

    logger.info('Running initializing sequence for service app')

    initialize_app_globals(model_class_fully_qualified_name=model_class_fully_qualified_name)
    initialize_scheduled_tasks()
