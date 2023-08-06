from marshmallow import Schema, fields
from . import RiotSchema


class ResponseStatus(RiotSchema):
    status_code = fields.String()
    message = fields.String()


class APIErrorResponse(RiotSchema):
    status = fields.Nested(ResponseStatus, many=False)
