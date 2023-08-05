import base64
import json
import pickle

import pytz
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from swiss_common_utils.datetime.datetime_utils import format_time_length
from swiss_logger.log_utils import log_enter_and_exit

from django_model_builder_service import app_globals
from django_model_builder_service.common.logger import get_logger

logger = get_logger()


def generate_error_json_response(error):
    return JsonResponse({"error": error})


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


@log_enter_and_exit
def get_model(request):
    app_globals.metrics_registrar.counter(name='get_model', documentation='get model request counter').inc()

    if request.method != 'GET':
        return generate_error_json_response('not a get request')

    try:
        logger.info('Getting')
        latest_model = app_globals.builder_service.get_model_data().as_dict()
        model = latest_model['model']
        model = pickle.dumps(model)
        model_enc = base64.b64encode(model)
        latest_model['model'] = model_enc.decode(
            'utf-8')  # Convert byte string to string (for json serialization to send over the network)

        logger.info('Size of response: {} KB'.format(int(len(str(latest_model).encode('utf-8')) / 1024)))
        return JsonResponse(latest_model)
    except Exception as e:
        error_msg = generate_exception_error_message(e)
        logger.exception(msg=error_msg)
        return generate_error_json_response(error_msg)


def show_model(request, identifier):
    app_globals.metrics_registrar.counter(name='show_model', documentation='show model request counter').inc()

    # Force Django to create new db connection.
    # Should prevent 'MySQL server has gone away' exceptions
    connection.close()

    from django_model_builder_service.models import PredictionModel
    model = get_object_or_404(PredictionModel, identifier=identifier)
    try:
        stats = json.loads(model.stats.replace("'", '"'))
        config = json.loads(model.config.replace("'", '"'))
    except Exception as e:
        logger.exception(msg=generate_exception_error_message(e))
        stats = model.stats
        config = model.config

    my_tz = pytz.timezone('Israel')
    timezone.activate(my_tz)
    now = timezone.localtime()
    build_time = timezone.localtime(model.build_time)
    context = {
        'now': now.strftime('%d %B %Y, %H:%M:%S'),
        'identifier': identifier,
        'build_time': build_time.strftime('%d %B %Y, %H:%M:%S'),
        'stats': stats,
        'build_duration': format_time_length(seconds=model.build_duration),
        'config': config,
        'memory_usage': model.memory_usage
    }

    return render(request, 'service/model.html', context)
