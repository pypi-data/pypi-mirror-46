# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import sys
import traceback
from functools import wraps

from tornado import web
from tornado.escape import json_decode, json_encode
from graphql.error import GraphQLError
from graphql.error import format_error as format_graphql_error


def error_status(exception):
    if isinstance(exception, web.HTTPError):
        return exception.status_code
    elif isinstance(exception, (ExecutionError, GraphQLError)):
        return 400
    else:
        return 500


def error_format(exception):
    if isinstance(exception, ExecutionError):
        return [{'message': e} for e in exception.errors]
    elif isinstance(exception, GraphQLError):
        return [format_graphql_error(exception)]
    elif isinstance(exception, web.HTTPError):
        return [{'message': exception.log_message,
                 'reason': exception.reason}]
    else:
        return [{'message': 'Unknown server error'}]


def error_response(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        log = getattr(self, 'log')

        try:
            result = func(self, *args, **kwargs)
        except Exception as ex:
            if not isinstance(ex, (web.HTTPError, ExecutionError, GraphQLError)):
                tb = ''.join(traceback.format_exception(*sys.exc_info()))
                if log:
                    log.exception('error_response')
            self.set_status(error_status(ex))
            error_json = json_encode({'errors': error_format(ex)})
            if log:
                log.debug('error_response_json', data=error_json)
            self.write(error_json)
        else:
            return result

    return wrapper


class ExecutionError(Exception):
    def __init__(self, status_code=400, errors=None):
        self.status_code = status_code
        if errors is None:
            self.errors = []
        else:
            self.errors = [str(e) for e in errors]
        self.message = '\n'.join(self.errors)


class GQLHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = self.application.log

    def options(self):
        self.set_status(204)
        self.finish()

    @error_response
    def post(self):
        return self.handle_graqhql()

    def handle_graqhql(self):
        result = self.execute_graphql()
        self.log.debug('got_graphql_result', data=result.data,
            errors=result.errors, invalid=result.invalid)

        if result and (result.errors or result.invalid):
            ex = ExecutionError(errors=result.errors)
            self.log.warn('got_graphql_error', error=ex)
            raise ex

        response = {'data': result.data}
        self.write(json_encode(response))

    def execute_graphql(self):
        graphql_req = self.graphql_request
        self.log.debug('got_graphql_request', req=graphql_req)
        return self.schema.execute(
            graphql_req.get('query'),
            variable_values=graphql_req.get('variables'),
            operation_name=graphql_req.get('operationName'),
            context_value=self.context,
            middleware=self.middleware
        )

    @property
    def graphql_request(self):
        return json_decode(self.request.body)

    @property
    def content_type(self):
        return self.request.headers.get('Content-Type', 'text/plain').split(';')[0]

    @property
    def schema(self):
        raise NotImplementedError('schema must be provided')

    @property
    def middleware(self):
        return []

    @property
    def context(self):
        return {}
