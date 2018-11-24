from __future__ import absolute_import

import os
import logging
from datetime import datetime

import certifi
import urllib3.contrib.pyopenssl
from urllib3 import PoolManager, Retry, Timeout

urllib3.contrib.pyopenssl.inject_into_urllib3()


class CRRetriever(object):
    BASE_URL = 'https://www.govinfo.gov/content/pkg/'
    user_agent = {
        'user-agent': 'congressional-record 0.0.1 (https://github.com/unitedstates/congressional-record)'
    }

    def __init__(self, connection_manager=None, *args, **kwargs):
        if not connection_manager:
            timeout = Timeout(connect=2.0, read=10.0)
            retry = Retry(total=3, backoff_factor=300)
            retry.BACKOFF_MAX = 602
            connection_manager = PoolManager(
                timeout=timeout,
                retries=retry,
                cert_reqs='CERT_REQUIRED',
                ca_certs=certifi.where(),
                headers=self.user_agent)
        self.connection_manager = connection_manager

    def get_cr(self, route, **kwargs):
        resp = self.connection_manager.request('GET', self.BASE_URL + route)
        if resp.status not in [200, 201]:
            raise Exception("Error during download: {0}".format(str(resp.status)))
        return resp.data
