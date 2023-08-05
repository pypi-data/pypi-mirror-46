import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django_model_prediction_service import app_globals
from django_model_prediction_service.common.logger import get_logger

logger = get_logger()


def generate_error_json_response(error):
    return JsonResponse({"error": error})


def generate_exception_error_message(e):
    return 'Exception caught. type: {}, message: {}'.format(type(e), str(e))


@csrf_exempt  # TODO: this disables csrf protection, should find a different solution
def get_prediction(request):
    if request.method != 'POST':
        return generate_error_json_response('not a post request')
    if request.content_type != 'application/json':
        return generate_error_json_response('invalid request content type')
    try:
        app_globals.metrics_registrar.counter(name='get_prediction', documentation='get prediction request counter').inc()

        data = request.body.decode('utf-8')
        data_json_obj = json.loads(data)
        prediction_result = app_globals.prediction_model_handler.get_prediction(data_json_obj)
        return JsonResponse(prediction_result)
    except Exception as e:
        error_msg = generate_exception_error_message(e)
        logger.error(error_msg)
        return generate_error_json_response(error_msg)
