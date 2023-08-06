# -*- coding: utf-8 -*-
import json
from django.http import HttpRequest
from jsonschema import validate, ValidationError
from rest_framework.exceptions import NotAcceptable


def json_schema_parser(schema):
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            try:
                data = json.loads(request.body.decode(encoding='utf-8'))
            except json.decoder.JSONDecodeError as e:
                raise NotAcceptable(_("Parse request data to json object fail."))

            try:
                validate(data, schema=schema)
            except ValidationError as e:
                raise NotAcceptable(e.message)

            return func(request, *args, **kwargs, **data)

        return wrapper

    return decorator
