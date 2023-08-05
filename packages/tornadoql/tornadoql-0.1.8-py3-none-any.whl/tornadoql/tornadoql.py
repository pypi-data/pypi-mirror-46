# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os
import copy

import tornado.web
from deeputil import Dummy

from tornadoql.graphql_handler import GQLHandler
from tornadoql.subscription_handler import GQLSubscriptionHandler

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
DUMMY_LOG = Dummy()

class GraphQLHandler(GQLHandler):
    @property
    def schema(self):
        return self.application.schema

    @property
    def context(self):
        c = super().context
        c['request'] = self.request
        return c


class GraphQLSubscriptionHandler(GQLSubscriptionHandler):

    def initialize(self, opts):
        super(GraphQLSubscriptionHandler, self).initialize()
        self.opts = opts

    @property
    def schema(self):
        return self.application.schema

    @property
    def sockets(self):
        return self.opts['sockets']

    @property
    def subscriptions(self):
        return self.opts['subscriptions'].get(self, {})

    @subscriptions.setter
    def subscriptions(self, subscriptions):
        self.opts['subscriptions'][self] = subscriptions


class GraphiQLHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(STATIC_PATH, 'graphiql.html'))


class TornadoQL:
    PORT = 8888
    SETTINGS = {
        'sockets': [],
        'subscriptions': {}
    }

    GRAPHQL_SUBSCRIPTION_HANDLER = GraphQLSubscriptionHandler
    GRAPHQL_HANDLER = GraphQLHandler
    GRAPHIQL_HANDLER = GraphiQLHandler

    def __init__(self, schema, port=PORT, settings=None, log=DUMMY_LOG):
        self.schema = schema
        self.settings = settings or copy.deepcopy(self.SETTINGS)
        self.log = log
        self.port = port

    def make_app(self):
        endpoints = self.define_endpoints()
        app = tornado.web.Application(endpoints, **self.settings)
        app.schema = self.schema
        app.log = self.log
        return app

    def define_endpoints(self):
        return [
            (r'/subscriptions', self.GRAPHQL_SUBSCRIPTION_HANDLER, dict(opts=self.settings)),
            (r'/graphql', self.GRAPHQL_HANDLER),
            (r'/graphiql', self.GRAPHIQL_HANDLER)
        ]

    def start(self, port=None):
        port = port or self.port

        self.log.info('starting_server', urls=dict(
            graphiql='http://localhost:%s/graphiql' % port,
            queries_and_mutations='http://localhost:%s/graphql' % port,
            subscriptions='ws://localhost:%s/subscriptions' % port))

        app = self.make_app()
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()
