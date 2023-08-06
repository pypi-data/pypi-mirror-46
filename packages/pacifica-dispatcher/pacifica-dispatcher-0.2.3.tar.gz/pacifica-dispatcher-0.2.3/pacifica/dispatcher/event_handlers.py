#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/event_handlers.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Event handlers module.

This module contains classes for handling the events. Users of this
library should create their own instances of the abstract class
``EventHandler`` to process on the downloaded data.
"""
import abc

from cloudevents.model import Event


# pylint: disable=too-few-public-methods
class EventHandler(abc.ABC):
    """
    Event handler abstract class.

    This class defines the interface for handling a cloud event.
    """

    @abc.abstractmethod
    def handle(self, event: Event) -> None:  # pragma: no cover
        """
        Abstract method for event handling.

        This method is called to process data after download.
        """
        raise NotImplementedError()


class NoopEventHandler(EventHandler):
    """
    The Noop event handler class.

    This class is a stub that does nothing when an event is received.
    This class maybe useful if the act of downloading and uploading
    is desired with no processing.
    """

    def handle(self, event: Event) -> None:
        """Method does nothing, intentionally."""


class ExceptionEventHandler(EventHandler):
    """
    The exception event handler class.

    This class is a stub that raises an exception when an event is
    received. This class is useful for testing error handling in
    the overall workflow.
    """

    def handle(self, event: Event) -> None:
        """Method raises an exception, because you are bad."""
        raise Exception('ExceptionEventHandler has raised an exception.')


__all__ = ('EventHandler', 'NoopEventHandler', 'ExceptionEventHandler', )
