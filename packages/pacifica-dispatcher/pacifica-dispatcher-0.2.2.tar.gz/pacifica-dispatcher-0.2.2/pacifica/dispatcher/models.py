#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/models.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Models module.

This class contains the data structure models for the dispatcher.
"""
import abc
import json
import os
import typing

from cloudevents.model import Event
from jsonpath2.path import Path

from .exceptions import TransactionDuplicateAttributeError


# pylint: disable=too-few-public-methods
class PacificaModel(abc.ABC):
    """
    Abstract base class for all Dispatcher models.

    Contains method interface definitions for all model classes.
    """

    # pylint: disable=line-too-long
    @classmethod
    @abc.abstractmethod
    def from_cloudevents_model(cls, event: Event) -> typing.Union['PacificaModel', typing.List['PacificaModel']]:  # NOQA: E501
        """Abstract method for creating a model from a cloud event."""
        raise NotImplementedError()  # pragma: no cover
    # pylint: enable=line-too-long


class File(PacificaModel):
    """
    File model class.

    This holds all information about a file from a cloud event.
    """

    _id = None
    ctime = None
    encoding = None
    hashsum = None
    hashtype = None
    mimetype = None
    mtime = None
    name = None
    size = None
    subdir = None
    suspense_date = None

    def __init__(self, **attrs: typing.Dict[str, typing.Any]) -> None:
        """Build the file attributes from the dictionary keywords."""
        super(File, self).__init__()
        attr_names = [
            '_id', 'ctime', 'encoding', 'hashsum', 'hashtype', 'mimetype',
            'mtime', 'name', 'size', 'subdir', 'suspense_date'
        ]
        for name in attr_names:
            setattr(self, name, attrs.get(name, None))

    @classmethod
    def from_cloudevents_model(cls, event: Event) -> typing.List['File']:
        """Factory creating instances of File from a cloud event."""
        insts = []

        for match_data in Path.parse_str('$[*][?(@["destinationTable"] = "Files")]').match(event.data):
            inst = cls(**match_data.current_value)

            insts.append(inst)

        return insts

    @property
    def path(self) -> str:
        """Path property accessor."""
        if self.name is None:
            raise AttributeError('field \'name\' is None')
        if self.subdir is None:
            return self.name
        return os.path.join(self.subdir, self.name)


class Transaction(PacificaModel):
    """
    Transaction model clas.

    This class holds all the information about a transaction from a
    cloud event.
    """

    _id = None
    analytical_tool = None
    description = None
    instrument = None
    project = None
    submitter = None
    suspense_date = None

    def __init__(self, **attrs: typing.Dict[str, typing.Any]) -> None:
        """Build the transaction from the attrs in keywords."""
        super(Transaction, self).__init__()

        for name in ['_id', 'analytical_tool', 'description', 'instrument', 'project', 'submitter', 'suspense_date']:
            setattr(self, name, attrs.get(name, None))

    @classmethod
    def from_cloudevents_model(cls, event: Event) -> 'Transaction':
        """Factory creating a transaction class from a cloud event."""
        attrs = {}
        attr_names = [
            '_id', 'analytical_tool', 'description', 'instrument',
            'project', 'submitter', 'suspense_date'
        ]
        for name in attr_names:
            matches = Path.parse_str(
                '$[*][?(@["destinationTable"] = {0})]["value"]'.format(
                    json.dumps('Transactions.{0}'.format(name))
                )
            ).match(event.data)
            for match_data in matches:
                if name in attrs:
                    raise TransactionDuplicateAttributeError(event, name)

                attrs[name] = match_data.current_value

            if name not in attrs:
                attrs[name] = None

        return cls(**attrs)


class TransactionKeyValue(PacificaModel):
    """
    Transaction key value model.

    This holds the transaction key value pairs from a cloud event.
    """

    def __init__(self, **attrs: typing.Dict[str, typing.Any]) -> None:
        """Construct the attributes from keywords."""
        super(TransactionKeyValue, self).__init__()

        for name in ['key', 'value']:
            setattr(self, name, attrs.get(name, None))

    @classmethod
    def from_cloudevents_model(cls, event: Event) -> typing.List['TransactionKeyValue']:
        """Factory creating all the key value pairs for a cloud event."""
        insts = []

        for match_data in Path.parse_str('$[*][?(@["destinationTable"] = "TransactionKeyValue")]').match(event.data):
            inst = cls(**match_data.current_value)

            insts.append(inst)

        return insts


__all__ = ('PacificaModel', 'File', 'Transaction', 'TransactionKeyValue', )
