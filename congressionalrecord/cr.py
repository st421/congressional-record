from __future__ import absolute_import

import logging
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from zipfile import ZipFile
from io import BytesIO

from congressionalrecord.parsing.doc import CRHtmlParser, CRChamberHtmlParser, CRDailyDigestHtmlParser, CRExtensionsHtmlParser
from congressionalrecord.retriever import CRRetriever

LOG = logging.getLogger(__name__)


class CRManager(object):
    DATE_FORMAT = "%Y-%m-%d"
    CR_PREFIX = "CREC-"
    DEFAULT_SKIP_PARSING = ['-Pgnull', 'FrontMatter']
    PARSER_CLASSES = {
        'H': CRChamberHtmlParser,
        'S': CRChamberHtmlParser,
        'D': CRDailyDigestHtmlParser,
        'E': CRExtensionsHtmlParser
    }

    def __init__(self, day, retriever=None, *, skip_parsing_for=None, output_format=None, **kwargs):
        if not retriever:
            retriever = CRRetriever()
        if isinstance(day, str):
            day = datetime.strptime(day, self.DATE_FORMAT)
        if not skip_parsing_for:
            skip_parsing_for = self.DEFAULT_SKIP_PARSING

        self.skip_parsing_for = skip_parsing_for
        self.output_format = output_format
        self.retriever = retriever
        self.day = day

    @property
    def filename(self):
        return self.build_filename(self.day)

    @classmethod
    def build_filename(cls, day, **kwargs):
        day_str = datetime.strftime(day, cls.DATE_FORMAT)
        return f"{cls.CR_PREFIX}{day_str}"

    def __call__(self):
        raise NotImplementedError()


class YieldingCRManager(CRManager):

    def __init__(self, day, *args, base_output_dir="output", **kwargs):
        super().__init__(day, *args, **kwargs)
        self.base_output_dir = base_output_dir

    def __call__(self):
        if not os.path.isdir(self.html_dir):
            self.extract(self.retriever.get_cr(self.filename + ".zip"))
        self.parse()

    @property
    def output_dir(self):
        return os.path.join(self.base_output_dir, self.filename)

    @property
    def html_dir(self):
        return os.path.join(self.output_dir, 'html')

    @property
    def mods(self):
        ''' Load up all metadata for this directory
         from the mods file.'''
        mods_path = os.path.join(self.output_dir, 'mods.xml')
        return open(mods_path, 'r')

    @property
    def html(self):
        ''' Load up all html '''
        html_files = []
        for html_file in os.listdir(self.html_dir):
            html_path = os.path.join(self.html_dir, html_file)
            skip = False
            for skip_str in self.skip_parsing_for:
                if skip_str in html_path:
                    skip = True
            if not skip:
                html_files.append(open(html_path, 'r'))
        return html_files

    def extract(self, cr_data, **kwargs):
        if cr_data:
            LOG.info("Extracting data to %s", self.output_dir)
            with ZipFile(BytesIO(cr_data)) as out_data:
                out_data.extractall(self.base_output_dir)
        else:
            LOG.info("No data to extract for %s", self.day)

    def parse(self, **kwargs):
        # TODO do something with mods
        for html_file in self.html:
            for doc_type in self.PARSER_CLASSES:
                if f"Pg{doc_type}" in html_file.name:
                    yield os.path.basename(html_file.name), self.PARSER_CLASSES.get(doc_type)(html_file).parse()


class LocalCRManager(YieldingCRManager):

    def __init__(self, *args, parsed_output_folder=None, **kwargs):
        super().__init__(*args, **kwargs)
        if self.output_format and not parsed_output_folder:
            parsed_output_folder = os.path.join(self.output_dir, self.output_format)
            if not os.path.isdir(parsed_output_folder):
                os.makedirs(parsed_output_folder)
        self.parsed_output_folder = parsed_output_folder

    def parse(self, **kwargs):
        self.write(super().parse(**kwargs))

    def write(self, data, **kwargs):
        raise NotImplementedError()


class LocalJsonCRManager(LocalCRManager):

    def __init__(self, day, *args, **kwargs):
        super().__init__(day, *args, output_format="json", **kwargs)

    def write(self, data, **kwargs):
        for file_name, parsed in data:
            with open(os.path.join(self.output_dir, self.output_format, file_name.replace(".htm", ".json")), 'w') as out_file:
                json.dump(parsed, out_file)
