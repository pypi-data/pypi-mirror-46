#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/receiver_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test the receiver module."""
import functools
import json
import os
import unittest
from time import sleep

import cherrypy
from cherrypy.test import helper
import playhouse.db_url

from cloudevents.constants import SPEC_VERSION
from jsonpath2.path import Path

from pacifica.dispatcher.event_handlers import NoopEventHandler, ExceptionEventHandler
from pacifica.dispatcher.receiver import create_peewee_model
from pacifica.dispatcher.router import Router

DB_ = playhouse.db_url.connect(os.getenv('DATABASE_URL', 'sqlite:///:memory:'))

ReceiveTaskModel = create_peewee_model(DB_)

MODELS_ = (ReceiveTaskModel, )

DB_.create_tables(MODELS_)

ROUTER = Router()
ROUTER.add_route(
    Path.parse_str('$[?(@["eventType"] = {})]'.format(json.dumps('io.cloudevents'))),
    NoopEventHandler()
)
ROUTER.add_route(
    Path.parse_str('$[?(@["eventType"] = {})]'.format(json.dumps('exception.event.type'))),
    ExceptionEventHandler()
)

CELERY_APP = ReceiveTaskModel.create_celery_app(
    ROUTER,
    'pacifica.dispatcher.app',
    'pacifica.dispatcher.tasks.receive',
    backend=os.getenv('BACKEND_URL', 'rpc://'),
    broker=os.getenv('BROKER_URL', 'pyamqp://')
)

APPLICATION = ReceiveTaskModel.create_cherrypy_app(CELERY_APP.tasks['pacifica.dispatcher.tasks.receive'])


def use_database(func):
    """Decorator to bind and wrap models to databases."""
    @functools.wraps(func)
    def inner(self):
        with DB_.bind_ctx(MODELS_):
            DB_.create_tables(MODELS_)
            try:
                func(self)
            finally:
                sleep(2)
                DB_.drop_tables(MODELS_)
    return inner


class ReceiveTaskModelTestCase(helper.CPWebCase):
    """CherryPy test case for receiving events."""

    def setUp(self):
        """Setup by creating a stub cloud event."""
        self.event_data = {
            'cloudEventsVersion': SPEC_VERSION,
            'eventType': 'io.cloudevents',
            'eventID': 'ID',
            'source': '/cloudevents/io',
            'data': [],
        }
        self.bad_event_data = {
            'cloudEventsVersion': SPEC_VERSION,
            'eventType': 'org.pacifica.metadata.doiupload',
            'eventID': 'ID',
            'source': '/cloudevents/io',
            'data': [],
        }
        self.exception_event_data = {
            'cloudEventsVersion': SPEC_VERSION,
            'eventType': 'exception.event.type',
            'eventID': 'ID',
            'source': '/cloudevents/io',
            'data': [],
        }

    @staticmethod
    def setup_server():
        """Start the cherrypy test server."""
        cherrypy.tree.mount(APPLICATION)

    @use_database
    def test_root(self):
        """Test root see it returns nothing."""
        self.getPage('/')
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')
        self.assertBody('[]')

    @use_database
    def test_get(self):
        """Test some get methods for not finding things."""
        self.getPage('/get/a')
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('422 Unprocessable Entity')

        self.getPage('/get/123e4567-e89b-12d3-a456-426655440000')
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('404 Not Found')

    @use_database
    def test_receive(self):
        """Test the receive endpoint."""
        request_body = bytes(json.dumps(self.event_data), 'utf-8')
        self.getPage('/receive', method='POST', body=request_body, headers=[
            ('Content-Length', str(len(request_body))),
            ('Content-Type', 'application/json;charset=utf-8'),
        ])
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')
        response_data = json.loads(self.body.decode('utf-8'))

        self.getPage('/get/{0}'.format(response_data))
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')

        self.getPage('/status/{0}'.format(response_data))
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')

    @use_database
    def test_receive_exc_event(self):
        """Test the receive endpoint."""
        request_body = bytes(json.dumps(self.exception_event_data), 'utf-8')
        self.getPage('/receive', method='POST', body=request_body, headers=[
            ('Content-Length', str(len(request_body))),
            ('Content-Type', 'application/json;charset=utf-8'),
        ])
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')
        response_data = json.loads(self.body.decode('utf-8'))
        sleep(2)
        self.getPage('/get/{0}'.format(response_data))
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')
        response_data = json.loads(self.body.decode('utf-8'))
        self.assertEqual(response_data['taskStatus'], '500 Internal Server Error')

    @use_database
    def test_receive_bad_event(self):
        """Test the receive endpoint."""
        request_body = bytes(json.dumps(self.bad_event_data), 'utf-8')
        self.getPage('/receive', method='POST', body=request_body, headers=[
            ('Content-Length', str(len(request_body))),
            ('Content-Type', 'application/json;charset=utf-8'),
        ])
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')
        response_data = json.loads(self.body.decode('utf-8'))
        sleep(2)
        self.getPage('/get/{0}'.format(response_data))
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('200 OK')
        response_data = json.loads(self.body.decode('utf-8'))
        self.assertEqual(response_data['taskStatus'], '422 Unprocessable Entity')

    @use_database
    def test_status(self):
        """Test the status page."""
        self.getPage('/status/a')
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('422 Unprocessable Entity')

        self.getPage('/status/123e4567-e89b-12d3-a456-426655440000')
        self.assertHeader('Content-Type', 'application/json')
        self.assertStatus('404 Not Found')


if __name__ == '__main__':
    unittest.main()
