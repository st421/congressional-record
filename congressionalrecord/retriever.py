import logging
import requests

LOG = logging.getLogger(__name__)


class CRRetriever(object):
    BASE_URL = 'https://www.govinfo.gov/content/pkg/'
    user_agent = {
        'user-agent': 'congressional-record 0.0.1 (https://github.com/unitedstates/congressional-record)'
    }

    def __init__(self, session=None, *args, **kwargs):
        if not session:
            session = requests.Session()
            session.headers.update(self.user_agent)
        self.session = session

    def get_cr(self, route, **kwargs):
        url = self.BASE_URL + route
        LOG.info("Requesting data at %s", url)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.content
