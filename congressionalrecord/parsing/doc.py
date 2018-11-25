import re
import inspect
from bs4 import BeautifulSoup
from congressionalrecord.parsing.base import BaseDocParser
from congressionalrecord.parsing.body import CRBodyParser

class CRHtmlParser(BaseDocParser):

    @property
    def id(self):
        return self.filename

    @property
    def headers(self):
        return None

    @property
    def title(self):
        return BeautifulSoup(self.in_data, "lxml").html.head.title.text

    def parse(self, *args, **kwargs):
        return {
            "id": self.id,
            "title": self.title,
            "content": CRBodyParser().generate_ans(self.in_data, start_tag="html.body.pre")
        }
'''
    def get_header(self):
        """
        Only after I wrote this did I realize
        how bad things can go when you call
        next() on an iterator instead of treating
        it as a list.

        This code works, though.
        """
        header_in = next(self.the_text)
        if header_in == u'':
            header_in = next(self.the_text)
        match = re.match(self.re_vol_file, header_in)
        if match:
            vol, num, wkday, month, day, year = match.group(
                'vol', 'num', 'wkday', 'month', 'day', 'year')
        else:
            return False
        header_in = next(self.the_text)
        match = re.match(self.re_chamber, header_in)
        if match:
            if match.group('chamber') == 'Extensions of Remarks':
                chamber = 'House'
                extensions = True
            else:
                chamber = match.group('chamber')
                extensions = False
        else:
            return False
        header_in = next(self.the_text)
        match = re.match(self.re_pages, header_in)
        if match:
            pages = match.group('pages')
        else:
            return False
        header_in = next(self.the_text)
        match = re.match(self.re_trail, header_in)
        if match:
            pass
        else:
            return False
        return vol, num, wkday, month, day, year, chamber, pages, extensions

    def write_header(self):
        self.crdoc['id'] = self.access_path
        header = self.get_header()
        if header:
            self.crdoc['header'] = {'vol': header[0], 'num': header[1],
                                    'wkday': header[2], 'month': header[3], 'day': header[4],
                                    'year': header[5], 'chamber': header[6], 'pages': header[7],
                                    'extension': header[8]}
        self.crdoc['doc_title'] = self.doc_title
'''