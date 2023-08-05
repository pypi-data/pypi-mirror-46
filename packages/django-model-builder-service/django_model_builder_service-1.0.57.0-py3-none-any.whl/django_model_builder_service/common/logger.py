from swiss_logger import log_utils

from django_model_builder_service import app_globals


def get_logger():
    if app_globals._logger:
        return app_globals._logger

    app_globals._logger = log_utils.get_logger('django_model_builder_service_logger')
    return app_globals._logger
