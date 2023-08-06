#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Cart API module for interacting with carts."""
import logging
from uuid import uuid4 as uuid
import time
from json import dumps
from .common import CommonBase


LOGGER = logging.getLogger(__name__)


class CartAPI(CommonBase):
    """
    Cart api object for manipulating carts.

    This class has two methods used for setting up a cart and waiting
    for completion.
    """

    _proto = None
    _addr = None
    _port = None
    _cart_api_url = None
    _auth = None

    def __init__(self, **kwargs):
        """
        Constructor for cart api.

        The constructor takes a required URL to the Cart API.
        Optionally, there can be passed a
        `requests <https://docs.python-requests.org>`_ session via
        keyword arguments. Also, an optional requests authentication
        dictionary can be passed via keyword arguments.
        """
        super(CartAPI, self).__init__()

        self._setup_requests_session()
        self.session = kwargs.get('session', self.session)

        self._server_url(
            [
                ('proto', 'http'),
                ('port', '8081'),
                ('addr', '127.0.0.1'),
                ('cart_api_url', None),
            ],
            'CARTD',
            kwargs
        )

        if self._cart_api_url is None:
            self._cart_api_url = '{}://{}:{}'.format(self._proto, self._addr, self._port)

        self._auth = kwargs.get('auth', {})

        LOGGER.debug('CartAPI URL %s auth %s', self._cart_api_url, self._auth)

    @property
    def auth(self):
        """Return the requests authentication dictionary."""
        return self._auth

    @property
    def cart_api_url(self):
        """Return the CartAPI URL."""
        return self._cart_api_url

    def setup_cart(self, yield_files):
        """
        Setup a cart from the method and return url to the download.

        This method takes a callable argument that returns an iterator.
        The iterator is used to generate a list that is directly sent to
        the `Cartd API <https://github.com/pacifica/pacifica-cartd>`_.
        This method returns the full url to the cart created.
        """
        cart_url = '{}/{}'.format(self._cart_api_url, uuid())
        resp = self.session.post(
            cart_url,
            data=dumps({
                'fileids': [file_obj for file_obj in yield_files()]
            }),
            headers={'Content-Type': 'application/json'},
            **self._auth
        )
        LOGGER.debug('CartAPI Setup code %s', resp.status_code)
        assert resp.status_code == 201
        return cart_url

    def wait_for_cart(self, cart_url, timeout=120):
        """
        Wait for cart completion to finish.

        This method takes a cart url returned from the
        `setup_cart()` method and polls the endpoint until the cart is
        ready to download.
        """
        while timeout > 0:
            resp = self.session.head(cart_url, **self._auth)
            resp_status = resp.headers['X-Pacifica-Status']
            resp_message = resp.headers['X-Pacifica-Message']
            resp_code = resp.status_code
            LOGGER.debug('CartAPI Wait code %s status %s message %s',
                         resp_code, resp_status, resp_message.replace('"', '\\"'))
            if resp_code == 204 and resp_status != 'staging':
                break
            if resp_code == 500:  # pragma: no cover
                logging.error(resp_message)
                break
            time.sleep(1)
            timeout -= 1
        assert resp_status == 'ready'
        assert resp_code == 204
        return cart_url
