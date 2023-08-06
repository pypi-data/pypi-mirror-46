#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The Downloader internal Module."""
import tarfile
import requests
from .cloudevent import CloudEvent
from .cartapi import CartAPI
from .policy import TransactionInfo


class Downloader(object):
    """
    Downloader Class.

    The other methods in this class are the supported
    download methods. Each method takes appropriate input for that
    method and the method will download the data to the location
    specified in the method's arguments.
    """

    def __init__(self, **kwargs):
        """
        Create the downloader.

        Keyword arguments are delegated to the CartAPI.
        """
        self.cart_api = CartAPI(**kwargs)

    def _download_from_url(self, location, cart_url, filename):
        """
        Download the cart from the url.

        The cart url is returned from the CartAPI.
        """
        resp = requests.get(
            '{}?filename={}'.format(cart_url, filename),
            stream=True, **self.cart_api.auth
        )
        cart_tar = tarfile.open(name=None, mode='r|', fileobj=resp.raw)
        cart_tar.extractall(location)
        cart_tar.close()

    def transactioninfo(self, location, transinfo, filename='data'):
        """
        Handle transaction info and download the data in a cart.

        Transaction info objects are pulled from the
        `PolicyAPI <https://pacifica-policy.readthedocs.io/>`_.
        """
        self._download_from_url(
            location,
            self.cart_api.wait_for_cart(
                self.cart_api.setup_cart(
                    TransactionInfo.yield_files(transinfo)
                )
            ),
            filename
        )

    def cloudevent(self, location, cloudevent, filename='data'):
        """
        Handle a cloud event and download the data in a cart.

        `CloudEvents <https://github.com/cloudevents/spec>`_
        is a specification for passing information about
        changes in cloud infrastructure or state. This method
        consumes events produced by the
        `Pacifica Notifications <https://github.com/pacifica/pacifica-notifications>`_
        service.
        """
        self._download_from_url(
            location,
            self.cart_api.wait_for_cart(
                self.cart_api.setup_cart(
                    CloudEvent.yield_files(cloudevent)
                )
            ),
            filename
        )
