#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Test the example module."""
from shutil import rmtree
from os.path import exists, join
from tempfile import mkdtemp
from hashlib import sha1
from unittest import TestCase
import requests
from pacifica.downloader import Downloader


class TestDownloader(TestCase):
    """Test the Downloader class."""

    def test_cart_api_url(self):
        """Test the CartAPI URL."""
        down = Downloader(proto='http', addr='127.0.0.1', port=8081)
        self.assertEqual(down.cart_api.cart_api_url, 'http://127.0.0.1:8081')

    def test_download_policy(self):
        """Test the download with policy."""
        down_path = mkdtemp()
        down = Downloader(cart_api_url='http://127.0.0.1:8081')
        resp = requests.get('http://127.0.0.1:8181/status/transactions/by_id/67')
        self.assertEqual(resp.status_code, 200)
        down.transactioninfo(down_path, resp.json())
        self.assertTrue(exists(join(down_path, 'data', 'a', 'b', 'foo.txt')))
        self.assertTrue(exists(join(down_path, 'data', 'a', 'b', u'\u00e9', u'bar\u00e9.txt')))
        rmtree(down_path)

    def test_download_cloudevent(self):
        """Test the download method in example class."""
        def sha1sum(text_data):
            """sha1sum the text_data and return string for sha1."""
            hashsum = sha1()
            hashsum.update(text_data)
            return hashsum.hexdigest()
        cloud_event_stub = {
            'data': [
                {
                    'destinationTable': 'Files',
                    '_id': file_id,
                    'name': 'file.{}.txt'.format(file_id),
                    'subdir': 'subdir_{}'.format(file_id),
                    'hashsum': sha1sum('The data for file {}.\n'.format(file_id).encode('utf8')),
                    'hashtype': 'sha1'
                } for file_id in range(1100, 1110)
            ]
        }
        down_path = mkdtemp()
        down = Downloader(cart_api_url='http://127.0.0.1:8081')
        down.cloudevent(down_path, cloud_event_stub)
        for file_id in range(1100, 1110):
            self.assertTrue(
                exists(join(down_path, 'data', 'subdir_{}'.format(file_id), 'file.{}.txt'.format(file_id))))
        rmtree(down_path)
