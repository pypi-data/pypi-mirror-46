#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/router_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test the Router module."""
import unittest

from cloudevents.constants import SPEC_VERSION
from jsonpath2.path import Path

from pacifica.dispatcher.event_handlers import NoopEventHandler
from pacifica.dispatcher.router import RouteNotFoundRouterError, Router


class RouterTestCase(unittest.TestCase):
    """Test the Router class."""

    def test_blank_router_raises(self):
        """Router can't be created without arguments."""
        router = Router()
        with self.assertRaises(RouteNotFoundRouterError):
            router(None)

    def test_router_matches_first(self):
        """Router needs to have some path."""
        router = Router()
        router.add_route(Path.parse_str('$'), NoopEventHandler())
        self.assertEqual(1, len(list(router.match(None))))

    def test_router_matches_second(self):
        """Router can match the second route."""
        router = Router()
        router.add_route(Path.parse_str('$["key"]'), NoopEventHandler())
        router.add_route(Path.parse_str('$'), NoopEventHandler())
        self.assertEqual(1, len(list(router.match(None))))

    def test_router_callable(self):
        """Test the route callable."""
        router = Router()
        router.add_route(Path.parse_str('$'), NoopEventHandler())
        self.assertEqual(None, router({
            'cloudEventsVersion': SPEC_VERSION,
            'eventID': 'ID',
            'eventType': 'io.cloudevents',
            'source': '/cloudevents/io',
            'data': [],
        }))


if __name__ == '__main__':
    unittest.main()
