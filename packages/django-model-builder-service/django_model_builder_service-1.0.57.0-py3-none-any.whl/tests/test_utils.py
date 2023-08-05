import json


def response_json_to_dict(response):
    return json.loads(response.content.decode('utf-8'))
