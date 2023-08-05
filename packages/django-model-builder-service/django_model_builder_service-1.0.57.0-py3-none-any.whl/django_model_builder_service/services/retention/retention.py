import datetime

from django.db import connection
from swiss_common_utils.datetime.datetime_utils import time_string_to_seconds
from swiss_logger.log_utils import log_enter_and_exit, print_ascii_art, get_logger

from django_model_builder_service import app_globals

logger = get_logger(name='retention_service')


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


def do_retention():
    app_globals.metrics_registrar.counter(name='retention_thread', documentation='retention thread start').inc()
    __do_retention()


@log_enter_and_exit
def __do_retention():
    try:
        app_globals.retention_service.run()
    except Exception as e:
        msg = generate_exception_error_message(e)
        global logger
        logger.exception(msg=msg)


class RetentionService:

    def __init__(self, config_manager):
        self.config_manager = config_manager

        retention_shelf_life_str = self.config_manager.get_config_val_with_default(
            'retention_shelf_life', '3d')  # Default is 3d
        retention_shelf_life_seconds = time_string_to_seconds(retention_shelf_life_str)
        retention_shelf_life_minutes = retention_shelf_life_seconds / 60

        global logger
        logger.info(
            'Initializing retention service. Shelf life: {}'.format(retention_shelf_life_str))

        self.shelf_life_minutes = retention_shelf_life_minutes

    @log_enter_and_exit
    def run(self):
        print_ascii_art('RETENTION')
        deletion_time = datetime.datetime.now() - datetime.timedelta(minutes=self.shelf_life_minutes)

        global logger
        logger.info('Deleting models built before: {}'.format(deletion_time.strftime('%Y-%m-%d %H:%M')))

        # Force Django to create new db connection.
        # Should prevent 'MySQL server has gone away' exceptions
        connection.close()

        from django_model_builder_service.models import PredictionModel
        records_deleted, queryset = PredictionModel.objects.filter(build_time__lt=deletion_time).delete()
        logger.info('Deleted {} models from db'.format(records_deleted))
