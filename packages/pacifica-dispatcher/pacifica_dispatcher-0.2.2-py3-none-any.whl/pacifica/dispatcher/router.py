#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/router.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Router module.

This module contains classes to handle routing of events to event
handlers.
"""
import typing

from cloudevents.model import Event
from jsonpath2.path import Path

from .event_handlers import EventHandler


class Route:
    """
    Route class.

    This class routes an event to an event handler.
    """

    def __init__(self, path: Path, event_handler: EventHandler) -> None:
        """Save the path and event handler in the route."""
        super(Route, self).__init__()
        self.path = path
        self.event_handler = event_handler

    def __call__(self, event_data: typing.Dict[str, typing.Any]) -> None:
        """Use event data to call the handler on the event."""
        event = Event(event_data)
        self.event_handler.handle(event)

    def match(self, event_data: typing.Dict[str, typing.Any]) -> bool:
        """Determine if the event matches the route."""
        for _match_data in self.path.match(event_data):
            return True
        return False


class Router:
    """Router handles a list of routes."""

    def __init__(self) -> None:
        """Initialize the internal list of routes."""
        super(Router, self).__init__()
        self._routes = []  # type: typing.List[Route]

    def __call__(self, event_data: typing.Dict[str, typing.Any]) -> None:
        """Match the first route object then call it."""
        route = self.match_first_or_raise(event_data)
        route(event_data)

    def add_route(self, *args, **kwargs) -> None:
        """Append new route objects based on keywords and args."""
        route = Route(*args, **kwargs)
        self._routes.append(route)

    def match(self, event_data: typing.Dict[str, typing.Any]) -> typing.Generator[Route, None, None]:
        """Yield all route objects that match the event."""
        for route in self._routes:
            if route.match(event_data):
                yield route

    def match_first_or_raise(self, event_data: typing.Dict[str, typing.Any]) -> Route:
        """Return the first route that matches the event."""
        for route in self.match(event_data):
            return route
        raise RouteNotFoundRouterError(self, event_data)


class RouterError(BaseException):
    """Router base exception class."""

    def __init__(self, router: Router) -> None:
        """Save the router as a part of the class."""
        super(RouterError, self).__init__()
        self.router = router


class RouteNotFoundRouterError(RouterError):
    """No route found exception."""

    def __init__(self, router: Router, event_data: typing.Dict[str, typing.Any]) -> None:
        """Save the event as well as the router."""
        super(RouteNotFoundRouterError, self).__init__(router)
        self.event_data = event_data

    def __str__(self) -> str:
        """Stringify the route not found exception."""
        return 'route not found'


__all__ = ('Route', 'Router', 'RouterError', 'RouteNotFoundRouterError', )
