#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/models_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test the models for storing data."""
import os
import unittest

from cloudevents.constants import SPEC_VERSION
from cloudevents.model import Event

from pacifica.dispatcher.exceptions import TransactionDuplicateAttributeError
from pacifica.dispatcher.models import File, Transaction, TransactionKeyValue


# pylint: disable=too-many-instance-attributes
class PacificaModelTestCase(unittest.TestCase):
    """Test the models for storing data."""

    def setUp(self):
        """Create a hand full of data objects."""
        self._file_data = {
            'destinationTable': 'Files',
            '_id': 1,
            'name': 'filename.ext',
            'subdir': 'filepath',
        }
        self._transaction_id_data = {
            'destinationTable': 'Transactions._id',
            'value': 1,
        }
        self._transaction_key_value_data = {
            'destinationTable': 'TransactionKeyValue',
            'key': 'key',
            'value': 'value',
        }

        self._event_data = []
        self._event_data.append(self._file_data)
        self._event_data.append(self._transaction_id_data)
        self._event_data.append(self._transaction_key_value_data)

        self._event_ok = Event({
            'cloudEventsVersion': SPEC_VERSION,
            'eventID': '1',
            'eventType': 'io.cloudevents',
            'source': '/cloudevents/io',
            'data': self._event_data,
        })

        self._event_data_error_duplicated_attr = self._event_data.copy()
        self._event_data_error_duplicated_attr.append(self._transaction_id_data)
        self._event_error_duplicated_attr = Event({
            'cloudEventsVersion': SPEC_VERSION,
            'eventID': '1',
            'eventType': 'io.cloudevents',
            'source': '/cloudevents/io',
            'data': self._event_data_error_duplicated_attr,
        })

    def test_file_from_cloudevents_model_ok(self):
        """Create a file from cloud event."""
        inst_list = File.from_cloudevents_model(self._event_ok)
        self.assertEqual(1, len(inst_list))

        for name in ['_id', 'name', 'subdir']:
            self.assertEqual(self._file_data.get(name, None), getattr(inst_list[0], name, None))

    def test_file_path_error(self):
        """Create a file with invalid path."""
        inst = File()
        with self.assertRaises(AttributeError):
            # pylint: disable=pointless-statement
            inst.path
            # pylint: enable=pointless-statement

    def test_file_path_ok_name(self):
        """Create a file and verify path flows through it correctly."""
        inst = File(name=self._file_data.get('name', None))
        self.assertEqual(self._file_data.get('name', None), inst.path)

    def test_file_path_ok_name_subdir(self):
        """Create a file and verify path and subdir flow through it correctly."""
        inst = File(name=self._file_data.get('name', None), subdir=self._file_data.get('subdir', None))
        self.assertEqual(os.path.join(self._file_data.get('subdir', None),
                                      self._file_data.get('name', None)), inst.path)

    def test_transaction_from_cloudevents_model_ok(self):
        """Create a transaction from cloud event."""
        inst = Transaction.from_cloudevents_model(self._event_ok)
        # pylint: disable=protected-access
        self.assertEqual(self._transaction_id_data.get('value', None), inst._id)
        # pylint: enable=protected-access

    def test_transaction_from_cloudevents_model_error_duplicated_attr(self):
        """Create a transaction from cloud event that already exists."""
        with self.assertRaises(TransactionDuplicateAttributeError):
            Transaction.from_cloudevents_model(self._event_error_duplicated_attr)

    def test_transaction_key_value_from_cloudevents_model_ok(self):
        """Create a transaction key value from cloud event."""
        inst_list = TransactionKeyValue.from_cloudevents_model(self._event_ok)
        self.assertEqual(1, len(inst_list))
        for name in ['key', 'value']:
            self.assertEqual(self._transaction_key_value_data.get(name, None), getattr(inst_list[0], name, None))


if __name__ == '__main__':
    unittest.main()
