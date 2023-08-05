#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/uploader_runners_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test the uploader runner."""
import os
import tempfile
import unittest

from pacifica.uploader import Uploader

from pacifica.dispatcher.exceptions import TransactionDuplicateAttributeError
from pacifica.dispatcher.models import Transaction, TransactionKeyValue
from pacifica.dispatcher.uploader_runners import LocalUploaderRunner, RemoteUploaderRunner


class LocalUploaderRunnerTestCase(unittest.TestCase):
    """Test the local uploader runner."""

    def test_local_uploader_runner(self):
        """Test the local uploader runner."""
        with tempfile.TemporaryDirectory() as uploader_tempdir_name:
            os.makedirs(os.path.join(uploader_tempdir_name, 'filepath'))

            f_data = 'Hello, world!'

            with open(os.path.join(uploader_tempdir_name, 'filepath', 'filename.ext'), mode='w') as test_file:
                test_file.write(f_data)

            with open(os.path.join(uploader_tempdir_name, 'filepath', 'filename.ext'), mode='r') as test_file:
                self.assertEqual(f_data, test_file.read())

            uploader_runner = LocalUploaderRunner()

            with self.assertRaises(TransactionDuplicateAttributeError):
                (bundle, job_id, state) = uploader_runner.upload(
                    uploader_tempdir_name,
                    transaction=Transaction(_id=1, submitter=1, instrument=1, project=1),
                    transaction_key_values=[TransactionKeyValue(key='Transactions._id', value=1)]
                )

            (bundle, job_id, state) = uploader_runner.upload(
                uploader_tempdir_name,
                transaction=Transaction(submitter=1, instrument=1, project=1),
                transaction_key_values=[TransactionKeyValue(key='Transactions._id', value=1)]
            )
            self.assertTrue(bundle.md_obj.is_valid())
            self.assertEqual(1, len(bundle.file_data))
            self.assertEqual('data/filepath/filename.ext', bundle.file_data[0].get('name', None))
            self.assertEqual(None, job_id)
            self.assertEqual({}, state)

            (bundle, job_id, state) = uploader_runner.upload(
                uploader_tempdir_name,
                transaction=Transaction(submitter=1, instrument=1, project=1)
            )
            self.assertTrue(bundle.md_obj.is_valid())
            self.assertEqual(1, len(bundle.file_data))
            self.assertEqual('data/filepath/filename.ext', bundle.file_data[0].get('name', None))
            self.assertEqual(None, job_id)
            self.assertEqual({}, state)


class RemoteUploaderRunnerTestCase(unittest.TestCase):
    """Test the remote uploader runner."""

    def test_remote_uploader_runner(self):
        """Test the remote uploader runner."""
        with tempfile.TemporaryDirectory() as uploader_tempdir_name:
            os.makedirs(os.path.join(uploader_tempdir_name, 'filepath'))

            f_data = 'Hello, world!'

            with open(os.path.join(uploader_tempdir_name, 'filepath', 'filename.ext'), mode='w') as test_file:
                test_file.write(f_data)

            uploader_runner = RemoteUploaderRunner(Uploader())

            (bundle, job_id, state) = uploader_runner.upload(
                uploader_tempdir_name,
                transaction=Transaction(submitter=10, instrument=54, project='1234a'),
                transaction_key_values=[TransactionKeyValue(key='Transactions._id', value=1)]
            )
            self.assertTrue(bundle.md_obj.is_valid())
            self.assertEqual(1, len(bundle.file_data))
            self.assertEqual('data/filepath/filename.ext', bundle.file_data[0].get('name', None))
            self.assertEqual(1, job_id)
            print(state)
            self.assertEqual(state['job_id'], 1)
            self.assertEqual(state['state'], 'OK')
            self.assertEqual(state['task'], 'ingest metadata')
            self.assertEqual(int(float(state['task_percent'])), 100)

            (bundle, job_id, state) = uploader_runner.upload(
                uploader_tempdir_name,
                transaction=Transaction(submitter=10, instrument=54, project='1234a')
            )
            self.assertTrue(bundle.md_obj.is_valid())
            self.assertEqual(1, len(bundle.file_data))
            self.assertEqual('data/filepath/filename.ext', bundle.file_data[0].get('name', None))
            self.assertEqual(2, job_id)
            self.assertEqual(state['job_id'], 2)
            self.assertEqual(state['state'], 'OK')
            self.assertEqual(state['task'], 'ingest metadata')
            self.assertEqual(int(float(state['task_percent'])), 100)


if __name__ == '__main__':
    unittest.main()
