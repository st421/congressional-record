import logging
import requests

LOG = logging.getLogger(__name__)


class GovInfoClient(object):
    BASE_URL = 'https://www.govinfo.gov/content/pkg'

    def __init__(self, session=None, *args, api_key=None, **kwargs):
        if not session:
            session = requests.Session()
            session.headers.update({
                'user-agent': 'congressional-record (https://github.com/unitedstates/congressional-record)',
                'X-API-Key': api_key
            })
        self.session = session

    def make_request(self, route, **kwargs):
        url = self.BASE_URL + route
        LOG.info("Requesting data at %s", url)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.content

    def get_zip(self, date, **kwargs):
        return self.make_request(f"/CREC-{date}.zip")
