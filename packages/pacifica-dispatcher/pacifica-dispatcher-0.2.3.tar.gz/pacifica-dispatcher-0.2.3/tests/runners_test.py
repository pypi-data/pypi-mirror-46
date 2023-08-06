#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/runners_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test the runners."""
import os
import tempfile
import unittest

from pacifica.dispatcher.downloader_runners import LocalDownloaderRunner
from pacifica.dispatcher.models import File, Transaction, TransactionKeyValue
from pacifica.dispatcher.uploader_runners import LocalUploaderRunner


class LocalRunnerTestCase(unittest.TestCase):
    """Test the runners."""

    # pylint: disable=too-many-locals
    def test_local_runners(self):
        """Test local runners."""
        transaction = Transaction(submitter=1, instrument=1, project=1)

        transaction_key_values = [
            TransactionKeyValue(key='Transactions._id', value=1),
        ]

        files = [
            File(name='filename.ext', subdir='filepath')
        ]

        file_strs = [
            'Hello, world!'
        ]

        self.assertEqual(len(files), len(file_strs))

        with tempfile.TemporaryDirectory() as basedir_name:
            for file, file_str in zip(files, file_strs):
                os.makedirs(os.path.join(basedir_name, os.path.dirname(file.path)))

                with open(os.path.join(basedir_name, file.path), mode='w') as file_data:
                    file_data.write(file_str)

                with open(os.path.join(basedir_name, file.path), mode='r') as file_data:
                    self.assertEqual(file_str, file_data.read())

            downloader_runner = LocalDownloaderRunner(basedir_name)

            with tempfile.TemporaryDirectory() as downloader_tempdir_name:
                openers = downloader_runner.download(downloader_tempdir_name, files=files)

                self.assertEqual(len(files), len(openers))

                with tempfile.TemporaryDirectory() as uploader_tempdir_name:
                    uploader_runner = LocalUploaderRunner()

                    for file, opener in zip(files, openers):
                        os.makedirs(os.path.join(uploader_tempdir_name, os.path.dirname(file.path)))

                        with opener() as orig_f:
                            with open(os.path.join(uploader_tempdir_name, file.path), mode='w') as new_f:
                                new_f.write(orig_f.read().upper())

                        with opener() as orig_f:
                            with open(os.path.join(uploader_tempdir_name, file.path), mode='r') as new_f:
                                self.assertEqual(orig_f.read().upper(), new_f.read())

                    (bundle, job_id, state) = uploader_runner.upload(
                        uploader_tempdir_name,
                        transaction=transaction,
                        transaction_key_values=transaction_key_values
                    )

                    self.assertTrue(bundle.md_obj.is_valid())

                    self.assertEqual(len(files), len(bundle.file_data))

                    for file, file_data in zip(files, bundle.file_data):
                        self.assertEqual('data/{}'.format(file.path.replace(os.path.sep, '/')),
                                         file_data.get('name', None))

                    self.assertEqual(None, job_id)
                    self.assertEqual({}, state)
    # pylint: enable=too-many-locals


class RemoteRunnerTestCase(unittest.TestCase):
    """Test remote runners."""

    def test_remote_runners(self):
        """Test remote runners."""


if __name__ == '__main__':
    unittest.main()
