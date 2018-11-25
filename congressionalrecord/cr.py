from __future__ import absolute_import

import logging
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from zipfile import ZipFile
from io import BytesIO

from congressionalrecord.parsing.file_parser import ParseCRFile
from congressionalrecord.retriever import CRRetriever

LOG = logging.getLogger(__name__)


class CRManager(object):
    DATE_FORMAT = "%Y-%m-%d"
    CR_PREFIX = "CREC-"
    DEFAULT_SKIP_PARSING = ['-Pgnull', 'FrontMatter']

    def __init__(self, day, parser_class=None, retriever=None, *, skip_parsing_for=None, output_format=None, **kwargs):
        if not retriever:
            retriever = CRRetriever()
        if not parser_class:
            parser_class = ParseCRFile
        if isinstance(day, str):
            day = datetime.strptime(day, self.DATE_FORMAT)
        if not skip_parsing_for:
            skip_parsing_for = self.DEFAULT_SKIP_PARSING

        self.skip_parsing_for = skip_parsing_for
        self.output_format = output_format
        self.retriever = retriever
        self.parser_class = parser_class
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


class LocalCRManager(CRManager):

    def __init__(self, day, *args, output_dir="output", **kwargs):
        super().__init__(day, *args, **kwargs)
        self.output_dir = output_dir

    def __call__(self):
        if not os.path.isdir(self.html_path):
            self.extract(self.retriever.get_cr(self.unextracted))
        self.parse()

    @property
    def output_path(self):
        return os.path.join(self.output_dir, self.filename)

    @property
    def unextracted(self):
        return self.filename + ".zip"

    @property
    def html_path(self):
        return os.path.join(self.output_path, 'html')

    @property
    def output_zip(self):
        return os.path.join(self.output_dir, self.unextracted)

    def extract(self, cr_data, **kwargs):
        if cr_data:
            LOG.info("Extracting data to %s", self.output_path)
            with ZipFile(BytesIO(cr_data)) as out_data:
                out_data.extractall(self.output_dir)
        else:
            LOG.info("No data to extract for %s", self.day)

    def get_mods(self, **kwargs):
        ''' Load up all metadata for this directory
         from the mods file.'''
        mods_path = os.path.join(self.output_path, 'mods.xml')
        with open(mods_path, 'r') as mods_file:
            return BeautifulSoup(mods_file, "lxml")

    def parse(self, **kwargs):
        if self.output_format:
            subfolder = os.path.join(self.output_path, self.output_format)
            if not os.path.isdir(subfolder):
                os.makedirs(subfolder)
        for html_file in os.listdir(self.html_path):
            parse_path = os.path.join(self.html_path, html_file)
            for skip_str in self.skip_parsing_for:
                print(skip_str)
                if skip_str in parse_path:
                    continue
                else:
                    crfile = ParseCRFile(parse_path, self.output_path)
                    yield crfile


class LocalJsonCRManager(LocalCRManager):

    def __init__(self, day, *args, **kwargs):
        super().__init__(day, *args, output_format="json", **kwargs)

    def parse(self, **kwargs):
        for crfile in super().parse():
            with open(os.path.join(self.output_path, self.output_format, crfile.filepath), 'w') as out_json:
                json.dump(crfile.crdoc, out_json)
