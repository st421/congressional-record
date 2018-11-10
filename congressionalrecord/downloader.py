from __future__ import absolute_import
#import requests
from builtins import str
from builtins import object
import certifi
import urllib3.contrib.pyopenssl
from urllib3 import PoolManager, Retry, Timeout
import os
from datetime import datetime, date, timedelta
from time import sleep
from zipfile import ZipFile
import json
import logging


urllib3.contrib.pyopenssl.inject_into_urllib3()


class CRDownloader(object):

    user_agent = {
        'user-agent': 'congressional-record 0.0.1 (https://github.com/unitedstates/congressional-record)'}
    its_today = datetime.strftime(datetime.today(),'%Y-%m-%d %H:%M')
    timeout = Timeout(connect=2.0,read=10.0)
    retry = Retry(total=3,backoff_factor=300)
    retry.BACKOFF_MAX = 602
    http = PoolManager(timeout=timeout,retries=retry,
                       cert_reqs='CERT_REQUIRED',
                       ca_certs=certifi.where(),
                       headers=user_agent)
    output_prefix = "CREC-"
    output_format = "zip"
    base_url = 'https://www.govinfo.gov/content/pkg/CREC-'
    
    def download_and_write(self, route, filename):
        logging.info('Sending request on {0}'.format(self.its_today))
        resp = self.http.request('GET', self.base_url + route)
        if resp.status not in [200, 201]:
            raise Exception("Error during download: {0}".format(str(resp.status)))
        binary_content = resp.data
        with open(filename, 'wb') as outfile:
            outfile.write(binary_content)
        logging.info('Wrote {0}'.format(filename))  
