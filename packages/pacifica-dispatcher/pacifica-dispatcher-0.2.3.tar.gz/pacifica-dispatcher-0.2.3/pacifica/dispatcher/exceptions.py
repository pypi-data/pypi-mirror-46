#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/exceptions.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Exceptions module.

This module contains specific exceptions that can happen during the
dispatching process.
"""
from cloudevents.model import Event


class EventError(BaseException):
    """
    Base event dispatcher error class.

    This the base event class used by all other error classes.
    """

    def __init__(self, event: Event) -> None:
        """Save the event for later use."""
        super(EventError, self).__init__()

        self.event = event


class TransactionDuplicateAttributeError(EventError):
    """
    Duplicate event error.

    Events can be sent multiple times, this error is raised if a
    transaction event has already been seen.
    """

    def __init__(self, event: Event, name: str) -> None:
        """Add the name of the event as well."""
        super(TransactionDuplicateAttributeError, self).__init__(event)

        self.name = name

    def __str__(self) -> str:  # pragma: no cover
        """Stringify the duplicate transaction."""
        return 'field \'Transactions.{0}\' is already defined'.format(self.name.replace('\'', '\\\''))


__all__ = ('EventError', 'TransactionDuplicateAttributeError', )
