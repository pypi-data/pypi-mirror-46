import toastedmarshmallow
from marshmallow import Schema, fields


import requests
from riot.connection import (
    get_headers, get_base_url, get_main_params)


class ToastedSchema(Schema):
    class Meta:
        jit = toastedmarshmallow.Jit


class ResponseStatus(ToastedSchema):
    status_code = fields.String()
    message = fields.String()


class RiotSchema(ToastedSchema):
    status = fields.Nested(ResponseStatus, many=False)
