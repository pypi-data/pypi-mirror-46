#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: tests/downloader_runners_test.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""Test the Downloader Module."""
import os
import tempfile
import unittest
import hashlib

from pacifica.downloader import Downloader
from pacifica.dispatcher.downloader_runners import LocalDownloaderRunner, RemoteDownloaderRunner
from pacifica.dispatcher.models import File


class LocalDownloaderRunnerTestCase(unittest.TestCase):
    """Test the local downloader."""

    def test_local_downloader_runner(self):
        """Generate a local temporary directory and download to it."""
        with tempfile.TemporaryDirectory() as basedir_name:
            os.makedirs(os.path.join(basedir_name, 'filepath'))

            f_data = 'Hello, world!'

            with open(os.path.join(basedir_name, 'filepath', 'filename.ext'), mode='w') as test_file:
                test_file.write(f_data)

            with open(os.path.join(basedir_name, 'filepath', 'filename.ext'), mode='r') as test_file:
                self.assertEqual(f_data, test_file.read())

            downloader_runner = LocalDownloaderRunner(basedir_name)

            with tempfile.TemporaryDirectory() as downloader_tempdir_name:
                openers = downloader_runner.download(
                    downloader_tempdir_name,
                    files=[File(name='filename.ext', subdir='filepath')]
                )
                self.assertEqual(1, len(openers))
                with openers[0]() as test_file:
                    self.assertEqual(f_data, test_file.read())

    def test_local_downloader_runner_nofiles(self):
        """Generate a local temporary directory and download to it."""
        with tempfile.TemporaryDirectory() as basedir_name:
            downloader_runner = LocalDownloaderRunner(basedir_name)
            with tempfile.TemporaryDirectory() as downloader_tempdir_name:
                with self.assertRaises(ValueError):
                    downloader_runner.download(downloader_tempdir_name)


class RemoteDownloaderRunnerTestCase(unittest.TestCase):
    """Remote downloader runner."""

    def test_remote_downloader_runner(self):
        """Test the downloader runner class."""
        # Hash sum the README.md at root of repo (it's what we use to system test).
        hash_obj = hashlib.sha1()
        with open(os.path.join('..', 'README.md'), 'r') as readme_fd:
            hash_obj.update(bytes(readme_fd.read(), 'utf8'))
        hashsum = hash_obj.hexdigest()
        with tempfile.TemporaryDirectory() as basedir_name:
            downloader_runner = RemoteDownloaderRunner(Downloader())
            openers = downloader_runner.download(
                basedir_name,
                files=[
                    File(_id=103, name='foo.txt', subdir='a/b', hashtype='sha1', hashsum=hashsum),
                    File(_id=104, name='bar\u00e9.txt', subdir='a/b/\u00e9', hashtype='sha1', hashsum=hashsum)
                ]
            )
            self.assertEqual(2, len(openers))
            with openers[0]() as readme_fd:
                self.assertTrue('Pacifica Dispatcher' in readme_fd.read())

    def test_remote_downloader_runner_nofiles(self):
        """Generate a local temporary directory and download to it."""
        with tempfile.TemporaryDirectory() as basedir_name:
            downloader_runner = RemoteDownloaderRunner(Downloader())
            with self.assertRaises(ValueError):
                downloader_runner.download(basedir_name)


if __name__ == '__main__':
    unittest.main()
