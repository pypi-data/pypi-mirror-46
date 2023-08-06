import logging as logger

from flask import request
from flask_restful import Resource, reqparse
from flask_restful_resource.comm.utils import move_space, validate_schema
from schema import Schema

from .exceptions import ErrorCode, ResourceException


class BaseResource(Resource):
    validate_data = None
    validate_schemas = {}
    allow_methods = ["get", "post", "put", "delete"]

    def dispatch_request(self, *args, **kwargs):
        if request.method.lower() not in self.allow_methods:
            return ResourceException(ErrorCode.METHOD_NOT_ALLOW, 405)
        req = None
        schema = None
        if request.method == "GET":
            schema = self.validate_schemas.get("get")
            req = request.args.to_dict()
        else:
            schema = self.validate_schemas.get(request.method.lower())
            req = request.json
        req = move_space(req)
        if isinstance(schema, Schema):
            data, errors = validate_schema(schema, req)
            if errors:
                logger.info(str(errors))
                return ResourceException(ErrorCode.VALIDATE_ERROR)
            self.validate_data = data
        elif isinstance(schema, reqparse.RequestParser):
            parse_req = schema.parse_args()
            strict = self.validate_schemas.get("strict") or ""
            if strict:
                parse_req = schema.parse_args(strict=True)
            self.validate_data = {k: v for k, v in parse_req.items() if v}

        if not self.validate_data:
            self.validate_data = req
        return super().dispatch_request(*args, **kwargs)

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
