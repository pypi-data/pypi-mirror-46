#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pacifica-dispatcher: pacifica/dispatcher/downloader_runners.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE for details.
"""
Download runner module.

This module contains two download runners. The first is for
downloading from a local directory (works well for testing). The
second is for downloading from a remote Pacifica Cartd service.

Additional methods for downloading could be used in the future.
"""
import abc
import functools
import os
import typing

from pacifica.downloader import Downloader

from .models import File


def _to_opener(basedir_name: str, file: File) -> typing.Callable[[typing.Dict[str, typing.Any]], typing.TextIO]:
    """Partial method to open files."""
    def func(**kwargs):
        """Python open wrapper to only open file relative to basedir_name."""
        return open(
            os.path.join(basedir_name, file.path),
            mode='r',
            encoding=file.encoding,
            **kwargs
        )
    return func


# pylint: disable=too-few-public-methods
class DownloaderRunner(abc.ABC):
    """Abstract downloader class for downloading files."""

    # pylint: disable=line-too-long
    @abc.abstractmethod
    def download(self, basedir_name: str,
                 files: typing.List[File] = None,
                 timeout: int = 180) -> typing.List[typing.Callable[[typing.Dict[str, typing.Any]], typing.TextIO]]:  # NOQA: E501
        """Abstract download method to define interface for downloading files."""
        raise NotImplementedError()  # pragma: no cover
    # pylint: enable=line-too-long


class LocalDownloaderRunner(DownloaderRunner):
    """
    Local download class.

    This class is used for running the handlers on previously
    downloaded data relative to some base directory.
    """

    def __init__(self, basedir_name: str) -> None:
        """Save the base directory to the instance of the class."""
        super(LocalDownloaderRunner, self).__init__()

        self.basedir_name = basedir_name

    # pylint: disable=line-too-long
    def download(self, basedir_name: str,
                 files: typing.List[File] = None,
                 timeout: int = 180) -> typing.List[typing.Callable[[typing.Dict[str, typing.Any]], typing.TextIO]]:  # NOQA: E501
        """
        Download the files locally.

        The download base directory may not match the class instance
        base directory. If that's the case symlink the files from the
        instance base directory to the called base directory.

        Either case return a list of methods used to open the files.
        """
        if not files:
            raise ValueError('Files should contain something.')
        if self.basedir_name != basedir_name:
            for file in files:
                if file.subdir is not None:
                    os.makedirs(os.path.join(basedir_name, file.subdir), exist_ok=True)

                os.symlink(os.path.join(self.basedir_name, file.path), os.path.join(basedir_name, file.path))

        openers = list(map(functools.partial(_to_opener, basedir_name), files))

        return openers
    # pylint: enable=line-too-long


class RemoteDownloaderRunner(DownloaderRunner):
    """
    Remote download runner class.

    This class downloads data from a Pacifica Cartd service to a
    local directory.
    """

    def __init__(self, downloader: Downloader) -> None:
        """
        Initialize the remote downloader class.

        The class is initialized with an instance of the
        ``pacifica.downloader.Downloader`` class.
        """
        super(RemoteDownloaderRunner, self).__init__()

        self.downloader = downloader

    # pylint: disable=line-too-long
    def download(self, basedir_name: str,
                 files: typing.List[File] = None,
                 timeout: int = 180) -> typing.List[typing.Callable[[typing.Dict[str, typing.Any]], typing.TextIO]]:  # NOQA: E501
        """
        Download the files using the downloader.

        The downloader is used to setup a cart of data from the Cartd
        service. The downloader used in it's blocking form, setting
        up the cart, waiting for it to complete and downloading it.

        Once complete a list of methods is returned for opening files.
        """
        if not files:
            raise ValueError('Files should contain something.')

        def yield_files():
            """Yield files for setup cart."""
            for file in files:
                # pylint: disable=protected-access
                yield {
                    'id': file._id,
                    'hashsum': file.hashsum,
                    'hashtype': file.hashtype,
                    'path': file.path,
                }
                # pylint: enable=protected-access

        # pylint: disable=protected-access
        self.downloader._download_from_url(
            basedir_name,
            self.downloader.cart_api.wait_for_cart(
                self.downloader.cart_api.setup_cart(yield_files),
                timeout
            ),
            'data'
        )

        openers = list(
            map(
                functools.partial(
                    _to_opener,
                    os.path.join(basedir_name, 'data')
                ),
                files
            )
        )

        return openers
    # pylint: enable=line-too-long
# pylint: enable=too-few-public-methods


__all__ = ('DownloaderRunner', 'LocalDownloaderRunner', 'RemoteDownloaderRunner', )
