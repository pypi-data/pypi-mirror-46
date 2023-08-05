import os
import sys

from django.utils import timezone
from prediction_model_wrapper.wrapper.prediction_model_wrapper import PredictionModelWrapper
from swiss_common_utils.datetime.datetime_utils import time_string_to_seconds
from swiss_logger.log_utils import log_enter_and_exit

from django_model_builder_service import app_globals
from django_model_builder_service.common.logger import get_logger
from django_model_builder_service.config.config_manager import ConfigManager
from django_model_builder_service.metrics.metrics import MetricsRegistrar
from django_model_builder_service.schedule_task.schedule_task_manager import ScheduleTaskManager
from django_model_builder_service.services.builder.builder import BuilderService, build_model
from django_model_builder_service.services.monitoring.monitoring import monitor_schedule_tasks
from django_model_builder_service.services.retention.retention import do_retention

logger = get_logger()


def initialize_scheduled_tasks():
    # Must be first
    initialize_schedule_task_monitoring_task()

    initialize_retention_task()
    initialize_build_model_task()

    jobs = app_globals.schedule_task_manager.get_tasks()
    logger.info('Scheduled tasks status:')
    for job in jobs:
        logger.info('{}: {}'.format(job, jobs[job]))


def initialize_schedule_task_monitoring_task():
    app_globals.schedule_task_manager.add_task(name='monitoring_task', interval=10,
                                               func=monitor_schedule_tasks, next_run_time=timezone.now())


def initialize_retention_task():
    retention_interval_str = app_globals.config_manager.get_config_val_with_default('retention_interval',
                                                                                    '1d')  # Default is 1d
    retention_interval_seconds = time_string_to_seconds(retention_interval_str)
    logger.info('Retention task interval: {}'.format(retention_interval_str))

    # First run happens after interval and recur every interval
    app_globals.schedule_task_manager.add_task(name='retention_task', interval=retention_interval_seconds,
                                               func=do_retention)


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


def initialize_build_model_task():
    build_interval_seconds_str = app_globals.config_manager.get_config_val_with_default('model_build_interval',
                                                                                        '0.0s')
    build_interval_seconds = time_string_to_seconds(build_interval_seconds_str)
    logger.info('Model build interval: {}'.format(build_interval_seconds_str))
    if build_interval_seconds < 30.0:
        logger.warning('Model build interval is too short! Schedule task will NOT be created...')
        build_model()
        return

    # First build happens immediately and then every interval
    app_globals.schedule_task_manager.add_task(name='build_model_task', interval=build_interval_seconds,
                                               func=build_model, next_run_time=timezone.now())


def initialize_app_globals(model_class_fully_qualified_name):
    # Initialization order matters - do not change!

    # Config manager
    app_globals.config_manager = ConfigManager()

    # Schedule task manager
    app_globals.schedule_task_manager = ScheduleTaskManager()

    # Metrics registrar
    app_globals.metrics_registrar = MetricsRegistrar()

    # Builder service
    config = app_globals.config_manager.get_config_dict()
    wrapper = PredictionModelWrapper(model_class_fully_qualified_name=model_class_fully_qualified_name, config=config)
    app_globals.builder_service = BuilderService(prediction_model_wrapper=wrapper,
                                                 config_manager=app_globals.config_manager)

    # Retention service
    from django_model_builder_service.services.retention.retention import RetentionService
    app_globals.retention_service = RetentionService(config_manager=app_globals.config_manager)


# Initialize all tasks here
@log_enter_and_exit
def initializae_service(model_class_fully_qualified_name):
    # migrate & test command may not finish due to the recurring task initialized next.
    # Initialize the recurring task only on runserver command
    if not should_start_initialize_sequence():
        return

    logger.info('Running initializing sequence for service app')

    initialize_app_globals(model_class_fully_qualified_name=model_class_fully_qualified_name)
    initialize_scheduled_tasks()
