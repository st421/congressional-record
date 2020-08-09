import logging
from datetime import datetime
import requests
from congressionalrecord.utils import DATE_FORMAT

LOG = logging.getLogger(__name__)


class CongressClient(object):
    BASE_URL = 'https://www.congress.gov/congressional-record'

    def __init__(self, session=None, *args, **kwargs):
        if not session:
            session = requests.Session()
            session.headers.update({
                'user-agent': 'congressional-record (https://github.com/unitedstates/congressional-record)'
            })
        self.session = session

    def make_request(self, route, **kwargs):
        url = self.BASE_URL + route
        LOG.info("Requesting data at %s", url)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.content

    def get_cr_daily_digest(self, date, **kwargs):
        date_with_slashes = datetime.strftime(datetime.strptime(date, DATE_FORMAT), "%Y/%m/%d")
        return self.make_request(f"/{date_with_slashes}/daily-digest")
