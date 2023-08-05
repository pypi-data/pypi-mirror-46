#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/uploader_runners.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Uploader runner module.

This module contains the methods for uploading data either remotely
or locally.
"""
import abc
import os
import tempfile
import time
import typing

from pacifica.uploader import Uploader
from pacifica.uploader.bundler import Bundler
from pacifica.uploader.metadata import MetaData, MetaObj

from .exceptions import TransactionDuplicateAttributeError
from .models import Transaction, TransactionKeyValue


def _should_sleep(**kwargs: typing.Dict[str, typing.Any]) -> bool:  # pragma: no cover
    for name in ['state', 'task', 'task_percent']:
        if name not in kwargs:
            raise ValueError('field \'{0}\' is not defined'.format(name.replace('\'', '\\\'')))

    if kwargs.get('state', None) == 'FAILED':
        return False
    if kwargs.get('state', None) != 'OK':
        return True
    if kwargs.get('task', None) != 'ingest metadata':
        return True
    if int(float(kwargs.get('task_percent', None))) != 100:
        return True
    return False


def _to_bundler(basedir_name: str, transaction: Transaction,
                transaction_key_values: typing.List[TransactionKeyValue]) -> Bundler:
    meta_data = _to_meta_data(transaction=transaction, transaction_key_values=transaction_key_values)

    file_data = _walk(basedir_name)

    bundler = Bundler(meta_data, file_data)

    return bundler


def _to_meta_data(transaction: Transaction,
                  transaction_key_values: typing.List[TransactionKeyValue]) -> MetaData:
    meta_objs = []

    if transaction is not None:
        for name in ['_id']:
            value = getattr(transaction, name, None)

            if value is not None:
                raise TransactionDuplicateAttributeError(None, name)

        for name in ['analytical_tool', 'description', 'instrument', 'project', 'submitter', 'suspense_date']:
            value = getattr(transaction, name, None)

            if value is not None:
                meta_obj = MetaObj(destinationTable='Transactions.{0}'.format(name), value=value)

                meta_objs.append(meta_obj)

    for transaction_key_value in transaction_key_values:
        meta_obj = MetaObj(destinationTable='TransactionKeyValue',
                           key=transaction_key_value.key, value=transaction_key_value.value)

        meta_objs.append(meta_obj)

    meta_data = MetaData(meta_objs)

    return meta_data


def _walk(basedir_name: str) -> typing.List[typing.Dict[str, typing.Any]]:
    accum_value = []

    for orig_walk_root, _walk_dirs, file_names in os.walk(basedir_name):
        new_walk_root = orig_walk_root[(len(basedir_name) + 1):]

        for file_name in file_names:
            orig_path = os.path.join(orig_walk_root, file_name)
            new_path = os.path.join(new_walk_root, file_name)

            orig_path_st = os.stat(orig_path)

            # NOTE Character encoding is undetermined.
            # NOTE Paths need to be unix for tar format.
            accum_value.append({
                'fileobj': open(orig_path, mode='r'),
                'name': 'data/{}'.format(new_path.replace(os.path.sep, '/')),
                'size': orig_path_st.st_size,
                # NOTE Should the next line be uncommented?
                # 'ctime': orig_path_st.st_ctime,
                'mtime': orig_path_st.st_mtime,
            })

    return accum_value


# pylint: disable=too-few-public-methods
class UploaderRunner(abc.ABC):
    """Abstract base class for uploading."""

    # pylint: disable=line-too-long
    @abc.abstractmethod
    def upload(self, basedir_name: str, transaction: Transaction = None,
               transaction_key_values: typing.List[TransactionKeyValue] = None,
               timeout: int = 180) -> typing.Tuple[Bundler, int, typing.Dict[str, typing.Any]]:
        """Upload interface method."""
        raise NotImplementedError()  # pragma: no cover
    # pylint: enable=line-too-long


class LocalUploaderRunner(UploaderRunner):
    """Handle uploading to a local directory."""

    # pylint: disable=line-too-long
    def upload(self, basedir_name: str, transaction: Transaction = None,
               transaction_key_values: typing.List[TransactionKeyValue] = None,
               timeout: int = 180) -> typing.Tuple[Bundler, int, typing.Dict[str, typing.Any]]:
        """Fake upload by bundling up data to output directory."""
        if transaction_key_values is None:
            transaction_key_values = []
        bundler = _to_bundler(
            basedir_name,
            transaction=transaction,
            transaction_key_values=transaction_key_values
        )

        # NOTE Prevent "ResourceWarning: unclosed file" warnings.
        for file_data in bundler.file_data:
            file_descriptor = file_data.get('fileobj', None)

            if (file_descriptor is not None) and not file_descriptor.closed:
                file_descriptor.close()

        return (bundler, None, {})
    # pylint: enable=line-too-long


class RemoteUploaderRunner(UploaderRunner):
    """Handle uploading to a remote Pacifica instance."""

    def __init__(self, uploader: Uploader):
        """Save the uploader class instance."""
        super(RemoteUploaderRunner, self).__init__()
        self.uploader = uploader

    # pylint: disable=line-too-long
    def upload(self, basedir_name: str, transaction: Transaction = None,
               transaction_key_values: typing.List[TransactionKeyValue] = None,
               timeout: int = 180) -> typing.Tuple[Bundler, int, typing.Dict[str, typing.Any]]:
        """Perform the upload to Pacifica."""
        if transaction_key_values is None:
            transaction_key_values = []
        bundler = _to_bundler(
            basedir_name,
            transaction=transaction,
            transaction_key_values=transaction_key_values
        )

        try:
            bundler_file = tempfile.NamedTemporaryFile(delete=False)
            bundler.stream(bundler_file)
            bundler_file.close()

            with open(bundler_file.name, mode='r') as bundler_file_descriptor:
                job_id = self.uploader.upload(
                    bundler_file_descriptor,
                    content_length=os.stat(bundler_file.name).st_size
                )

            state = self.uploader.getstate(job_id)

            while timeout and _should_sleep(**state):
                time.sleep(1)
                timeout -= 1
                state = self.uploader.getstate(job_id)

            return (bundler, job_id, state)
        finally:
            os.unlink(bundler_file.name)
    # pylint: enable=line-too-long
# pylint: enable=too-few-public-methods


__all__ = ('UploaderRunner', 'LocalUploaderRunner', 'RemoteUploaderRunner', )
